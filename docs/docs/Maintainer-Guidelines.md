---
id: Maintainer-Guidelines
title: Maintainer Guidelines
---
# Guidelines

Make sure contributors are respecting the [Contribution Guidelines](https://github.com/anitab-org/mentorship-backend/blob/develop/.github/CONTRIBUTING.md).
If they don't let them know about it: what is missing, what was disrespected?

## Code Review

* When possible get a second opinion before merging.
* Make sure the PR has a link to the issue.
* If you can, let them know why your change request makes sense.
* (nice to have) If you have time, thank them for contributing to the project.
* **Make sure that, if the PR changes actual code, to properly test it or wait for someone to confirm the behavior**

## Merging PRs

**TL;DR:**
1. Select "Squash and Merge".
2. Edit commit if necessary to follow our [style guide](Commit-Message-Style-Guide) and leave the PR id in the message.

**Long version:**

About merging pull requests (PRs), to keep the project commit history clean, it's important to have all commits from a PR to be squashed when merging. For this you may have to select "Squash and Merge" option:

![Squash and Merge option on GitHub](https://user-images.githubusercontent.com/11148726/76369025-06146e80-632a-11ea-922a-c28073539125.png)

If the commit does not follow our [Commit Message Style Guide](Commit-Message-Style-Guide), make sure to ask the contributor to fix it **or** you can fix it when merging.

![Editing commit when merging](https://user-images.githubusercontent.com/11148726/76369362-33155100-632b-11ea-90d1-879dbecfb059.png)

Make sure to always leave the PR identifier, so that we can traceback a commit to a specific PR.