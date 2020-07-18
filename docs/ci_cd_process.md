# CI / CD process

This document aims to explain everything related to Continuous Integration and Continuous Development (CI / CD) processes of the app.

## Deployment process

This app is in current development under the `develop` branch. The `master` branch is currently empty, because we have not yet put this into production (however this is in the works).

Currently we have the development version oof this app deployed on [Heroku]. Because we have "Automatic Deploys" feature  enabled, everytime a new pull request is merged into `develop` branch a new version of the app is deployed to [Heroku].

🔗 https://mentorship-backend-temp.herokuapp.com/

## Pull Request Checks

We use [GitHub Actions](https://github.com/features/actions) to perform checks on every PR which runs unit tests and performs code coverage analysis.
You can see the GitHub actions workflow [here](/.github/workflows/main.yml).

We use [Codecov](https://codecov.io/) to check the code coverage in our code.

## Development environment

As mentioned before in development environment we are hosting the app on [Heroku] so that it is available to anyone interested in testing it without having to setup the development envioronment locally.

Regarding the data we host, we are using a PostgreSQL database as a service called [ElephantSQL], which is the Heroku app is connected to.

[Heroku]: https://www.heroku.com/
[ElephantSQL]: https://www.elephantsql.com/
