# mentorship-backend

Backend REST API for Mentorship System. Depending on branches the following instances of application are running

| Branch | Server |
| :---: | :---: |
| [gsoc18-code](https://github.com/systers/mentorship-backend/tree/gsoc18-code) | [Development](http://systers-mentorship-test.zsgdmpswrc.eu-central-1.elasticbeanstalk.com/) |
| [develop](https://github.com/systers/mentorship-backend/tree/develop) | Staging |
| [master](https://github.com/systers/mentorship-backend/tree/master) | Production |

## Setup and run

The project runs on Python 3. 

1. Create a virtual environment:
`virtualenv venv --python=python3`

2. Activate the virtual environment:
`source ./venv/bin/activate`

3. Install all the dependencies in `requirements.txt` file:
`pip install -r requirements.txt`

4. Export the following environment variables:

```
export  SECRET_KEY=<your-secret-key>
export  FLASK_ENVIRONMENT_CONFIG=<dev-or-test-or-prod>
```

5. Run the app:
`python run.py`

6. When you are done using the app, deactivate the virtual environment:
`deactivate`

### Run tests

To run the unitests run the following command in the terminal (while the virtual environment is activated):

`python -m unittest discover tests`
