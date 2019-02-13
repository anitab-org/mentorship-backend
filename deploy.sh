#!/usr/bin/env bash

# Travis build triggered on a forked repository
if [ "$TRAVIS_REPO_SLUG" != "systers/mentorship-backend" ]; then
    echo "Skip publishing, this is a forked repo."
    exit 0
fi

# Travis build triggered by a PR
if [ "$TRAVIS_PULL_REQUEST" != "false" ]; then
    echo "Skip publising, just a PR."
    exit 0
fi

# Checking branch
if [ "$TRAVIS_BRANCH" == "develop" ]; then
    FLASK_ENVIRONMENT_CONFIG="dev"
    SERVER="Development"
elif [ "$TRAVIS_BRANCH" == "master" ]; then
    FLASK_ENVIRONMENT_CONFIG="prod"
    SERVER="Production"
else 
    echo "Skip publishing, we don't publish for branches other than develop and master."
    exit 0
fi

# Get the latest code
cd $HOME
git clone --branch=$TRAVIS_BRANCH https://github.com/systers/mentorship-backend.git
cd mentorship-backend

# Create AWS Elastic Beanstalk profile
mkdir ~/.aws
echo "[profile eb-cli]" > ~/.aws/config
echo "aws_access_key_id = $AWS_ACCESS_ID" >> ~/.aws/config
echo "aws_secret_access_key = $AWS_SECRET_KEY" >> ~/.aws/config

# Add environment variables
eb setenv FLASK_ENVIRONMENT_CONFIG=$FLASK_ENVIRONMENT_CONFIG MAIL_DEFAULT_SENDER=$MAIL_DEFAULT_SENDER MAIL_SERVER=$MAIL_SERVER APP_MAIL_USERNAME=$APP_MAIL_USERNAME APP_MAIL_PASSWORD=$APP_MAIL_PASSWORD SECRET_KEY=$SECRET_KEY SECURITY_PASSWORD_SALT=$SECURITY_PASSWORD_SALT

# Publishing
echo "Publishing to '$SERVER' server"
eb deploy
if [ $? -eq 0 ]; then
    echo "Publishing successful."
else
    echo "Publishing failed."
    exit 2
fi
# Pylint code quality check
find . -name "*.py" -depth -exec pylint {} \; |   # Finding files with .py extension
grep -oE "\-?[0-9]+\.[0-9]+" |                    # Extract the score from each message
awk 'NR==1 || NR % 4 == 0' |                      # Previuos command will generate garbage numbers as weel, this cuts away unnecasary data
while read -r i
do  
    if (( $(echo "$i < 7.00" |bc -l) )); then
        exit 2    
    fi
done
