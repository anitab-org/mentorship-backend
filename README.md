# Mentorship System (Backend)

| Branch | [Travis](https://travis-ci.org/) | [Codacy](https://www.codacy.com/) | Server |
| :---: | :---: | :---: | :---: |
| [master](https://github.com/systers/mentorship-backend/tree/master) | [![Build Status](https://travis-ci.org/systers/mentorship-backend.svg?branch=master)](https://travis-ci.org/systers/mentorship-backend) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5181ca06835045d1aea78fdd30fc37d9?branch=master)](https://www.codacy.com/app/systers/mentorship-backend) | [Production](http://systers-mentorship.eu-central-1.elasticbeanstalk.com/) |
| [develop](https://github.com/systers/mentorship-backend/tree/develop) | [![Build Status](https://travis-ci.org/systers/mentorship-backend.svg?branch=develop)](https://travis-ci.org/systers/mentorship-backend) | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5181ca06835045d1aea78fdd30fc37d9?branch=develop)](https://www.codacy.com/app/systers/mentorship-backend) | [Development](http://systers-mentorship-dev.eu-central-1.elasticbeanstalk.com/) |

[Mentorship System](https://github.com/systers/mentorship-backend) is an application that allows women in tech to mentor each other, on career development topics, through 1:1 relations for a certain period.
This is the Backend REST API for the Mentorship System.

## Setup and run

To setup the project locally read these wiki pages and follow the instructions:

 - [Fork, Clone and Remote](https://github.com/systers/mentorship-backend/wiki/Fork%2C-Clone-%26-Remote)
 - [Export Environment Variables](https://github.com/systers/mentorship-backend/wiki/Environment-Variables)

### Run app

The project runs on Python 3.

1. Create a virtual environment:
`virtualenv venv --python=python3`

2. Activate the virtual environment:
`source ./venv/bin/activate`

3. Install all the dependencies in `requirements.txt` file:
`pip install -r requirements.txt`

4. Make sure you create `.env` using `.env.template` and update the values of corresponding environment variables
or
make sure you exported the following [environment variables](https://github.com/systers/mentorship-backend/wiki/Environment-Variables):

```
export FLASK_ENVIRONMENT_CONFIG=<dev-or-test-or-prod>
export SECRET_KEY=<your-secret-key>
export SECURITY_PASSWORD_SALT=<your-security-password-salt>
export MAIL_DEFAULT_SENDER=<mail-default-sender>
export MAIL_SERVER=<mail-server>
export APP_MAIL_USERNAME=<app-mail-username>
export APP_MAIL_PASSWORD=<app-mail-password>
```

5. Run the app:
`python run.py`

6. When you are done using the app, deactivate the virtual environment:
`deactivate`

### Run with docker
1. Make sure you exported the following [environment variables](https://github.com/systers/mentorship-backend/wiki/Environment-Variables) to '.env' file

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

`python -m unittest discover tests`

## Contributing

Please read our [Contributing guidelines](https://github.com/systers/mentorship-backend/blob/develop/.github/CONTRIBUTING.md), [Code of Conduct](http://systers.io/code-of-conduct) and [Reporting Guidelines](http://systers.io/reporting-guidelines)

Please follow our [Commit Message Style Guide](https://github.com/systers/mentorship-backend/wiki/Commit-Message-Style-Guide) while sending PRs.

## Branches

The repository has the following permanent branches:

 * **master** This contains the code which has been released.

 * **develop** This contains the latest code. All the contributing PRs must be sent to this branch. When we want to release the next version of the app, this branch is merged into the `master` branch.

## Contact

You can reach maintainers team @mentorship-team on [Systers Open Source Slack](http://systers.io/slack-systers-opensource/) or @systers/maintainers-mentorship-backend on GitHub.

We use [#mentorship-system](https://systers-opensource.slack.com/messages/CAE8QK41L/) channel on Slack to discuss this project. If you're interested in contributing to this project, join us there!
