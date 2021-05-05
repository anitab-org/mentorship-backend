---
id: Log-in-using-Swagger-UI
title: Log in using Swagger UI
---
This page shows how to log in a user and then use the User token to access a restricted API.

1. Go to POST /login API under Users section and click "Try it out" button:

![First step](https://user-images.githubusercontent.com/11148726/44313082-dcb78900-a3f9-11e8-9f37-6af67d3356f1.png)

2. Use valid credentials in the request body. Valid credentials mean username/email and password from a user that has already been registered to the System and has its email verified. Then click the “Execute” button:

![Second step](https://user-images.githubusercontent.com/11148726/44312936-ce686d80-a3f7-11e8-9df3-17e073fd9fcf.png)

3. Copy the access token returned in the response (highlighted in blue).

![Third step](https://user-images.githubusercontent.com/11148726/44312940-df18e380-a3f7-11e8-9837-093c2c56ffdd.png)

4. Then use it in a restricted API, e.g.: GET /user to get the logged in user’s profile. Paste the access token as indicated in the Authorization field following this example: “Bearer <access_token>”.

![Fourth step](https://user-images.githubusercontent.com/11148726/44312943-eb9d3c00-a3f7-11e8-8b3c-4c24723f61bf.png)

5. Then hit the “Execute” button, and you’ll be able to receive a proper response.

![Fifth step](https://user-images.githubusercontent.com/11148726/44312951-ff48a280-a3f7-11e8-888e-3d6ed0372812.png)
