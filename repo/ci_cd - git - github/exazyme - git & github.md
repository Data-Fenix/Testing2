# Exazyme practices for CI/CD
**Continuous integration and continuous deployement with Github**
*- WORK IN PROGRESS -* 

# main / dev branches
We have a main <- dev <- feature branches design

## Main branch
Secured -> nobody can push directly to it 
Stable -> nothing that has not been extensively tested can be pushed there
Needs to be updated via `Pull Requests` only from the Dev branch. \
*- Frequency, strategy for PR from Dev to Main needs to be Defined -*

## Dev branch
Secured -> nobody can push directly to it. \
Beta version -> feature branches are pushed to it via `Pull Requests` and Code reviews. \
It is not "stable" because always changing in case of PR from feature branches. \

# Feature Branches
The feature branches are created for a **specific purpose** (as specific as it gets), used for that purpose and should ideally be deleted once merged with the dev branch. In some cases the branch can stay open if a multiple PR/merge strategy is adopted for a feature development (see the next section, on Pull Requests). \
Ideally it should be done as follows:
- **1.** make a new branch from dev for a new feature
- **2.** develop it and run unit tests
- **3.** make sure your local dev branch is up to date with origin/dev
- **4.** `git merge dev` into it or `git rebase dev` (to get the most recent updates) and solve the merge conflicts, if any. \
    - If something strange happens at this point, you can still delete your local branch, pull from origin and try again.
    - See https://www.atlassian.com/git/tutorials/merging-vs-rebasing \
        `git rebase ...` is prefered for clearer history and gives you the opportunity to clean the commit list but it sometimes fails. \
        `git merge ...` somehow works more reliably but it results in intertwined history.
    -  if the feature branch development takes a while, it might be worth to do this multiple time in case dev evolves a lot. Or alternatively, and more ideally, you can adopt a more frequent PR/merge strategy.
- **5.** run unit tests
- **6.** commit your changes
- **7.** pushing to origin might not work only with `git push`, especially after rebasing 
    - instead you can do `git push --force-with-lease origin <branch_name>`. 
    This should be safe and `--force-with-lease` checks that no-one else made some changes since you last pulled.
- **8.** pull request to dev 

# Pull requests. 

A pull request is a proposed code change or update submitted by a developer to a code repository. It allows for collaboration and code review before merging the changes into the main codebase.

Pull requests should be a **priority** - every feature development is intertwined with others, that is why quick updates of the repository is essential. 

A given `feature branch` should have a very defined purpose, achieved as quickly as possible. As soon as a feature branch is functional, a pull request to the `dev branch` should be open so other developers can review the changes, comment and make suggestions, which should then be implemented before merging. 

Once a pull request is accepted, merge conflicts, if any, should be resolved, and only then the `feature branch` should be mergeable with the `dev branch`. 

Most times the `feature branch` should be deleted, in order ot keep a clean repository.

# GitHub Actions
*- to write / to define -*

# Saving API keys
API keys or passwords should never be hardcoded in commited code.
*- to define -*

