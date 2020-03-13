import unittest
from app.utils.validation_utils import is_email_valid


class TestEmailValidation(unittest.TestCase):
    def test_empty_email(self):
        email = ""
        is_valid = is_email_valid(email)
        self.assertFalse(is_valid)

    def test_valid_email(self):
        email = "valid@email.com"
        is_valid = is_email_valid(email)
        self.assertTrue(is_valid)

    def test_invalid_email_with_no_dot_after_at(self):
        email = "invalid@emailcom"
        is_valid = is_email_valid(email)
        self.assertFalse(is_valid)

    def test_invalid_email_with_no_at(self):
        email = "invalidemail.com"
        is_valid = is_email_valid(email)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
