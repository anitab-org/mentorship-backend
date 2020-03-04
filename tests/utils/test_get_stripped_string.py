import unittest
from app.utils.validation_utils import get_stripped_string


class TestGetStrippedStringFunction(unittest.TestCase):
    def test_empty_string(self):
        test_string = ""
        expected_result = ""
        actual_result = get_stripped_string(test_string)
        self.assertEqual(expected_result, actual_result)

    def test_with_no_spaces_string(self):
        test_string = "asdf"
        expected_result = test_string
        actual_result = get_stripped_string(test_string)
        self.assertEqual(expected_result, actual_result)

    def test_with_spaces_string(self):
        test_string = " a s d f "
        expected_result = "asdf"
        actual_result = get_stripped_string(test_string)
        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
