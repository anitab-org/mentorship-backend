# mentorship-backend

Backend REST API for Mentorship System.

## Setup and run

### Setup environment

First you have to create a virtual environment using python 3.x:
```
virtualenv venv --python=python3
```

1. Activate the virtual environment running on terminal `source ./venv/bin/activate` (to deactivate use `deactivate`).
2. Then install all the dependencies in `requirements.txt` with `pip install requirements.txt`

### Run app

To run the app type this on the terminal:
```
python -m app.run
```


### Run tests

To run the unitests type this on the terminal:
```
python -m unittest discover tests
```
