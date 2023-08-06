from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import os
from typing import List
from functools import wraps

from git import Head
from git.util import IterableList

from gitflow_linter import Gitflow
from gitflow_linter.report import Section, Issue, Level
from gitflow_linter.repository import Repository, RepositoryVisitor


def arguments_checker(keywords):
    def wrap(f):
        @wraps(f)
        def new_function(*args, **kw):
            missing = [keyword for keyword in keywords if keyword not in kw.keys()]
            if len(missing) > 0:
                raise ValueError(
                    "Following arguments are missing: {}".format(', '.join(keywords)))
            return f(*args, **kw)

        return new_function

    return wrap


class BaseVisitor(RepositoryVisitor, ABC):
    """
    Abstract class describing how gitflow-linter works. A visitor must provide a rule that it is supposed to verify.
    The linter will let the visitor visit a repository only if user wants to check the repository against the rule.
    Plugins can override default visitors by returning the same rule as a visitor they wish override.
    """

    @property
    @abstractmethod
    def rule(self) -> str:
        """
        :return: Rule from YAML file that is checked by the visitor
        """
        pass

    def __init__(self, gitflow: Gitflow):
        self.gitflow = gitflow

    @abstractmethod
    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        """
        Verifies the :class:`repository <gitflow_linter.repository.Repository>` - checks if ``self.rule`` is respected

        :param repo: Tiny wrapper for GitPython's repository
        :param args:
        :param kwargs: arguments from YAML file
        :return: :class:`Section <gitflow_linter.report.Section>` with results
        """
        pass


class StatsRepositoryVisitor(RepositoryVisitor):

    def __init__(self, gitflow: Gitflow):
        self.gitflow = gitflow

    def visit(self, repo: Repository, **kwargs):
        def names(branches: IterableList):
            return [b.name for b in branches]

        return {
            "references": {
                "master": names(branches=repo.branches(folder=self.gitflow.master)),
                "develop": names(branches=repo.branches(folder=self.gitflow.develop)),
                "features": names(branches=repo.branches(folder=self.gitflow.features)),
                "fixes": names(branches=repo.branches(folder=self.gitflow.fixes)),
                "releases": names(branches=repo.branches(folder=self.gitflow.releases)),
                "hotfixes": names(branches=repo.branches(folder=self.gitflow.hotfixes)),
            },
            "counts": {
                "master": len(repo.branches(folder=self.gitflow.master)),
                "develop": len(repo.branches(folder=self.gitflow.develop)),
                "features": len(repo.branches(folder=self.gitflow.features)),
                "fixes": len(repo.branches(folder=self.gitflow.fixes)),
                "releases": len(repo.branches(folder=self.gitflow.releases)),
                "hotfixes": len(repo.branches(folder=self.gitflow.hotfixes)),
            }
        }


class SingleBranchesVisitor(BaseVisitor):
    __doc__ = """gitflow strongly relies on the fact that there is (1) only one branch for keeping the release history 
    and (2) only one integration branch """

    @property
    def rule(self) -> str:
        return 'single_master_and_develop'

    def visit(self, repo: Repository, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if repo contains single release history branch and single '
                                                'integration branch')
        # TODO add smarter checking
        if len(repo.branches(folder=self.gitflow.master)) > 1:
            section.append(Issue.error('Repository contains more than one master branch'))
        if len(repo.branches(folder=self.gitflow.develop)) > 1:
            section.append(Issue.error('Repository contains more than one develop branch'))

        return section


