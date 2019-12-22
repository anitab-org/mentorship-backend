FROM python:3.7

# Copying all the files to 'dockerRun' folder
COPY . /dockeRun
# Changing the working directory
WORKDIR /dockeRun

# This statement installs all the required modules from the 'requirements.txt' file.
RUN pip install -r requirements.txt

COPY . /dockeRun

# This statement runs the 'run.py' file
CMD [ "python","run.py" ]
