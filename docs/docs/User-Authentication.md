---
id: User-Authentication
title: User Authentication
---
## How it works

User Authentication is [JSON Web Token (JWT)](https://jwt.io) based. To implement this we use a flask extension, flask-jwt-extended. You can see an example of [basic usage with this extension here](https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage.html).

In short, when a user logs in, the user will receive an authentication token (e.g.: `access_token`) which contains part of the user's identity and other token related fields, as the expiration date.

You can get an access token once you are registered into the backend. Here's a quick tutorial on [how to login using Swagger UI](Log-in-using-Swagger-UI) provided by the deployed server.

The user can then use this `access_token` when using a protected/restricted API, such as, `GET /user` API. To access this the client has to send the `access_token` in the header of the HTTP request, following this format: "Autorization: Bearer `access_token`".

## Example

Here's an inside look at an `access_token` using [jwt.io](https://jwt.io) Debugger.
![image](https://user-images.githubusercontent.com/11148726/44627573-1de2f800-a928-11e8-87a7-0107b0a622bc.png)
