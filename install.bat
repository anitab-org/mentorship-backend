@ECHO OFF

ECHO Welcome to mentorship-backend installer!

SET /P email="Enter admin account email address: "
ECHO Email: %email%

SET /P username="Enter admin username (part of email before "@"): "
ECHO Username: %username%

SET /P password="Enter password for email %email%: "
ECHO Password: %password%

SET /P mailserver="Enter mailserver address: "
ECHO Mailserver: %mailserver%

ECHO 1. dev
ECHO 2. test
ECHO 3. prod

CHOICE /C 123 /M "Select environment config: "
If %ErrorLevel%==1 GOTO dev
If %ErrorLevel%==2 GOTO test
If %ErrorLevel%==3 GOTO prod
Exit/B

:dev
SET config=dev
GOTO end

:test
SET config=test
GOTO end

:prod
SET config=prod
GOTO end

:end
ECHO Environment config: %config%

SET /P secret="Enter secret key: "
ECHO Secret: %secret%

SET /P salt="Enter security password salt: "
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

python3 -m unittest discover tests

ECHO Installation successful!

PAUSE