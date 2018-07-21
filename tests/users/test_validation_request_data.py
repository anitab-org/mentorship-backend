import unittest
from random import SystemRandom
from string import ascii_lowercase

from app.api.validations.user import validate_user_registration_request_data, NAME_MIN_LENGTH, NAME_MAX_LENGTH, \
    USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH, validate_new_password
from tests.test_data import user1


class TestUserApiRequestDataValidation(unittest.TestCase):

    def test_user_registration_valid_request_data(self):
        expected_result = {}
        request_body = dict(
                name=user1['name'],
                username=user1['username'],
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_name_field(self):
        expected_result = {"message": "Name field is missing."}
        request_body = dict(
                username=user1['username'],
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_username_field(self):
        expected_result = {"message": "Username field is missing."}
        request_body = dict(
            name=user1['name'],
            password=user1['password'],
            email=user1['email'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_password_field(self):
        expected_result = {"message": "Password field is missing."}
        request_body = dict(
            name=user1['name'],
            username=user1['username'],
            email=user1['email'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_email_field(self):
        expected_result = {"message": "Email field is missing."}
        request_body = dict(
            name=user1['name'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_terms_and_conditions_field(self):
        expected_result = {"message": "Terms and conditions field is missing."}
        request_body = dict(
            name=user1['name'],
            username=user1['username'],
            password=user1['password'],
            email=user1['email'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_with_terms_unchecked(self):
        expected_result = {"message": "Terms and conditions are not checked."}
        request_body = dict(
                name=user1['name'],
                username=user1['username'],
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=False)
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_name_inferior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The name field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=NAME_MIN_LENGTH-1,
                                                                                        max_limit=NAME_MAX_LENGTH+1)}
        random_generated_name = "".join(secure_random.choice(ascii_lowercase) for x in range(NAME_MIN_LENGTH-1))
        request_body = dict(
                name=random_generated_name,
                username=user1['username'],
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_name_superior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The name field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=NAME_MIN_LENGTH-1,
                                                                                        max_limit=NAME_MAX_LENGTH+1)}
        random_generated_name = "".join(secure_random.choice(ascii_lowercase) for x in range(NAME_MAX_LENGTH+1))
        request_body = dict(
                name=random_generated_name,
                username=user1['username'],
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_username_inferior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The username field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=USERNAME_MIN_LENGTH-1,
                                                                                        max_limit=USERNAME_MAX_LENGTH+1)}
        random_generated_username = "".join(secure_random.choice(ascii_lowercase) for x in range(USERNAME_MIN_LENGTH-1))
        request_body = dict(
                name=user1['name'],
                username=random_generated_username,
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_username_superior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The username field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=USERNAME_MIN_LENGTH-1,
                                                                                        max_limit=USERNAME_MAX_LENGTH+1)}
        random_generated_username = "".join(secure_random.choice(ascii_lowercase) for x in range(USERNAME_MAX_LENGTH+1))
        request_body = dict(
                name=user1['name'],
                username=random_generated_username,
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_password_inferior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The password field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=PASSWORD_MIN_LENGTH-1,
                                                                                        max_limit=PASSWORD_MAX_LENGTH+1)}
        random_generated_password = "".join(secure_random.choice(ascii_lowercase) for x in range(PASSWORD_MIN_LENGTH-1))
        request_body = dict(
                name=user1['name'],
                username=user1['username'],
                password=random_generated_password,
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_password_superior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The password field has to longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=PASSWORD_MIN_LENGTH-1,
                                                                                        max_limit=PASSWORD_MAX_LENGTH+1)}
        random_generated_password = "".join(secure_random.choice(ascii_lowercase) for x in range(PASSWORD_MAX_LENGTH+1))
        request_body = dict(
                name=user1['name'],
                username=user1['username'],
                password=random_generated_password,
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked'])
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_password_change_request_password_inferior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The password field has to be longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=PASSWORD_MIN_LENGTH-1,
                                                                                        max_limit=PASSWORD_MAX_LENGTH+1)}
        random_generated_password = "".join(secure_random.choice(ascii_lowercase) for x in range(PASSWORD_MIN_LENGTH-1))
        data = dict(new_password=random_generated_password, current_password=random_generated_password)
        actual_result = validate_new_password(data)
        self.assertEqual(expected_result, actual_result)

    def test_user_password_change_request_password_superior_to_limit(self):
        secure_random = SystemRandom()
        expected_result = {"message": "The password field has to be longer than {min_limit} "
                           "characters and shorter than {max_limit} characters.".format(min_limit=PASSWORD_MIN_LENGTH-1,
                                                                                        max_limit=PASSWORD_MAX_LENGTH+1)}
        random_generated_password = "".join(secure_random.choice(ascii_lowercase) for x in range(PASSWORD_MAX_LENGTH+1))
        data = dict(new_password=random_generated_password, current_password=random_generated_password)
        actual_result = validate_new_password(data)
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
