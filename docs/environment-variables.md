# Environment Variables

To run the backend you need to export environment variables.

These are the needed environment variables:
```
export FLASK_ENVIRONMENT_CONFIG=<dev-or-test-or-prod-or-local>
export SECRET_KEY=<your-secret-key>
export SECURITY_PASSWORD_SALT=<your-security-password-salt>
export MAIL_DEFAULT_SENDER=<mail-default-sender>
export MAIL_SERVER=<mail-server>
export APP_MAIL_USERNAME=<app-mail-username>
export APP_MAIL_PASSWORD=<app-mail-password>
```

## Environment Variables Description

### Run Configuration

| Environment Variable     | Description                                                                                                                                                                                                                    | Example |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|

| FLASK_ENVIRONMENT_CONFIG | Short running environment name so that Flask know which configuration to load. Currently, there are 4 options for this: `dev`, `test`, `local` and `prod`.  If you want to use a simple local database (e.g.: sqlite) then set your environment config value as `local`. To use the development environment with a remote database configuration you should use `dev` as a value.  | local     |


These are the currently available run configurations:
- **local:** Local environment used when developing locally
- **dev:** Development environment used when developing with a remote database configuration
- **test:** Testing environment used when running tests
- **prod:** Production environment used when a server is deployed

### Security

| Environment Variable   | Description                                                                                                                                                                                                                                       | Example              |
|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|
| SECRET_KEY             | Variable used to encrypt or hash sensitive data.  JWT based authentication uses this variable to calculate the hash of the access token. Its also used to calculate the password hash to avoid saving it in plain text. This is in string format. | 'some random key'    |
| SECURITY_PASSWORD_SALT | Variable used for email confirmation token generation. This is in string format.                                                                                                                                                    | 'some password salt' |

### Email Verification

Email verification is when a user registers into the application and to be able to login, this user has to verify/confirm its email. To do this the user has to go to its emails and click the link from the mail sent by our application email.

| Environment Variable | Description                                                                                                     | Example                |
|----------------------|-----------------------------------------------------------------------------------------------------------------|------------------------|
| MAIL_DEFAULT_SENDER  | Email used to send email verification emails. This is in string format.                                         | 'some_username@gmail.com' |
| MAIL_SERVER          | SMTP server address/name used by the email account that sends the verification emails. This is in string format. | 'smtp.gmail.com'       |
| APP_MAIL_USERNAME    | Username of the email account used to send verification emails. This is in string format.                       | 'some_username'        |
| APP_MAIL_PASSWORD    | Password of the email account used to send verification emails. This is in string format.                       | 'some_password'        |

_Note:_
- In the examples we use Gmail account example, but you are not restricted to use a Gmail account to send the verification email. If you use other email providers make sure to research about the correct SMTP server name.
- The `'` character may be optional for environment variables without space on them.

## Exporting Environment Variables

Assume that KEY is the name of the variable and VALUE is the actual value of the environment variable.
To export an environment variable you have to run:
```
export KEY=VALUE
```

- Example:
```
export FLASK_ENVIRONMENT_CONFIG=dev
```

Windows user should use **set** instead of **export** for setting these environment variables. <br/>
Another way to do this in flask applications is by having a file called `.env` which will have all of the environment variables. When a flask application runs, it will load these variables from the file.

- Content of `.env` file:

```
FLASK_ENVIRONMENT_CONFIG=dev
SECRET_KEY='some_random_key'
(...)
```