class OldDevelopmentBranchesVisitor(BaseVisitor):
    __doc__ = """having old feature or bugfix branches may create a mess in the repository
    
    use ``max_days_features`` option to configure what 'old' means for you"""

    @property
    def rule(self) -> str:
        return 'no_old_development_branches'

    @arguments_checker(['max_days_features'])
    def visit(self, repo: Repository, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if repo contains abandoned feature branches')
        deadline = datetime.now() - timedelta(days=kwargs['max_days_features'])
        merged_branches = repo.raw_query(lambda git: git.branch('-r', '--merged', self.gitflow.develop))

        def _check_for_issues(branches: IterableList, name: str):
            for branch in branches:
                if deadline > branch.commit.committed_datetime.replace(tzinfo=None) \
                        and branch.name not in merged_branches:
                    description = '{} {} has not been touched since {}'.format(name, branch.name, branch.commit.committed_datetime)
                    section.append(Issue.error(description, obj=branch))

        _check_for_issues(branches=repo.branches(folder=self.gitflow.features), name='Feature')
        _check_for_issues(branches=repo.branches(folder=self.gitflow.fixes), name='Fix')

        return section


class NotScopedBranchesVisitor(BaseVisitor):
    __doc__ = """having branches that are out of configured folders (eg. created out of feature/, bugfix/) may be an 
    indicator that you do something wrong and create a mess in the repo"""

    @property
    def rule(self) -> str:
        return 'no_orphan_branches'

    def visit(self, repo: Repository, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if repo contains orphan branches (created out of expected '
                                                'folders)')
        expected_prefix_template = '{remote}/{branch}'
        expected_prefixes = [
                                expected_prefix_template.format(remote=repo.remote.name, branch='HEAD'),
                                expected_prefix_template.format(remote=repo.remote.name,
                                                                branch=self.gitflow.master),
                                expected_prefix_template.format(remote=repo.remote.name,
                                                                branch=self.gitflow.develop),
                                expected_prefix_template.format(remote=repo.remote.name,
                                                                branch=self.gitflow.features),
                                expected_prefix_template.format(remote=repo.remote.name,
                                                                branch=self.gitflow.fixes),
                                expected_prefix_template.format(remote=repo.remote.name,
                                                                branch=self.gitflow.hotfixes),
                                expected_prefix_template.format(remote=repo.remote.name,
                                                                branch=self.gitflow.releases),
                            ] + [expected_prefix_template.format(remote=repo.remote.name, branch=branch.strip())
                                 for branch in self.gitflow.others]

        def has_expected_prefix(branch: Head) -> bool:
            for prefix in expected_prefixes:
                if branch.name.startswith(prefix):
                    return True
            return False

        orphan_branches = [branch for branch in repo.branches() if not has_expected_prefix(branch=branch)]
        for branch in orphan_branches:
            section.append(Issue.error('{branch} looks like created out of expected scopes'.format(branch=branch.name), obj=branch))

        return section


class MainCommitsAreTaggedVisitor(BaseVisitor):
    __doc__ = """if your master branch contains commits that are not tagged, it probably means that you don't use 
    master as your releases history keeper"""

    @property
    def rule(self) -> str:
        return 'master_must_have_tags'

    def visit(self, repo: Repository, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if main repo branch has tagged commits')
        main_branch = '/'.join([repo.remote.name, self.gitflow.master])
        main_commits = repo.raw_query(
            lambda git: git.log(main_branch, '--merges', '--format=format:%H', '--first-parent'),
            predicate=lambda sha: sha)
        tags = repo.repo.tags
        tags_sha = [tag.commit.hexsha for tag in tags]
        tags_not_on_main_branch = [sha for sha in tags_sha if sha not in main_commits]
        main_commits_not_tagged = [commit for commit in main_commits if commit not in tags_sha]

        for main_commit_not_tagged in main_commits_not_tagged:
            object = next(iter([tag for tag in tags if tag.commit.hexsha.startswith(main_commit_not_tagged)]))
            section.append(Issue.error('{commit} commit in main branch is not tagged'
                                       .format(commit=main_commit_not_tagged[:8]), obj=object))

        for tag_not_on_main in tags_not_on_main_branch:
            section.append(Issue.warning('{commit} commit contains a tag but is not a part of the master branch'
                                         .format(commit=tag_not_on_main[:8])))

        return section


class NoDirectCommitsToProtectedBranches(BaseVisitor):
    """
    the purposes behind develop and master are different but there is an assumption that at least those two are protected

    the rule is here to check if it is really the case and both branches does not contain direct commits (commits
    that were pushed directly)
    """

    @property
    def rule(self) -> str:
        return 'no_direct_commits_to_protected_branches'

    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if {} and {} contain only merges without direct commits'
                          .format(self.gitflow.develop, self.gitflow.master))
        initial_commit = next(iter(repo.raw_query(lambda git: git.log('--format=format:%s', '--reverse'))))

        def _get_direct_commits(branch: str) -> List[str]:
            merges = repo.raw_query(
                lambda git: git.log(branch, '--merges', '--format=format:%H', '--first-parent'),
                predicate=lambda sha: sha)
            potential_fast_forwards = repo.raw_query(
                lambda git: git.reflog('show', branch, '--format=format:%H'),
                predicate=lambda sha: sha)
            all_commits = repo.raw_query(
                lambda git: git.log(branch, '--format=format:%H', '--first-parent'),
                predicate=lambda sha: sha)
            return [sha for sha in all_commits if sha not in merges and sha not in potential_fast_forwards]

        def _get_issues(direct_commits: List[str], branch: str) -> List[Issue]:
            issuers = [repo.commit(sha, branch) for sha in direct_commits]
            issue_msg_fmt = 'Branch {} contains commit "{}" that was pushed directly rather than merged'
            return [
                Issue.error(issue_msg_fmt.format(branch, ' '.join([str(commit.hexsha)[:8], commit.summary.strip()])), obj=commit)
                for commit in issuers if commit and commit.message.lower().strip() != initial_commit.lower().strip()
            ]
        
        dev_branch = '/'.join([repo.remote.name, self.gitflow.develop])
        main_branch = '/'.join([repo.remote.name, self.gitflow.master])

        develop_results = _get_direct_commits(dev_branch)
        master_results = _get_direct_commits(main_branch)
        section.extend(_get_issues(direct_commits=develop_results, branch=dev_branch))
        section.extend(_get_issues(direct_commits=master_results, branch=main_branch))
        return section


class VersionNamesConventionVisitor(BaseVisitor):
    __doc__ = """checks if release branches and tags follow version naming convention
    
    the convention must be specified in ``version_regex`` argument as a regular expression string"""

    @property
    def rule(self) -> str:
        return 'version_names_follow_convention'

    @arguments_checker(['version_regex'])
    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        import re
        section = Section(rule=self.rule, title='Checked if version names follow given convention')
        releases = [branch for branch in repo.branches(self.gitflow.releases)]
        tags = [tag for tag in repo.repo.tags]
        version_reg = kwargs['version_regex']

        def _validate_version(v: str) -> bool:
            return re.search(version_reg, v) is not None

        release_issues = [release for release in releases if not _validate_version(release.name.split('/')[-1])]
        tags_issues = [tag for tag in tags if not _validate_version(tag.name)]

        section.extend(
            [Issue.error('Release {branch} does not follow name convention'.format(branch=release.name), obj=release) for release in
             release_issues])
        section.extend(
            [Issue.error('Tag {tag} does not follow name convention'.format(tag=tag.name), obj=tag) for tag in tags_issues])

        return section


class DevBranchNamesFollowConvention(BaseVisitor):
    """
    sometimes you may wish to have feature and bugfix branch names containing eg. ticket numbers

    the given convention is checked by providing ``name_regex`` as an argument

    if you want to provide different conventions for features and bugfixes, use ``feature_name_regex`` and ``bugfix_name_regex`` respectively
    """

    @property
    def rule(self) -> str:
        return 'dev_branch_names_follow_convention'

    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        import re
        features_regex = kwargs.get('name_regex', None) if not kwargs.get('feature_name_regex', None) else kwargs.get(
            'feature_name_regex')
        bugfixes_regex = kwargs.get('name_regex', None) if not kwargs.get('bugfix_name_regex', None) else kwargs.get(
            'bugfix_name_regex')
        if not features_regex or not bugfixes_regex:
            raise Exception('Configuration of the rule is invalid: desired convention is not provided')

        feature_prefix = '/'.join([repo.remote.name, self.gitflow.features, ''])
        bugfix_prefix = '/'.join([repo.remote.name, self.gitflow.fixes, ''])

        def _is_valid(branch: str, regex: str) -> bool:
            return re.search(regex, branch) is not None

        feature_issuers = [feature for feature in repo.branches(self.gitflow.features) if
                           not _is_valid(branch=feature.name.replace(feature_prefix, ''), regex=features_regex)]
        bugfix_issuers = [bugfix for bugfix in repo.branches(self.gitflow.fixes) if
                          not _is_valid(branch=bugfix.name.replace(bugfix_prefix, ''), regex=bugfixes_regex)]

        issue_msg_fmt = '{branch} branch does not follow given convention'
        issues = [Issue.error(issue_msg_fmt.format(branch=branch.name), obj=branch) for branch in (feature_issuers + bugfix_issuers)]

        return Section(rule=self.rule, title='Checked if feature and bugfix names follow convention', issues=issues)


class DeadReleasesVisitor(BaseVisitor):
    __doc__ = """release branches that are not closed may create a mess in the repository and breaks the master/main 
    branch - releases must be closed as soon as they are deployed to production environment (or just before, 
    depending on your case)
    
    since hotfixes are in fact releases started from master instead of develop, the rule will be checked against them as well
    
    configure how long releases are supposed to be maintained by using ``deadline_to_close_release`` (number of days)"""

    @property
    def rule(self) -> str:
        return 'no_dead_releases'

    @arguments_checker(['deadline_to_close_release'])
    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if repo contains abandoned and not removed releases')
        deadline = datetime.now() - timedelta(days=kwargs['deadline_to_close_release'])
        main_branch = '/'.join([repo.remote.name, self.gitflow.master])
        dev_branch = '/'.join([repo.remote.name, self.gitflow.develop])
        release_branch = '/'.join([repo.remote.name, self.gitflow.releases, ''])
        hotfix_branch = '/'.format([repo.remote.name, self.gitflow.hotfixes, ''])

        releases_not_merged_to_main = repo.raw_query(lambda git: git.branch('-r', '--no-merged', main_branch),
                                                 predicate=lambda release: release.strip().startswith(
                                                     release_branch) or release.strip().startswith(
                                                     hotfix_branch),
                                                 map_line=lambda release: repo.branch(release))
        releases_not_merged_to_develop = repo.raw_query(lambda git: git.branch('-r', '--no-merged', dev_branch),
                                                 predicate=lambda release: release.strip().startswith(
                                                     release_branch) or release.strip().startswith(
                                                     hotfix_branch),
                                                 map_line=lambda release: repo.branch(release))

        potential_dead_releases = [release for release in releases_not_merged_to_main if release in releases_not_merged_to_develop]
        
        releases_merged_only_into_develop = [release for release in releases_not_merged_to_main if release not in releases_not_merged_to_develop]

        dead_releases = [dead_release for dead_release in potential_dead_releases if
                         deadline > dead_release.commit.committed_datetime.replace(tzinfo=None)]

        suspicious_releases = [suspicious_release for suspicious_release in releases_merged_only_into_develop 
                            if deadline > suspicious_release.commit.committed_datetime.replace(tzinfo=None)]

        section.extend([
            Issue.error('{release} seems abandoned - it has never been merged into the {master} branch'.format(release=r.name, master=self.gitflow.master), obj=r) 
            for r in dead_releases
        ])

        section.extend([
            Issue.warning(description='{release} has been merged back into {develop} but never into {master}'.format(release=r.name, develop=self.gitflow.develop, master=self.gitflow.master), obj=r)
            for r in suspicious_releases
        ])

        return section


class DependantFeaturesVisitor(BaseVisitor):
    __doc__ = """creating feature/bugfix branches one from another or merging them together before merging to develop 
    may result in ugly issues during code review and merge mistakes 
    
    creating such a feature/merge is sometimes inevitable, you must configure the limit of such branches by using 
    ``max_dependant_branches`` option """

    @property
    def rule(self) -> str:
        return 'no_dependant_features'

    @arguments_checker(['max_dependant_branches'])
    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if repo contains dependant feature branches')
        dev_branch = '/'.join([repo.remote.name, self.gitflow.develop])
        max_dependant_branches = int(kwargs['max_dependant_branches'])
        merged_branches = repo.raw_query(lambda git: git.branch('-r', '--merged', self.gitflow.develop))
        not_merged = [repo.branch(b.name) for b in repo.branches(self.gitflow.features) if b.name not in merged_branches] + [repo.branch(b.name) for b in repo.branches(self.gitflow.fixes) if b.name not in merged_branches]
        branch_issue_format = '{} seems to depend on other feature branches. It contains following merges: {}'
        problematic_branch_sep = os.linesep + '\t\t\t- '

        for feature in not_merged:
            name = feature.name
            merge_commits_query = repo.raw_query(lambda git: git.log('..'.join([dev_branch, name]), '--merges',
                                                                     '--first-parent', '--format=format:%H'))
            merge_commits_sha = [commit_sha.strip() for commit_sha in merge_commits_query]
            merge_commits_in_feature = [commit for commit in repo.repo.iter_commits(name, max_count=200) if
                                        commit.hexsha in merge_commits_sha]
            branch_issues = [commit for commit in merge_commits_in_feature if
                             self.gitflow.develop not in commit.message]

            if branch_issues:
                is_limit_exceeded = len(branch_issues) > max_dependant_branches
                issue_level = Level.ERROR if is_limit_exceeded else Level.WARNING
                issues_titles = [next(iter(commit.message.split(os.linesep)), None) for commit in branch_issues]
                issue_desc = branch_issue_format.format(name, problematic_branch_sep + problematic_branch_sep.join(issues_titles))
                section.append(Issue(level=issue_level, description=issue_desc, obj=feature))

        # chained features or features that share commits
        commits_in_ft_branches = dict()
        issues_in_ft_branch = dict()
        branch_issue_format = '{} seems to depend on other feature branches. It shares commits with following branches: {}'
        for feature in not_merged:
            commit_hashes = repo.raw_query(lambda git: git.rev_list('--left-right','..'.join([dev_branch, feature.name])))
            commits_in_ft_branches[feature] = commit_hashes

        for feature in commits_in_ft_branches.keys():
            other_dependant_ft_branches = [
                ft for ft in commits_in_ft_branches.keys() 
                if ft != feature and any(hash_c in commits_in_ft_branches[feature] for hash_c in commits_in_ft_branches[ft])
            ]
            if other_dependant_ft_branches:
                issues_in_ft_branch[feature] = other_dependant_ft_branches
        
        for feature in issues_in_ft_branch.keys():
            is_limit_exceeded = len(issues_in_ft_branch[feature]) > max_dependant_branches
            issue_level = Level.ERROR if is_limit_exceeded else Level.WARNING
            problematic_branches_names = [b.name for b in issues_in_ft_branch[feature]]
            dependant_branches = problematic_branch_sep + problematic_branch_sep.join(problematic_branches_names)
            issue_desc = branch_issue_format.format(feature.name, dependant_branches)
            section.append(Issue(level=issue_level, description=issue_desc, obj=feature))

        return section


def visitors(gitflow: Gitflow) -> List[BaseVisitor]:
    return [
        SingleBranchesVisitor(gitflow=gitflow),
        OldDevelopmentBranchesVisitor(gitflow=gitflow),
        NotScopedBranchesVisitor(gitflow=gitflow),
        MainCommitsAreTaggedVisitor(gitflow=gitflow),
        NoDirectCommitsToProtectedBranches(gitflow=gitflow),
        VersionNamesConventionVisitor(gitflow=gitflow),
        DevBranchNamesFollowConvention(gitflow=gitflow),
        DeadReleasesVisitor(gitflow=gitflow),
        DependantFeaturesVisitor(gitflow=gitflow),
    ]
