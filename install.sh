#!/bin/bash 
# this script does the following
# 1. checks if mentorship-backend repository, .env file and virtual environment exists otherwise creates them
# 2. .env inputs: Exits if inputs are invalid. APP_MAIL_USERNAME is found using substring
# 3. Installs python dependencies
# 4. Performs unit tests
# 5. Runs the backend
write_dir="yes"
write_env="yes"
write_virtualenv="yes"

if [ -d "mentorship-backend" ] 
then
    read -p "Directory /mentorship-backend exists, do you want to overwrite it?(yes/no): " write_dir
    if [ $write_dir == "yes" ] 
    then
        rm -rf mentorship-backend
        git clone https://github.com/systers/mentorship-backend.git        
    fi
fi
if [ $write_dir == "yes" ]
then
    git clone https://github.com/systers/mentorship-backend.git 
fi

cd mentorship-backend
if [ -f ".env" ] 
then
    read -p ".env file exists, do you want to overwrite it?(yes/no): " write_env
    if [ $write_env == "yes" ] 
    then
        rm .env
    fi
fi

if [ $write_env == "yes" ]
then
    echo "Environment variable setup: please enter details"

    echo "FLASK_ENVIRONMENT_CONFIG=<dev-or-test-or-prod>" && read FLASK_ENVIRONMENT_CONFIG
    if [[ -z "$FLASK_ENVIRONMENT_CONFIG" ]]; then
    printf '%s\n' "No input entered"
    exit 1
    fi
    echo "SECRET_KEY=<your-secret-key>" && read SECRET_KEY
    if [[ -z "$SECRET_KEY" ]]; then
    printf '%s\n' "No input entered"
    exit 1
    fi
    echo "SECURITY_PASSWORD_SALT=<your-security-password-salt>" && read SECURITY_PASSWORD_SALT
    if [[ -z "$SECURITY_PASSWORD_SALT" ]]; then
    printf '%s\n' "No input entered"
    exit 1
    fi
    echo "MAIL_DEFAULT_SENDER=<mail-default-sender>" && read MAIL_DEFAULT_SENDER
    if [[ -z "$MAIL_DEFAULT_SENDER" ]]; then
    printf '%s\n' "No input entered"Directory /mentorship-backend exists
    exit 1
    fi
    echo "MAIL_SERVER=<mail-server>" && read MAIL_SERVER
    if [[ -z "$MAIL_SERVER" ]]; then
    printf '%s\n' "No input entered"
    exit 1
    fi
    # find APP_MAIL_USERNAME using substring
    APP_MAIL_USERNAME=${MAIL_DEFAULT_SENDER%@*}

    echo "APP_MAIL_PASSWORD=<app-mail-password>" && read APP_MAIL_PASSWORD
    if [[ -z "$APP_MAIL_PASSWORD" ]]; then
    printf '%s\n' "No input entered"
    exit 1
    fi

    echo "export FLASK_ENVIRONMENT_CONFIG=$FLASK_ENVIRONMENT_CONFIG" >> .env
    echo "export SECRET_KEY=$SECRET_KEY" >> .env
    echo "export SECURITY_PASSWORD_SALT=$SECURITY_PASSWORD_SALT" >> .env
    echo "export MAIL_DEFAULT_SENDER=$MAIL_DEFAULT_SENDER" >> .env
    echo "export MAIL_SERVER=$MAIL_SERVER" >> .env
    echo "export APP_MAIL_USERNAME=$APP_MAIL_USERNAME" >> .env
    echo "export APP_MAIL_PASSWORD=$APP_MAIL_PASSWORD" >> .env
else
    echo "skipping .env setup"
fi

echo "creating virtual environment"
pip3 install --user virtualenv
if [ -d "venv" ] 
then
    read -p "Virtual environment, do you want to overwrite it?(yes/no): " write_virtualenv
    if [ $write_virtualenv == "yes" ] 
    then
        rm -rf venv
    fi
fi

if [ $write_virtualenv == "yes" ]
then
    virtualenv venv -p python3
fi
source venv/bin/activate
echo "installing dependencies from requirements.txt"
pip3 install -r requirements.txt
echo "Running unit tests"
python3 -m unittest discover tests
echo "---------------congratulations---------------"
python3 run.py