## How it works

User Authentication is [JSON Web Token (JWT)](https://jwt.io) based. To implement this we use a flask extension, flask-jwt-extended. You can see an example of [basic usage with this extension here](https://flask-jwt-extended.readthedocs.io/en/latest/basic_usage.html).

In short, when a user logs in (`POST /login`), the user will receive an authentication token (e.g.: `access_token`) which contains part of the user's identity and other token related fields, as the expiration date. Expriry date comes as a [UNIX timestamp](https://www.unixtimestamp.com/) in the `access_expiry` attribute in the response.

You can get an access token once you are registered into the backend. Here's a quick tutorial on [how to login using Swagger UI](https://github.com/systers/mentorship-backend/wiki/Log-in-using-Swagger-UI) provided by the deployed server.

The user can then use this `access_token` when using a protected/restricted API, such as, `GET /user` API. To access this the client has to send the `access_token` in the header of the HTTP request, following this format: "Autorization: Bearer `access_token`".

## Example

Here's an inside look at an `access_token` using [jwt.io](https://jwt.io) Debugger.

![image](https://user-images.githubusercontent.com/11148726/44627573-1de2f800-a928-11e8-87a7-0107b0a622bc.png)

## Social Sign In

In addition to authenticating a user using username and password using the (`POST /login`) API, convenient social sign-in using Apple and Google sign-in is also there. This is done using the (`POST /apple/auth/callback`) and (`POST /google/auth/callback`) APIs.

All the three APIs return the same data model for a successful login, making the implementation in the client app simpler. The flow of social sign-in starts with the client app, where the user uses a provider (Apple or Google) to sign-in with. The provider authenticates the user on their end and sends a user unique `id_token`, `full_name`, and `email`. This data is then used in the callback APIs to authenticate the user on the Mentorship System backend.

To enable the social sign-in functionality, a separate social sign-in table has been created which links with the `users` table using the user id and stores the social sign-in data such as id_token, associated_email, etc. The functionality has been designed in a way where linking of different accounts can be enabled as a future scope.

The callback APIs work as follows:
1. The email of the user is used to find an existing user in the database.
2. If a user is not found for the email, a new user is created using the data. If a user with the unique `id_token` already exists on the system, an error message is returned. Else, tokens are generated and returned, successfully signing in the user.
3. If a user is found, the social sign-in details are verified for the user id and the exact provider (apple/google). If a social sign-in record is not found, an error is returned. Else, tokens are generated an returned, successfully signing in the user.

Official Developer Documentation:
[Sign In with Apple](https://developer.apple.com/sign-in-with-apple/get-started/)
[Sign In with Google](https://developers.google.com/identity/sign-in/ios/start?ver=swift)
