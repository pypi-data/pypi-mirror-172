from typing import Union, Optional, Tuple, List, Callable

from mysutils.file import write_file
from mysutils.tmp import removable_tmp, RemovableTemp, Removable
from git import Repo
from git.types import Commit_ish
from git.util import Actor, RemoteProgress, IterableList
from git.objects import UpdateProgress
from git.objects import Commit
from os import PathLike
import os


class TemporalGitRepository(object):
    """ A simple class to create a local, temporal Git repository copy,
        modify it and push it very easily using a SSH key.
    """
    @property
    def repository_url(self) -> str:
        """ The Git repository URL. """
        return self._repository_url

    @property
    def repository(self) -> Repo:
        """ A GitPython Repo object that represents the Git repository."""
        return self._repository

    @property
    def repo_dir(self) -> str:
        """ The local copy directory of the Git repository."""
        return self._repo_dir.files[0]

    @property
    def branch(self) -> str:
        """ The branch of the Git repository to clone. """
        return self._branch

    def __init__(self,
                 repository: str,
                 repo_dir: Union[str, PathLike] = None,
                 branch: str = None,
                 ssh_key: str = None,
                 remove: bool = True) -> None:
        """  Create a temporal copy of a Git repository.

        :param repository: The url to the Git repository.
        :param repo_dir: The local path to the local copy. By default, it will create a temporal folder.
        :param branch: The branch to clone, if it is not given, the master or main branch is used.
        :param ssh_key: The SSH key value (not a file). By default, the process will use the system default SSH KEY.
        :param remove: If remove is False, then the temporal folder will not be removed automatically.
        """
        self._repo_dir = RemovableTemp(True) if repo_dir is None else Removable(repo_dir)
        self._branch = branch
        self._remove = remove
        self._repository_url = repository
        self._repository = self.clone(self.repo_dir, branch, ssh_key)

    def clone(self, repo_dir: Union[str, PathLike], branch: str = None, ssh_key: str = None) -> Repo:
        """ Clone the repository into a local directory using, optionally a SSH key.

        :param repo_dir: The local reopository directory.
        :param branch: The branch to clone, if it is not given, the master or main branch is used.
        :param ssh_key: The SSH key value (not a file). By default, the process will use the system default SSH KEY.
        :return: The git repository.
        """
        kwargs = {'branch': branch} if branch else {}
        with removable_tmp() as key_file:
            if ssh_key is not None:
                descriptor = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
                write_file(descriptor, ssh_key)
                kwargs['env'] = {'GIT_SSH_COMMAND': f'ssh -i {key_file} -o StrictHostKeyChecking=no'}
            try:
                return Repo.clone_from(self._repository_url, repo_dir, **kwargs)
            except Exception as e:
                self.close()
                raise e

    def add(self, *files: Union[str, PathLike, bytes]) -> Union[str, bytes, Tuple[int, Union[str, bytes], str]]:
        """ Add files to a commit.

        :param files: The files to commit.
        """
        return self._repository.git.add(*files)

    def commit(self,
               message: str,
               parent_commits: Union[Commit_ish, None] = None,
               head: bool = True,
               author: Union[None, Actor] = None,
               committer: Union[None, Actor] = None,
               author_date: Optional[str] = None,
               commit_date: Optional[str] = None,
               skip_hooks: bool = False) -> Commit:
        """ Commit the current default index file, creating a commit object.
            For more information on the arguments, see Commit.create_from_tree().

        :note: If you have manually altered the .entries member of this instance,
               don't forget to write() your changes to disk beforehand.
               Passing skip_hooks=True is the equivalent of using `-n`
               or `--no-verify` on the command line.
        :return: Commit object representing the new commit
        """
        return self._repository.index.commit(message, parent_commits, head, author, committer, author_date,
                                             commit_date, skip_hooks)

    def push(self,
             refspec: Union[str, List[str], None] = None,
             progress: Union[RemoteProgress, UpdateProgress, Callable, None] = None,
             kill_after_timeout: Union[None, float] = None,
             **kwargs) -> IterableList:
        """ Push changes from source branch in refspec to target branch in refspec.

        :param refspec: see ‘fetch’ method
        :param progress: Can take one of many value types:
            * None to discard progress information
            * A function (callable) that is called with the progress information.
              Signature: progress(op_code, cur_count, max_count=None, message='').
              Click here for a description of all arguments given to the function.
            * An instance of a class derived from git.RemoteProgress that overrides the update() function.

        :param kill_after_timeout: To specify a timeout in seconds for the git command,
            after which the process should be killed. It is set to None by default.
        :param kwargs: Additional arguments to be passed to git-push.
        :note: No further progress information is returned after push returns.
        :return: list(PushInfo, …) list of PushInfo instances, each one informing about an individual head which had
            been updated on the remote side. If the push contains rejected heads, these will have the PushInfo.ERROR
            bit set in their flags.
            If the operation fails completely, the length of the returned IterableList will be 0.
        """
        return self._repository.git.push(refspec, progress, kill_after_timeout, **kwargs)

    def has_changes(self) -> bool:
        """ Check whether the local repository has any changes or not."""
        return bool(self._repository.head.commit.diff())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """ Close the local repository and if the attribute remote is set to True (by defalt), then remove it. """
        if self._remove:
            self._repo_dir.close()
