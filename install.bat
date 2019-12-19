@ECHO off

ECHO "Welcome to the setup for mentorship-backend repo."

ECHO "This installation requires Python version above 3.0. Make sure you have it installed."

SET /P check_repo="Do you want to clone the repository [y/n] : "
IF %check_repo%==y ( ECHO "Cloning the repository"
git clone https://github.com/systers/mentorship-backend.git 
) ELSE ( 
ECHO "Make sure that you have the repository and the install.bat file in the same folder!" 
)

cd mentorship-backend

ECHO "Installing the virtual environment - 'venv'"
pip3 install virtualenv
virtualenv venv --python=python3

CALL venv\Scripts\activate	

ECHO "Activated virtual environment - 'venv'"

ECHO "Installing the required modules"
pip3 install -r requirements.txt
IF %errorlevel% == 0 ( 
goto :next 
) ELSE ( 
ECHO "Error in installing modules. Exited with status : %errorlevel%"
goto :steps
)

:next
ECHO "Setting up the environment variables"

SET /P config="Enter value for FLASK_ENVIRONMENT_CONFIG (dev/test/prod)"
SET FLASK_ENVIRONMENT_CONFIG=%config%

SET /P secret_key="Enter value for SECRET_KEY"
SET SECRET_KEY=%secret_key%

SET /P security_password_salt="Enter value for SECURITY_PASSWORD_SALT"
SET SECURITY_PASSWORD_SALT=%security_password_salt%

SET /P mail_sender="Enter value for MAIL_DEFAULT_SENDER "
SET MAIL_DEFAULT_SENDER=%mail_sender%

SET /P mail_server="Enter value for MAIL_SERVER "
SET MAIL_SERVER=%mail_server%

SET /P app_mail_username="Enter value for APP_MAIL_USERNAME "
SET APP_MAIL_USERNAME=%app_mail_username%

SET /P app_mail_password="Enter value for APP_MAIL_PASSWORD "
SET APP_MAIL_PASSWORD=%app_mail_password%

ECHO "Executing the unit test"
python3 -m unittest discover tests

IF %errorlevel% == 0 (
 ECHO "Congratulations! Installation Successful"
goto :steps 
) ELSE ( 
ECHO "Error while testing the file. Exited with status : %errorlevel%"
goto :steps
)

:steps
ECHO "Steps to activate the virtual environment again..."
ECHO "1. Locate to the mentorship-backend project in your system"
ECHO "2. Enter the following command - 'CALL venv\Scripts\activate'"

ECHO "To follow the entire process manually, please visit : 'https://github.com/systers/mentorship-backend/blob/develop/README.md'"
ECHO "Exiting.."

deactivate

EXIT /B 0
