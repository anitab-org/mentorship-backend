import re

email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_regex = r"(^[a-zA-Z0-9]+$)"


def is_email_valid(email):
    return re.match(email_regex, email)


def is_username_valid(username):
    return re.match(username_regex, username)
