@echo off

echo Welcome to mentorship-backend installer!

set /p email="Enter admin account email address: "
echo Email: %email%

set /p username="Enter admin username (part of email before "@"): "
echo Username: %username%

set /p password="Enter password for email %email%: "
echo Password: %password%

set /p mailserver="Enter mailserver address: "
echo Mailserver: %mailserver%

set /p config="Enter environment config (dev OR test OR prod): "
echo Config: %config%

set /p secret="Enter secret key: "
echo Secret: %secret%

set /p salt="Enter security password salt: "
echo salt: %salt%

@echo set FLASK_ENVIRONMENT_CONFIG=%config%> .env
@echo set SECRET_KEY=%secret%>> .env
@echo set SECURITY_PASSWORD_SALT=%salt%>> .env
@echo set MAIL_DEFAULT_SENDER=%email%>> .env
@echo set MAIL_SERVER=%mailserver%>> .env
@echo set APP_MAIL_USERNAME=%username%>> .env
@echo set APP_MAIL_PASSWORD=%password%>> .env

pip3 install virtualenv

virtualenv venv

echo virtual environment created

venv\Scripts\activate

echo virtual environment activated

pip3 install -r requirements.txt

echo dependencies installed

python -m unittest discover tests

pause