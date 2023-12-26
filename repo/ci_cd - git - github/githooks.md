# Git Hooks
*- WORK IN PROGRESS -*

Through the use of a “hooks” system, git allows developers and administrators to extend functionality by specifying scripts that git will call based on different events and actions.

Git hooks are event-based. When you run certain git commands, the software will check the hooks directory within the git repository to see if there is an associated script to run.

# Scope of hooks
Hooks are local to any given Git repository, and they are not copied over to the new repository when you run git clone. And, since hooks are local, they can be altered by anybody with access to the repository.

This has an important impact when configuring hooks for a team of developers. First, you need to find a way to make sure hooks stay up-to-date amongst your team members. Second, you can’t force developers to create commits that look a certain way—you can only encourage them to do so.

Maintaining hooks for a team of developers can be a little tricky because the .git/hooks directory isn’t cloned with the rest of your project, nor is it under version control. A simple solution to both of these problems is to store your hooks in the actual project directory (above the .git directory). This lets you edit them like any other version-controlled file. To install the hook, you can either create a symlink to it in .git/hooks, or you can simply copy and paste it into the .git/hooks directory whenever the hook is updated.

## Creating shortcuts of the commited hooks
The `.git/hooks` folder is not committed, so every the hooks should be setup on every machine.
We should keep commited version of the githooks (in a separate, committed folder for each repo), and we can create a link from those in the .git/hook folder

```shell
ln -s <absolute_path>/enzyme_efficiency_prediction/.githooks/pre-commit <absolute_path>/python/enzyme_efficiency_prediction/.git/hooks/pre-commit
ln -s <absolute_path>/enzyme_efficiency_prediction/.githooks/post-commit <absolute_path>/python/enzyme_efficiency_prediction/.git/hooks/post-commit
```

The issue here could be that some elements depends on your local machine, and maybe it is better to copy-paste the content of the committed githooks. -> THIS NEEDS FURTHER CHECKs

## .git/hooks written in python
Make sure to enable a valid python environment for your machine. 
``` python
#!/Users/jean/opt/anaconda3/envs/pe/bin/python
from __future__ import with_statement, print_function
import os
import ...
...
```


# Server-side Hooks
These hooks are executed on servers that are used to receive pushes. Generally, that would be the main git repo for a project. \
- Pre-receive and post-receive: These are executed on the server receiving a push to do things like check for project conformance and to deploy after a push.
- Update: This is like a pre-receive, but operates on a branch-by-branch basis to execute code prior to each branch being accepted.


# Ressources


1 - https://www.atlassian.com/git/tutorials/git-hooks - 15 min

2 - https://www.youtube.com/watch?v=ObksvAZyWdo - 30 min tutorial

3 - https://pre-commit.com/ - hook package 

4 - https://www.digitalocean.com/community/tutorials/how-to-use-git-hooks-to-automate-development-and-deployment-tasks - advanced tutorial


# To Check / to do 
- global .git/hooks
- .gitconfig 
- copy paste instead of shortcut
- `ggshield` avoid commiting secrets

