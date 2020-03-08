import unittest
from app.utils.validation_utils import is_username_valid


class TestUsernameValidation(unittest.TestCase):
    def test_empty_username(self):
        username = ""
        is_valid = is_username_valid(username)
        self.assertFalse(is_valid)

    def test_username_with_just_spaces(self):
        username = "   "
        is_valid = is_username_valid(username)
        self.assertFalse(is_valid)

    def test_valid_username_without_underscore(self):
        username = "validusername"
        is_valid = is_username_valid(username)
        self.assertTrue(is_valid)

    def test_valid_username_with_numbers(self):
        username = "validusername123"
        is_valid = is_username_valid(username)
        self.assertTrue(is_valid)

    def test_invalid_username_with_underscore(self):
        username = "valid_username"
        is_valid = is_username_valid(username)
        self.assertTrue(is_valid)

    def test_invalid_username_with_spaces(self):
        username = "username with spaces"
        is_valid = is_username_valid(username)
        self.assertFalse(is_valid)

    def test_invalid_username_with_slash(self):
        username = "valid-username"
        is_valid = is_username_valid(username)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
