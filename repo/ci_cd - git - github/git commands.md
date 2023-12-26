# git commands
https://www.atlassian.com/git/glossary#commands

## basics

- `git status`        display the state of the current repo and the staging area

- `git add`    adds the changes in the working directory to the staging area. It creates a staged snapshot of the project.
    - `git add <file>` add a specific file to the staging areas
    - `git add .` adds the changes from the entire directory         

- `git commit -m "your commit message here"`        equivalent of a traditional "save" of a collection of files and directory
    - commit messages should be as descriptive and concise as possible. writing commit messages is a little bit of an art form.

- `git commit -a -m "your commit message here"` adds all and commit at once

- `git push` push the changes to the remote repository. 
- `git pull` pull the changes from the remote repository. 
 - Your local repository needs to be cleaned first. Eeverything needs to be commited or, alternatively, stashed (see `git stash`)

- `git checkout <branchename>` switches to <branchename> 
    - `git checkout -b <branchname>` creates and switches to <branchename>, based on the current HEAD
    - `git checkout -b <branchname> <basebranch>` creates <branchname> based on <basebranch>
    - https://www.atlassian.com/git/tutorials/using-branches/git-checkout

- `git fetch --all` fetching all the remote branches on your local repository


## (more) advanced 
### `git stash`
read: https://www.atlassian.com/git/tutorials/saving-changes/git-stash

- `git stash` temporarily shelves changes made that are not ready to be commited 
- `git stash list` gives the list of the stashes - you can have several at the same time.
- **recommmended usage**: `git stash save "message"` to know what's in each stash. 
- `git stash pop` reapply the stashed changes
- `git stash -u` also stashes the untracked files. By default, `git stash` only stashes (1) staged changes or (2) changes to files currently tracked by git; not new files or ignored files
- `git stash branch <branchname> stash@{1}` - creates a new branch <branchname> from stash@{1}

### `git reset`
It is a complex and versatile tool. Please read: https://www.atlassian.com/git/tutorials/undoing-changes/git-reset

- `git reset` is used to undo a commit or staged snapshot
- default `git reset --mixed HEAD`; `HEAD` is the specific commit
- different levels/commands line arguments
    - `--soft`: 
    - `--mixed`: default behavior 
    - `--hard`: The Commit History ref pointers are updated to the specified commit
        - Staging Index and Working Directory are reset to match that of the specified commit

### `git rebase`
read:
- https://docs.github.com/en/get-started/using-git/about-git-rebase
- https://www.atlassian.com/git/tutorials/merging-vs-rebasing

### `git fetch --prune origin`
to prune remote-tracking branches for the origin remote (the default remote)

Remote-tracking branches are branches that track the state of branches on the remote repository (the repository that you have cloned from or pushed to). They have names like origin/master or origin/feature1. Remote-tracking branches can help you keep track of what is happening on the remote repository and synchronize your local branches with it.

However, sometimes remote-tracking branches may become stale or obsolete. This may happen when a branch on the remote repository is deleted or renamed, but your local repository still has a reference to it. Stale or obsolete remote-tracking branches can cause confusion and errors when you try to fetch, pull, or push from or to the remote repository.

To prune remote-tracking branches, you can use the git fetch command with the --prune option. This command will fetch the latest updates from the remote repository and delete any remote-tracking branches that no longer exist on the remote repository.


## resources
### git documentation
https://git-scm.com/
https://www.atlassian.com/git/tutorials/what-is-git

### github basics
https://docs.github.com/en/get-started/quickstart/hello-world

### git with VS code
https://code.visualstudio.com/docs/sourcecontrol/intro-to-git
https://learn.microsoft.com/en-us/visualstudio/version-control/?view=vs-2022

### pro Git
https://git-scm.com/book/en/v2