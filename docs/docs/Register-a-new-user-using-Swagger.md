---
id: Register-a-new-user-using-Swagger
title: Register a new user using Swagger
---
This page will show how to register a new user into Mentorship System and verify the email using Swagger UI and a temporary email creation service provider.

1. Go to the Backend public API page (you can find the most recent URL on README). You'll see a Swagger UI. Click on POST /register from User API.

![Swagger UI that shows post method to register a new user](https://user-images.githubusercontent.com/11148726/50458627-68b75f80-095c-11e9-92c6-27977f64d4e3.png)

2. Create a temporary email to create the new user, so that you can create multiple users without ever using your personal email.

For this, I tend to use https://temp-mail.org/ service. This will allow you to use an arbitrary email and verify the email to be able to login in the app and use protected APIs.

![temporary email website](https://user-images.githubusercontent.com/11148726/50458672-c51a7f00-095c-11e9-9ea8-179259ff197d.png)

3. Copy the email you see in the website.

![random email on temp email service provider](https://user-images.githubusercontent.com/11148726/50458746-77524680-095d-11e9-9ce2-cb615b09595e.png)

4. Register the new user using POST /register from User API. Here you can fill the user data however you want as long the username and the email is unique in the system.

![filling post data for registering a user  into the system](https://user-images.githubusercontent.com/11148726/50458719-3823f580-095d-11e9-9a00-9c14ebedf517.png)

5. Check for new emails on the temporary email inbox.

![Temporary Email inbox](https://user-images.githubusercontent.com/11148726/50458746-77524680-095d-11e9-9ce2-cb615b09595e.png)

6. Open the email and click the link provided in the email body.

![Email from Systers OS on Temporary Email inbox](https://user-images.githubusercontent.com/11148726/50458758-8c2eda00-095d-11e9-835a-49f7633a45e8.png)

7. By clicking the above link, you'll be forwarded to this page which shold confirm you successfully confirmed your email.

![Email confirmation response](https://user-images.githubusercontent.com/11148726/50458775-a49ef480-095d-11e9-9e48-b10160f74b05.png)