@ECHO off

ECHO "Welcome to the setup for mentorship-backend repo."

ECHO "This installation requires Python version above 3.0. Make sure you have it installed."

SET /P check_repo="Do you want to clone the repository [y/n] : "
IF %check_repo%==y ( ECHO "Cloning the repository"
git clone https://github.com/systers/mentorship-backend.git 
cd mentorship-backend
) ELSE ( 
ECHO "Make sure that you have the repository and the install.bat file in the same folder!" 
)

ECHO "Installing the virtual environment - 'venv'"
pip3 install virtualenv
virtualenv venv

CALL venv\Scripts\activate	

ECHO "Activated virtual environment - 'venv'"

ECHO "Installing the required modules"
pip3 install -r requirements.txt
IF %errorlevel% == 0 ( 
goto :next 
) ELSE ( 
ECHO "Error in installing modules. Exited with status : %errorlevel%"
goto :help
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

ECHO "Setting up the MAIL_SERVER"
set "server=%mail_sender:@=" & set "server=%"
set "mail_server=smtp.%server%"
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
goto :help 
)

:help

ECHO "Follow the below mentioned links according to the status codes : "

ECHO "Status 1 OR 9009 : "
ECHO "For error in installing modules : https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command"

ECHO "For error in unit testing :https://stackoverflow.com/questions/17953124/python-is-not-recognized-as-an-internal-or-external-command"

ECHO "Status 2 OR 3 : https://stackoverflow.com/questions/33638281/what-is-the-reason-for-the-error-message-system-cannot-find-the-path-specified"

ECHO "Status 5 : https://www.eassos.com/how-to/how-to-fix-access-denied-error-in-windows.php"

goto :steps

:steps
ECHO "-----------------------------"
ECHO "Steps to activate the virtual environment again..."
ECHO "1. Locate to the mentorship-backend project in your system"
ECHO "2. Enter the following command - 'CALL venv\Scripts\activate'"

ECHO "To follow the entire process manually, please visit : 'https://github.com/systers/mentorship-backend/blob/develop/README.md'"
ECHO "Exiting.."

deactivate

EXIT /B 0
