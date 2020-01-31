import re

name_regex = r"(^[a-zA-Z\s\-]+$)"
email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_regex = r"(^[a-zA-Z0-9_]+$)"


def is_name_valid(name):
    return re.match(name_regex, name)


def is_email_valid(email):
    return re.match(email_regex, email)


def is_username_valid(username):
    return re.match(username_regex, username)


def validate_length(field_length, min_length, max_length, field_name):
    if not (min_length <= field_length <= max_length):
        if min_length <= 0:
            error_msg = {
                "message": get_length_validation_error_message(
                    field_name, None, max_length)}
        else:
            error_msg = {
                "message": get_length_validation_error_message(
                    field_name, min_length, max_length)}
        return False, error_msg
    else:
        return True, {}


def get_length_validation_error_message(field_name, min_length, max_length):
    if min_length is None:
        return f"The {field_name} field has to be shorter than " \
               f"{max_length + 1} characters."
    else:
        return f"The {field_name} field has to be longer than " \
               f"{min_length - 1} characters and shorter than " \
               f"{max_length + 1} characters."


def get_stripped_string(string_with_whitespaces):
    return ''.join(string_with_whitespaces.split())
