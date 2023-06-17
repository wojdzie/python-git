# PyGit - simple version control system implemented in Python

## How to use PyGit?

### Initialization

![img.png](images/init_screenshot.png)

To initialize a new repository, use the following command:
```bash
pygit init
```

### Adding Files

![img.png](images/add_screenshot.png)

To add files to the staging area, use the following command:
```bash
pygit add <file1> <file2>
```
Replace `<file1>`, `<file2>`, etc. with the paths to the files you want to add.

### Committing Changes

![img.png](images/commit_screenshot.png)

To commit the changes in the staging area, use the following command:
```bash
pygit commit
```
This will create a new commit with the changes in the staging area.

### Switching Branches

![img.png](images/checkout_screenshot.png)

To switch to a different branch, use the following command:
```bash
pygit checkout <branch-name>
```
Replace `<branch-name>` with the name of the branch you want to switch to.

### Viewing Commit History

![img.png](images/log_screenshot.png)

To view the commit history, use the following command:
```bash
pygit log
```
This will display a list of commits with their respective details.