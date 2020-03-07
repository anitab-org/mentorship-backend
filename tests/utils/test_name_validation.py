import unittest
from app.utils.validation_utils import is_name_valid


class TestNameValidation(unittest.TestCase):
    def test_empty_name(self):
        name = ""
        is_valid = is_name_valid(name)
        self.assertFalse(is_valid)

    def test_valid_name(self):
        name = "valid"
        is_valid = is_name_valid(name)
        self.assertTrue(is_valid)

    def test_valid_name_with_dash(self):
        name = "valid-name"
        is_valid = is_name_valid(name)
        self.assertTrue(is_valid)

    def test_invalid_name_with_special_characters(self):
        name = "invalidname@123"
        is_valid = is_name_valid(name)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
