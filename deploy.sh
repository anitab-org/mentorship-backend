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
if [ "$TRAVIS_BRANCH" == "gsoc18-code" ]; then
    SERVER="Development"
elif [ "$TRAVIS_BRANCH" == "develop" ]; then
    SERVER="Staging"
elif [ "$TRAVIS_BRANCH" == "master" ]; then
    SERVER="Production"
else 
    echo "Skip publishing, we don't publish for '$TRAVIS_BRANCH' branch"
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

# Publishing
echo "Publishing to '$SERVER' server"
eb deploy
if [ $? -eq 0 ]; then
    echo "Publishing successful."
else
    echo "Publishing failed."
    exit 2
fi
