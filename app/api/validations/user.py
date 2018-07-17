from app.utils.validation_utils import is_email_valid, is_username_valid

# Field character limit

NAME_MAX_LENGTH = 30
NAME_MIN_LENGTH = 2
USERNAME_MAX_LENGTH = 25
USERNAME_MIN_LENGTH = 5
PASSWORD_MAX_LENGTH = 25
PASSWORD_MIN_LENGTH = 8


def validate_user_registration_request_data(data):
    # Verify if request body has required fields
    if 'name' not in data:
        return {"message": "Name field is missing."}
    if 'username' not in data:
        return {"message": "Username field is missing."}
    if 'password' not in data:
        return {"message": "Password field is missing."}
    if 'email' not in data:
        return {"message": "Email field is missing."}
    if 'terms_and_conditions_checked' not in data:
        return {"message": "Terms and conditions field is missing."}

    name = data['name']
    username = data['username']
    password = data['password']
    email = data['email']
    terms_and_conditions_checked = data['terms_and_conditions_checked']

    if not (isinstance(name, str) and isinstance(username, str) and isinstance(password, str)):
        return {"message": "Name, username and password must be in string format."}

    if not (NAME_MIN_LENGTH <= len(name) <= NAME_MAX_LENGTH):
        return {"message": "The name field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=NAME_MIN_LENGTH-1,
                                                                                        max_limit=NAME_MAX_LENGTH+1)}

    if not (USERNAME_MIN_LENGTH <= len(username) <= USERNAME_MAX_LENGTH):
        return {"message": "The username field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=USERNAME_MIN_LENGTH-1,
                                                                                        max_limit=USERNAME_MAX_LENGTH+1)}

    if not (PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH):
        return {"message": "The password field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=PASSWORD_MIN_LENGTH-1,
                                                                                        max_limit=PASSWORD_MAX_LENGTH+1)}

    # Verify business logic of request body
    if terms_and_conditions_checked is False:
        return {"message": "Terms and conditions are not checked."}

    if not is_email_valid(email):
        return {"message": "Your email is invalid."}

    if not is_username_valid(username):
        return {"message": "Your username is invalid."}

    return {}


def validate_resend_email_request_data(data):

    # Verify if request body has required fields
    if 'email' not in data:
        return {"message": "Email field is missing."}

    email = data['email']
    if not is_email_valid(email):
        return {"message": "Your email is invalid."}

    return {}
