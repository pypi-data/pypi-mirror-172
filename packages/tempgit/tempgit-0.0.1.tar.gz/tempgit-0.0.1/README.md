# tempgit
Some temporal operations over git repositories using, mainly, ssh private keys and a git monitor
to detect changes in a repository.

* [Temporal git repository](#temporal-git-repository)
* [Git monitor](#git-monitor)

# Temporal git repository<a id="temporal-git-repository" name="temporal-git-repository"></a>

This is used to get a temporal git repository, for example, to clone it, modify and push the changes
without maintaining a local copy of the repository. The syntax is:

```python
from tempgit import TemporalGitRepository

# Using "with" command. The repository will be removed automatically after the "with" command finishes 
with TemporalGitRepository(repository, branch=branch, ssh_key=ssh_key) as repo:
    repo.add(...)
    repo.commit(...)
    repo.push()
```

For example:

```python
from tempgit import TemporalGitRepository

# Using "with" command. The repository will be removed automatically after the "with" command finishes 
with TemporalGitRepository(repository, branch=branch, ssh_key=ssh_key) as repo:
    repo.add(file1, file2, file3, ...)  # Add the modifications
    repo.commit('Message')  # Commit the changes
    repo.push()  # Push the commit

# With close(). The repository will be removed when you close the object.
repo = TemporalGitRepository(repository, branch=branch, ssh_key=ssh_key):
repo.add(file1, file2, file3, ...)
repo.commit('Message')
repo.push()
repo.close()
```

Yo can avoid the 

# Git monitor<a id="git-monitor" name="git-monitor"></a>

Monitor a Git repository to check if there is any change in the remote repository with respect the local one.

```python
from mysutils.git import GitMonitor

# Function to execute when the is a change
def func(*files: str) -> None:
  # Print the changed files
  print(files)

# Create a monitor instance to execute one only time  
monitor = GitMonitor(func, 'local_dir', 'remote_url', 'branch_name')
# Execute the monitor
monitor.monitor()
# Execute the monitor as a thread
monitor.start()

# If you want to check the git repository several times you need add an interval to
monitor = GitMonitor(func, 'local_dir', 'remote_url', 'branch_name', interval=30)  # 30 seconds
# If you want to execute func() the first time although the repository has not changed, use force
monitor = GitMonitor(func, 'local_dir', 'remote_url', 'branch_name', force=True, interval=30)
```