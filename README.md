# Mentorship System (Backend)

![Build Status](https://github.com/anitab-org/mentorship-backend/workflows/Run%20tests/badge.svg)
[![codecov](https://codecov.io/gh/anitab-org/mentorship-backend/branch/develop/graph/badge.svg)](https://codecov.io/gh/anitab-org/mentorship-backend)
[![project chat](https://img.shields.io/badge/zulip-join_chat-brightgreen.svg)](https://anitab-org.zulipchat.com/#narrow/stream/222534-mentorship-system)
[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)


Mentorship System is an application that allows women in tech to mentor each other, on career development topics, through 1:1 relations for a certain period.
This is the Backend REST API for the Mentorship System.

This API is being used by 3 frontend projects currently being developed:
- android: [anitab-org/mentorship-android](https://github.com/anitab-org/mentorship-android)
- iOS: [anitab-org/mentorship-ios](https://github.com/anitab-org/mentorship-ios)
- flutter: [anitab-org/mentorship-flutter](https://github.com/anitab-org/mentorship-flutter)

**Table of Contents**

- [Features](#Features)
- [Setup and run](#setup-and-run)
    - [Run app in Windows](#run-app-in-Windows)
    - [Run app in Linux](#run-app-in-Linux)
    - [Run with Docker](#run-with-docker)
    - [Run tests](#run-tests)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Branches](#branches)
- [Contact](#contact)
- [License](#license)

## Features

- Once the App is installed user can view an onboarding screen which introduces the app and give user an idea of how it works.
- A member gets an option to be a Mentor, Mentee or Both.
- A member can build/customise the app profile with username, bio, skills, interests, location, occupation, etc. anytime.
- A member can read and know more about Mentorship System including the terms and conditions, privacy and policy and code of conduct.
- A member can directly access the AnitaB-org Github repo, Zulip chat and website from this App.
- A member can refresh the every page.
- A member can view a list of other members and search for a member on the Members Page.
- A member can search for particular members there in Mentorship System.
- A member can sort other members on the basis of their name either (A-Z) OR (Z-A), registration date, age.
- A member can filter other members by the label need mentoring or available to mentor, interest, location and skills that given while creating profile.
- A member can either send mentorship requests to other members as a Mentor or Mentee according to their interests or reject mentorship requests from other members.
- A member can track the number of Pending Resquests, Accepted Requests, Rejected Requests, and Completed Requests and view Recent Achievements on the Home Page.
- A member can view the details of pending, past, all the mentorship requests in the Requests Page.
- A member can create, update, or delete tasks in their current mentorship relation.
- A member can send feedback about the Mentorship System such as reporting a bug, giving suggestions or other comments.
- A member can delete their account.
- A member can change their account password anytime.
## Setup and run

To setup the project locally read these wiki pages and follow the instructions:

 - [Fork, Clone and Remote](https://github.com/anitab-org/mentorship-backend/wiki/Fork%2C-Clone-%26-Remote)
 - [Export Environment Variables](docs/environment-variables.md)

### Run app in Windows

The project runs on Python 3.

1. Create a virtual environment:
```
virtualenv venv --python=python3
```

2. Activate the virtual environment:
For Git Bash Users:
```
source /venv/Scripts/activate
```
For Windows Command Line Users:
```
venv\Scripts\activate
```

3. Install all the dependencies in `requirements.txt` file:
```
pip install -r requirements.txt
```

4. Make sure you create `.env` using `.env.template` and update the values of corresponding environment variables
or make sure you exported the following [environment variables](docs/environment-variables.md):

```
export FLASK_ENVIRONMENT_CONFIG=<local-or-dev-or-test-or-prod-or-stag>
export SECRET_KEY=<your-secret-key>
export SECURITY_PASSWORD_SALT=<your-security-password-salt>
export MAIL_DEFAULT_SENDER=<mail-default-sender>
export MAIL_SERVER=<mail-server>
export APP_MAIL_USERNAME=<app-mail-username>
export APP_MAIL_PASSWORD=<app-mail-password>
export MOCK_EMAIL = <True-or-False>
```

If you're testing any environment other than "local", then you have to also set these other variables:
```
export DB_TYPE=<database_type>
export DB_USERNAME=<database_username>
export DB_PASSWORD=<database_password>
export DB_ENDPOINT=<database_endpoint>
export DB_NAME=<database_name>
```

5. Run the app:
```
python run.py
```

6. Navigate to http://localhost:5000 in your browser

7. When you are done using the app, deactivate the virtual environment:
```
deactivate
```

### Run app in Linux

The project runs on Python 3.

1. Create a virtual enviorntment:
```
virtualenv venv
```

2. Activate the virtual environment:
```
source venv/bin/activate
```

3. Install all the dependencies in `requirements.txt` file:
```
pip3 install -r requirements.txt
```

4. Make sure you create `.env` using `.env.template` and update the values of corresponding environment variables. Make sure you exported the following [environment variables](docs/environment-variables.md) if you didn't adapt `.env.template` in the `.env` file:

```
export FLASK_ENVIRONMENT_CONFIG=<local-or-dev-or-test-or-prod-or-stag>
export SECRET_KEY=<your-secret-key>
export SECURITY_PASSWORD_SALT=<your-security-password-salt>
export MAIL_DEFAULT_SENDER=<mail-default-sender>
export MAIL_SERVER=<mail-server>
export APP_MAIL_USERNAME=<app-mail-username>
export APP_MAIL_PASSWORD=<app-mail-password>
export MOCK_EMAIL = <True-or-False>
```

If you're testing any environment other than "local", then you have to also set these other variables in the .env file.
```
export DB_TYPE=<database_type>
export DB_USERNAME=<database_username>
export DB_PASSWORD=<database_password>
export DB_ENDPOINT=<database_endpoint>
export DB_NAME=<database_name>
```

Use: `printenv` to print the environment variables and check all configurations.

5. Run the app with `python run.py` or:
```
 export FLASK_APP=run.py
 flask run
```

6. Navigate to http://localhost:5000 or the current server in which you are running(will be shown when app is running) in your browser.

7. When you are done using the app, deactivate the virtual environment:
```
deactivate
```

or use:

```
source deactivate
```

### Run with docker

1. Make sure you exported the following [environment variables](docs/environment-variables.md) to `.env` file

2. Build docker image
```
docker build -t mentorship-backend:latest .
```
3. Deploy
Docker container ports must be mapped to the host machine port using '--publish' so they're visible.
```sh
docker run --env "FLASK_APP=run.py" --publish 5000:5000 mentorship-backend:latest
```

### Run tests

To run the unitests run the following command in the terminal (while the virtual environment is activated):

```
python -m unittest discover tests
```

### Auto-formatting with black

We use [_Black_](https://github.com/psf/black) to format code automatically so that we don't have to worry about clean and
readable code. To install _Black_:

```
pip install black
```

To run black:

```
black .
```

## Documentation

You can learn more about this project through the documentation in the [docs](./docs) folder and on [our Wiki](https://github.com/anitab-org/mentorship-backend/wiki).

- **Language:** Python 3
- **Framework:** [Flask](http://flask.pocoo.org/)
- **Flask Extensions:** [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/), [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org), [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/latest/), [Flask-Mail](https://pythonhosted.org/Flask-Mail)

Here are some links to documentation for this project:

- [How to use Backend Swagger UI](https://github.com/anitab-org/mentorship-backend/wiki/Using-Backend-Swagger-UI) and [test PR guide](/docs/test-pr-guide.md) contains a few resources for you to understand how to use the Swagger user interface provided by this app.
- [Features Overview](/docs/features.md) has a high level understanding of the features this application has.
- [Future ideas for the project](https://github.com/anitab-org/mentorship-backend/wiki/Future-ideas).
- [Troubleshoot guide](/docs/troubleshoots.md) contains common isssues other contributors may run into in their setup.
- [Quality Assurance test cases](/docs/quality-assurance-test-cases.md) has test cases for each endpoint we have which you can use to learn about how each feature should work.
- [CI/CD Process](/docs/ci_cd_process.md) which explains the processes and tools involved in deploying new code.
- [Code Organisation](/docs/code_organization.md) which explains the code organisation and architecture within the repository.
- [User Authentication](/docs/user_authentication.md) which is JSON Web Token (JWT) based and tells about the user authentication in the application.

Understand more about our technical decisions made along with this project development in [Technical Decisions Wiki page](https://github.com/anitab-org/mentorship-backend/wiki/Technical-Decisions).

## Contributing

Please read our [Contributing guidelines](./.github/CONTRIBUTING.md), [Code of Conduct](./docs/code_of_conduct.md) and [Reporting Guidelines](http://systers.io/reporting-guidelines)

Please follow our [Commit Message Style Guide](https://github.com/anitab-org/mentorship-backend/wiki/Commit-Message-Style-Guide) and [Coding Standards](./docs/coding_standards.md) while sending PRs.

## Branches

The repository has the following permanent branches:

 * **master** This contains the code which has been released.

 * **develop** This contains the latest code. All the contributing PRs must be sent to this branch. When we want to release the next version of the app, this branch is merged into the `master` branch. This is the branch that is used in the deployed version of the app on Heroku.

## Contact

You can reach the maintainers and our community on [AnitaB.org Open Source Zulip](https://anitab-org.zulipchat.com/). If you are interested in contributing to the mentorship system, we have a dedicated stream for this project [#mentorship-system](https://anitab-org.zulipchat.com/#narrow/stream/222534-mentorship-system), where you can ask questions and interact with the community, join with us!

## License

Mentorship System is licensed under the GNU General Public License v3.0. Learn more about it in the [LICENSE](LICENSE) file.
