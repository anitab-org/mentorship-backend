#!/usr/bin/env bash

# Easy setup - change only what's unique to you

export FLASK_ENVIRONMENT_CONFIG=dev
export SECRET_KEY='some random key'
export SECURITY_PASSWORD_SALT='some password salt'
export MAIL_DEFAULT_SENDER='username@gmail.com' # replace with the Gmail account address that you created
export MAIL_SERVER='smtp.gmail.com'
export APP_MAIL_USERNAME='username' # replace with the part of the email before "@"
export APP_MAIL_PASSWORD='password' # replace with password to the email