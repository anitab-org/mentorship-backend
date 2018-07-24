import re

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_regex = r"(^[a-zA-Z0-9_]+$)"


def is_email_valid(email):
    return re.match(email_regex, email)


def is_username_valid(username):
    return re.match(username_regex, username)


def validate_length(field_length, min_length, max_length, field_name):
    if not (min_length <= field_length <= max_length):
        if min_length <= 0:
            error_msg = {"message": get_length_validation_error_message(field_name, None, max_length)}
        else:
            error_msg = {"message": get_length_validation_error_message(field_name, min_length, max_length)}
        return False, error_msg
    else:
        return True, {}


def get_length_validation_error_message(field_name, min_length, max_length):
    if min_length is None:
        return "The {field_name} field has to be shorter than {max_limit} characters.".format(field_name=field_name,
                                                                                              max_limit=max_length + 1)
    else:
        return "The {field_name} field has to be longer than {min_limit} " \
               "characters and shorter than {max_limit} characters.".format(field_name=field_name,
                                                                            min_limit=min_length - 1,
                                                                            max_limit=max_length + 1)


def get_stripped_string(string_with_whitespaces):
    return ''.join(string_with_whitespaces.split())
