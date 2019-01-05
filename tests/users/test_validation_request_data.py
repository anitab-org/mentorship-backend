import unittest
from random import SystemRandom
from string import ascii_lowercase

from app.api.validations.user import (
    validate_user_registration_request_data,
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    validate_new_password,
)
from app.utils.validation_utils import get_length_validation_error_message
from tests.test_data import USER1


class TestUserApiRequestDataValidation(unittest.TestCase):
    def test_user_registration_valid_request_data(self):
        expected_result = {}
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_name_field(self):
        expected_result = {"message": "Name field is missing."}
        request_body = dict(
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_username_field(self):
        expected_result = {"message": "Username field is missing."}
        request_body = dict(
            name=USER1["name"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_password_field(self):
        expected_result = {"message": "Password field is missing."}
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_email_field(self):
        expected_result = {"message": "Email field is missing."}
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_missing_terms_and_conditions_field(
            self):
        expected_result = {"message": "Terms and conditions field is missing."}
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_with_terms_unchecked(self):
        expected_result = {"message": "Terms and conditions are not checked."}
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=False,
        )
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_name_inferior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_name = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(NAME_MIN_LENGTH - 1)
        )
        request_body = dict(
            name=random_generated_name,
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "name", NAME_MIN_LENGTH, NAME_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_name_superior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_name = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(NAME_MAX_LENGTH + 1)
        )
        request_body = dict(
            name=random_generated_name,
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "name", NAME_MIN_LENGTH, NAME_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_username_inferior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_username = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(USERNAME_MIN_LENGTH - 1)
        )
        request_body = dict(
            name=USER1["name"],
            username=random_generated_username,
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "username", USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_username_superior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_username = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(USERNAME_MAX_LENGTH + 1)
        )
        request_body = dict(
            name=USER1["name"],
            username=random_generated_username,
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "username", USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_password_inferior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_password = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(PASSWORD_MIN_LENGTH - 1)
        )
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            password=random_generated_password,
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_password_superior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_password = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(PASSWORD_MAX_LENGTH + 1)
        )
        request_body = dict(
            name=USER1["name"],
            username=USER1["username"],
            password=random_generated_password,
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_registration_request_data_name_with_just_spaces_good_length(
            self):
        request_body = dict(
            name=" " * (NAME_MIN_LENGTH + 1),
            username=USER1["username"],
            password=USER1["password"],
            email=USER1["email"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "name", NAME_MIN_LENGTH, NAME_MAX_LENGTH
            )
        }
        actual_result = validate_user_registration_request_data(request_body)

        self.assertEqual(expected_result, actual_result)

    def test_user_password_change_request_password_inferior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_password = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(PASSWORD_MIN_LENGTH - 1)
        )
        data = dict(
            new_password=random_generated_password,
            current_password=random_generated_password,
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "new_password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
            )
        }
        actual_result = validate_new_password(data)

        self.assertEqual(expected_result, actual_result)

    def test_user_password_change_request_password_superior_to_limit(self):
        secure_random = SystemRandom()
        random_generated_password = "".join(
            secure_random.choice(ascii_lowercase)
            for x in range(PASSWORD_MAX_LENGTH + 1)
        )
        data = dict(
            new_password=random_generated_password,
            current_password=random_generated_password,
        )

        expected_result = {
            "message": get_length_validation_error_message(
                "new_password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
            )
        }
        actual_result = validate_new_password(data)

        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
