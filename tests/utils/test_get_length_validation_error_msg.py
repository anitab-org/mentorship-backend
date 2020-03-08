import unittest
from app.utils.validation_utils import get_length_validation_error_message


class TestGetLengthValidationErrorMessageFunction(unittest.TestCase):
    def test_error_message_with_no_min_length(self):
        field_length = 3
        max_length = field_length + 1
        field_name = "field"

        expected_result = (
            "The {field_name} field has to be shorter "
            "than {max_limit} characters.".format(
                field_name=field_name, max_limit=max_length + 1
            )
        )
        actual_result = get_length_validation_error_message(
            field_name, None, max_length
        )

        self.assertEqual(expected_result, actual_result)

    def test_error_message_with_min_length(self):
        field_length = 3
        min_length = field_length - 1
        max_length = field_length + 1
        field_name = "field"

        expected_result = (
            "The {field_name} field has to be longer than {min_limit} "
            "characters and shorter than {max_limit} characters.".format(
                field_name=field_name,
                min_limit=min_length - 1,
                max_limit=max_length + 1,
            )
        )
        actual_result = get_length_validation_error_message(
            field_name, min_length, max_length
        )

        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()
