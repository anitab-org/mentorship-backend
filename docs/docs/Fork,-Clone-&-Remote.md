---
id: Fork,-Clone-&-Remote
title: Fork, Clone & Remote
---
## Fork

_**Note**: This is only needed if you want to contribute to the project._

If you want to contribute to the project you will have to create your own copy of the project on GitHub. You can do this by clicking the **Fork** button that can be found on the top right corner of the [landing page](https://github.com/anitab-org/mentorship-backend) of the repository.

![image showing fork symbol on GitHub](https://user-images.githubusercontent.com/17262180/44300717-53d11c80-a329-11e8-8782-5595a520446e.png)

## Clone 

_**Note**: For this you need to install [git](https://git-scm.com/) on your machine. You can download the git tool from [here](https://git-scm.com/downloads)._

 - If you have forked the project, run the following command - 

`git clone https://github.com/YOUR_GITHUB_USER_NAME/mentorship-backend`

where `YOUR_GITHUB_USER_NAME` is your GitHub handle.

 - If you haven't forked the project, run the following command - 

`git clone https://github.com/anitab-org/mentorship-backend`

## Remote

_**Note**: This is only needed if you want to contribute to the project._

When a repository is cloned, it has a default remote named `origin` that points to your fork on GitHub, not the original repository it was forked from. To keep track of the original repository, you should add another remote named upstream. For this project it can be done by running the following command - 

`git remote add upstream https://github.com/anitab-org/mentorship-backend`

You can check that the previous command worked by running `git remote -v`. You should see the following output:
```
$ git remote -v
origin  https://github.com/YOUR_GITHUB_USER_NAME/mentorship-backend (fetch)
origin  https://github.com/YOUR_GITHUB_USER_NAME/mentorship-backend (push)
upstream        https://github.com/anitab-org/mentorship-backend.git (fetch)
upstream        https://github.com/anitab-org/mentorship-backend.git (push)
```