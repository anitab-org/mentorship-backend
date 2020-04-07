import unittest
from app.utils.validation_utils import (
    validate_length,
    get_length_validation_error_message,
)


class TestValidateLengthFunction(unittest.TestCase):
    def test_valid_length_with_min_and_max(self):
        field_length = 3

        expected_result = (True, {})
        actual_result = validate_length(
            field_length, field_length - 1, field_length + 1, "field"
        )

        self.assertEqual(expected_result, actual_result)

    def test_valid_length_without_min(self):
        field_length = 3

        expected_result = (True, {})
        actual_result = validate_length(field_length, 0, field_length + 1, "field")

        self.assertEqual(expected_result, actual_result)

    def test_invalid_length_without_min(self):
        field_length = 3
        min_length = 0
        max_length = field_length - 1
        field_name = "field"

        expected_error_msg = {
            "message": get_length_validation_error_message(field_name, None, max_length)
        }
        expected_result = (False, expected_error_msg)
        actual_result = validate_length(
            field_length, min_length, max_length, field_name
        )

        self.assertEqual(expected_result, actual_result)

    def test_invalid_superior_length(self):
        field_length = 3
        min_length = field_length - 1
        max_length = field_length - 1
        field_name = "field"

        expected_error_msg = {
            "message": get_length_validation_error_message(
                field_name, min_length, max_length
            )
        }
        expected_result = (False, expected_error_msg)
        actual_result = validate_length(
            field_length, min_length, max_length, field_name
        )

        self.assertEqual(expected_result, actual_result)

    def test_invalid_inferior_length(self):
        field_length = 3
        min_length = field_length + 1
        max_length = field_length + 1
        field_name = "field"

        expected_error_msg = {
            "message": get_length_validation_error_message(
                field_name, min_length, max_length
            )
        }
        expected_result = (False, expected_error_msg)
        actual_result = validate_length(
            field_length, min_length, max_length, field_name
        )

        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
