@ECHO OFF

ECHO Welcome to mentorship-backend installer!

SET /p email="Enter admin account email address: "
ECHO Email: %email%

SET /p username="Enter admin username (part of email before "@"): "
ECHO Username: %username%

SET /p password="Enter password for email %email%: "
ECHO Password: %password%

SET /p mailserver="Enter mailserver address: "
ECHO Mailserver: %mailserver%

SET /p config="Enter environment config (dev OR test OR prod): "
ECHO Config: %config%

SET /p secret="Enter secret key: "
ECHO Secret: %secret%

SET /p salt="Enter security password salt: "
ECHO salt: %salt%

@ECHO set FLASK_ENVIRONMENT_CONFIG=%config%> .env
@ECHO set SECRET_KEY=%secret%>> .env
@ECHO set SECURITY_PASSWORD_SALT=%salt%>> .env
@ECHO set MAIL_DEFAULT_SENDER=%email%>> .env
@ECHO set MAIL_SERVER=%mailserver%>> .env
@ECHO set APP_MAIL_USERNAME=%username%>> .env
@ECHO set APP_MAIL_PASSWORD=%password%>> .env

pip3 install virtualenv

virtualenv venv

ECHO virtual environment created

CALL venv\Scripts\activate

ECHO virtual environment activated

pip3 install -r requirements.txt

ECHO dependencies installed

python -m unittest discover tests

ECHO Installation successful!

PAUSE