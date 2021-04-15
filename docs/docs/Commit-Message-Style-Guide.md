---
id: Commit-Message-Style-Guide
title: Commit Message Style Guide
---
## Commit Message Structure
A commit message should consist of two distinct parts separated by a blank line: the `title` and an optional `body`. The layout looks like this:

```
type: subject

body
```

### Title
The title should consist of the `type` of the change and `subject` separated by a colon `:`. Title should be no longer than 50 characters.

##### Type
The type is contained within the title and can be one of these types:
* **feat**: a new feature
* **fix**: a bug fix
* **docs**: changes to documentation
* **style**: formatting, missing semi colons, etc; no code change
* **refactor**: refactoring production code
* **test**: adding tests, refactoring test; no production code change
* **chore**: updating build tasks, package manager configs, etc; no production code change

##### Subject
Should begin with a capital letter and not end with a period.

Use an imperative tone to describe what a commit does, rather than what it did. For example, use change; not changed or changes.

### Body
If the changes made in a commit are complex, they should be explained in the commit body. Use the body to explain the what and why of a commit, not the how.

When writing a body, the blank line between the title and the body is required and you should limit the length of each line to no more than 72 characters.

##### Examples
Without body
```
docs: update screenshots in the documentation
```

or

With body
```
fix: fix crash caused by new libraries 

After merging PRs #126 and #130 crashes were occurring. 
These crashes were because of deprecated functions. 
Found a solution here (https://stackoverflow.com/questions/22718185) 
This will resolve issue #140
```