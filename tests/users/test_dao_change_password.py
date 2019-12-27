import unittest
from app.api.dao.user import UserDAO
from app import messages
from tests.base_test_case import BaseTestCase
from tests.test_data import test_admin_user

class TestChangePasswordDao(BaseTestCase):

    def test_change_password_dao(self):
        expected_response = messages.PASSWORD_SUCCESSFULLY_UPDATED
        actual_response = UserDAO.change_password(
            user_id = self.admin_user.id,
            data = {
                "current_password": test_admin_user["password"],
                "new_password": "newpassword"
            }
        )
        self.assertEqual(201, actual_response[1])
        self.assertDictEqual(expected_response, actual_response[0])

    def test_change_password_duplicate_dao(self):
        expected_response = messages.DUPLICATE_PASSWORD
        actual_response = UserDAO.change_password(
            user_id = self.admin_user.id,
            data = {
                "current_password": test_admin_user["password"],
                "new_password": test_admin_user["password"]
            }
        )
        self.assertEqual(400, actual_response[1])
        self.assertDictEqual(expected_response, actual_response[0])

if __name__ == '__main__':
    unittest.main()
