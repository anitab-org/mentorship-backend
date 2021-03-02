# mentorship-backend

Backend REST API for Mentorship System.

## Setup and run

The project runs on Python 3. 

1. Create a virtual environment:
`virtualenv venv --python=python3`

2. Activate the virtual environment:
`source ./venv/bin/activate`

3. Install all the dependencies in `requirements.txt` file:
`pip install -r requirements.txt`

4. Run the app:
`python run.py`

5. When you are done using the app, decativate the virtual environment:
`deactivate`


### Run tests

To run the unitests type this on the terminal:
```
python -m unittest discover tests
```
