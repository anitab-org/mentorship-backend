<h1>Steps to test a PR</h1>

1. Follow instructions in 

[README](https://github.com/anitab-org/mentorship-backend/blob/develop/README.md) to setup the system running locally.

2. Check on Zulip chat if any of the PR's 
[here](https://github.com/anitab-org/mentorship-backend/labels/Needs%20Testing) are high-priority if the priority is not set already.

3. If the PRs are not prioritized then pick any 1 PR from the list from the link in step 2 to test locally.

4. Go to the Issue that PR is fixing and follow the steps to reproduce that issue while you are under the develop branch.

5. Run the following commands to get to the PR branch, where `<contributor>` is the GitHub username of the contributor that submitted the PR:

git checkout -b <contributor>-<branch-name> develop
  
git pull https://github.com/<contributor>/mentorship-backend/ <branch-name>

6. Verify the code addition/deletions in the PR.

7. Reproduce the issue and test the fix.

8. Get screenshots/gifs of before and after the fix and attach them to the PR comment.

<h1>Steps to test multiple features (User Registration, List users, ...) of the Mentorship System.</h1>

<h2>Registering users</h2>
Register 3 users. Follow instructions in

[this demo on Youtube](https://www.youtube.com/watch?v=xRZrdR47R-w&feature=youtu.be&t=672) to register users. The users used here are 

* testusera
* testuserb
* testuserc

![Register user screenshot](https://user-images.githubusercontent.com/26095715/79673508-4a582180-81a8-11ea-87ce-fe0bfda82fea.png)

<h2>Login as the users and capture the access tokens</h2>

Steps to login and capture the token are shown in 

[this video](https://www.youtube.com/watch?v=xRZrdR47R-w&feature=youtu.be&t=672)

![Login user screenshot](https://user-images.githubusercontent.com/26095715/79673507-4a582180-81a8-11ea-96ff-2268733e9673.png)

<h2>Get the user ID's of the users</h2>

In this example they are:

* testusera - ID: 120
* testuserb - ID: 121
* testuserc - ID: 122

![User ID screenshot1](https://user-images.githubusercontent.com/26095715/79673506-49bf8b00-81a8-11ea-8bf3-0dffd8b269f5.png)

![User ID screenshot2](https://user-images.githubusercontent.com/26095715/79673505-49bf8b00-81a8-11ea-89f2-687913a238fe.png)

<h2>Create a mentorship relation between 2 users</h2>
<h3>Send a mentorship request</h3>

In this example testusera is the mentee and testuserb is the mentor and testusera is sending the request. The steps to do this is explained in this video.

[Demo Video](https://www.youtube.com/watch?v=xRZrdR47R-w&feature=youtu.be&t=672)

![Mentorship Request screenshot1](https://user-images.githubusercontent.com/26095715/79673504-49bf8b00-81a8-11ea-9a1e-c136cb345440.png)

<h3>Check pending requests</h3>

Check pending requests for testusera. The relation should be in state 1 (pending). Note the request ID. Here it is 13.

![Pending request testusera screenshot1](https://user-images.githubusercontent.com/26095715/79673502-4926f480-81a8-11ea-8695-882117830657.png)

![Pending request testusera screenshot2](https://user-images.githubusercontent.com/26095715/79673501-4926f480-81a8-11ea-9d78-25704487ce28.png)

<h3>Accept the mentorship request</h3>

testuserb accepts the mentorship request from testusera.

![Accepted request screenshot](https://user-images.githubusercontent.com/26095715/79673500-4926f480-81a8-11ea-9c97-bac8cc800f85.png)

<h3>List current relations of a user</h3>

List the current relationships of testusera. The relation should be state 2 (accepted).

![Current relations screenshot](https://user-images.githubusercontent.com/26095715/79673499-4926f480-81a8-11ea-8641-79749fdc89ab.png)

<h2>Create a task under a relation.</h2>

Testusera creates a task for the relation 13. This will be successful because testusera is a part of this relation.

![Create task screenshot](https://user-images.githubusercontent.com/26095715/79673498-4926f480-81a8-11ea-8e95-a7cd3ea24e56.png)

Testuserc cannot create a task under this relation

![Invalid task screenshot](https://user-images.githubusercontent.com/11148726/79637378-16b0d380-8177-11ea-96ef-202c17908e5c.png)
