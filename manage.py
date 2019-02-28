"""
This module is to suffice all the major commands in one script
directly through terminal/command-line using:

python manage.py <cmd> [args]

cmd
- To run the app = runserver
    eg. python manage.py runserver
- To create first user (by default with admin status) = createsuperuser
    eg. python manage.py createsuperuser
- To run all tests = test
    eg. python manage.py test
- To run specific test = test [args]
    eg. python manage.py test admin tasks
    (it will run all tests for admin and tasks)
"""

import os
import sys
import time
import unittest

from unittest.loader import TestLoader
from app.database.models.user import UserModel
from run import application


def build(cmd_line_arguments):
    """
    Build the app.
    """
    if len(cmd_line_arguments) > 1:
        if cmd_line_arguments[1] == "runserver":
            run_server()
        elif cmd_line_arguments[1] == "createsuperuser":
            create_superuser()
        elif cmd_line_arguments[1] == "test":
            test(cmd_line_arguments[2:])
        else:
            print("'" + cmd_line_arguments[1]  + "'" + " command is not available!")

    else:
        print(" No parameters given ")

def run_server():
    """
    Run the app.
    """
    application.run(port=5000)
    return 0

def test(list_to_test):
    """
    It will perform tests (on all or some specific parts).
    """
    # if additional arguments then it will test only for specified parts
    testloader = TestLoader()
    if list_to_test:
        for test_area in list_to_test:
            suite = testloader.discover(start_dir=test_area, top_level_dir="tests/")
            print("\nTesting " + test_area)
            unittest.TextTestRunner().run(suite)

    else:
        suite = testloader.discover(start_dir=".", top_level_dir=None)
        unittest.TextTestRunner().run(suite)
    return 0

def create_superuser():
    """
    It will create the admin (if it is first user). It uses environment
    variables for name, username, password and email for SuperUser.
    """
    with application.app_context():
        if UserModel.is_empty():
            heading = "-"*14 + " Registered SuperUser(First user) " + "-"*14
            print(heading)
            name = os.getenv('SUPERUSER_NAME', None)
            username = os.getenv('SUPERUSER_USERNAME', None)
            email = os.getenv('SUPERUSER_EMAIL', None)
            password = os.getenv('SUPERUSER_PASSWORD', None)
            terms_and_conditions_checked = True
            user = UserModel(name, username,
                             password, email, terms_and_conditions_checked)
            user.isadmin = True
            user.is_email_verified = True
            user.need_mentoring = True
            user.available_to_mentor = True
            user.registration_date = time.time()
            user.save_to_db()
            print("Name: " + name)
            print("Username: " + username)
            print("Email: " + email)
            print("Password: " + password)

        else:
            print("You are not the first user")


if __name__ == "__main__":
    build(sys.argv)
