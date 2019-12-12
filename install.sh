#!/usr/bin/env bash

GREEN=$'\e[0;32m'
RED=$'\e[0;31m'
PURPLE=$'\e[0;35m'
CYAN=$'\e[0;36m'
NC=$'\e[0m'

echo "Welcome to ${PURPLE}mentorship-backend${NC} installer!"
read -p "[ press Enter to begin ] "

mode="" # "clone" or "install"
current_dir=${PWD##*/}

if [ "$current_dir" == "mentorship-backend" ]; then
  mode="install"
else
  mode="clone"
fi


if [ -d "mentorship-backend" ]; then
  echo "${RED}WARNING! Read below!${NC}"
  echo "mentorship-backend directory already exists. It ${RED}will be deleted${NC} and replaced with the one pulled from GitHub."
  read -p "Do you want to proceed? [y/n]: " agree
  
  echo $agree
  
  if [ "$agree" == "y" ] || [ "$agree" == "Y" ]; then
    rm -rf mentorship-backend
    echo "mentorship-backend directory was removed!"
  else
    echo "${RED} Setup cancelled by user${NC}"
    exit 2
  fi
fi

if [ "$mode" == "clone" ]; then
  echo "Cloning project from GitHub..."
  git clone https://github.com/systers/mentorship-backend.git
  echo "Project cloned successfully!"
  cd mentorship-backend
fi

# Email
read -p "Enter admin account email address: " email
while ! [[ "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$ ]]; do
  echo "${RED}Entered string isn't a correct email address. Please try again.${NC}"
  read -p "Enter admin account email address: " email
done
echo "Admin email:${CYAN} $email ${NC}"

# Username
username=$(echo $email | cut -f1 -d"@")
echo "Username inferred from email is:${CYAN} $username ${NC}"

# Password
read -p "Enter password for $email: " password
while [ -z ${password} ]; do
  echo "${RED}Password is empty. Try again.${NC}"
  read -p "Enter password for $email: " password
done
echo "Password:${CYAN} $password ${NC}"

# Mail server
read -p "Enter mail server address: " mailserver
while [ -z ${mailserver} ]; do
  echo "${RED}Mail server is empty. Try again.${NC}"
  read -p "Enter mail server address: " mailserver
done
echo "Mailserver:${CYAN} $mailserver ${NC}"

PS3='Select environment config [number]: '
configs=("dev" "test" "prod")
select env_config in "${configs[@]}"
do
  case $env_config in
    "dev")
      echo "Environment will be set up as ${GREEN}$env_config${NC}"
      break
    ;;
    "test")
      echo "Environment will be set up as ${GREEN}$env_config${NC}"
      break
    ;;
    "prod")
      echo "Environment will be set up as ${GREEN}$env_config${NC}"
      break
    ;;
    *) echo "${RED}Invalid option. Try again.${NC}";;
  esac
done


read -p "Enter secret key [ press Enter to use default ]: " secret_key
secret_key="${secret_key:=default}"

read -p "Enter password salt [ press Enter to use default ]: " password_salt
password_salt="${password_salt:=default}"

# Install the rest of stuff

echo "Detected python3 version: $(python3 --version)"

echo "Installing virtualenv..."
pip3 install virtualenv

echo "Creating virtual environment named \"venv\" "
virtualenv venv --python=python3

source ./venv/bin/activate

echo "Installing dependencies from requirements.txt"
pip3 install -r requirements.txt

touch .env

echo "export FLASK_ENVIRONMENT_CONFIG=$env_config" >> .env
echo "export SECRET_KEY=$secret_key" >> .env
echo "export SECURITY_PASSWORD_SALT=$password_salt" >> .env
echo "export MAIL_DEFAULT_SENDER=$email" >> .env
echo "export MAIL_SERVER=$mailserver" >> .env
echo "export APP_MAIL_USERNAME=$username" >> .env
echo "export APP_MAIL_PASSWORD=$password" >> .env

read -p "Do you want to run unittest now? ${GREEN}(recommended)${NC} [y/n] " unittests
if [ "$unittests" == "y" ] || [ "$unittests" == "Y" ]; then
  python3 -m unittest discover tests
fi

### SUCCESS ###
# Display some helpful info

echo "${GREEN}Installation has been completed successfully!${NC}"

echo ""
echo "--- How to use virtualenv? (below) ---"
echo "To activate the virtual environment (virtualenv):"
echo "${CYAN}\$ source ./venv/bin/activate${NC}"
echo "To deactivate the virtual environment:"
echo "${CYAN}\$ deactivate${NC}"
echo ""

echo "${GREEN}> ${NC}Below are some links you might want to check out${GREEN} <${NC}"
echo "Project's GitHub: https://github.com/systers/mentorship-backend"
echo "Wiki page: https://github.com/systers/mentorship-backend/wiki"
echo "Our Slack: https://systers-opensource.slack.com/"

read -p "Do you want to start the server now? [y/n] " startnow
if [ "$startnow" == "y" ] || [ "$startnow" == "Y" ]; then
  python3 run.py
fi
