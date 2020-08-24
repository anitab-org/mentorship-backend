import unittest

from app.api.dao.user import UserDAO
from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel


class TestSocialSignIn(BaseTestCase):
    def test_create_user_using_social_sign_in(self):
        user_data = dict(
            id_token="test_token",
            name="test_name",
            email="test_email"
        )
        social_sign_in_type = "test_type"

        # Call create user using social sign in method
        UserDAO.create_user_using_social_login(user_data, social_sign_in_type)

        # Test the user created
        user = UserDAO.get_user_by_email("test_email")
        self.assertEqual(user.name, user_data["name"])
        self.assertTrue(user.username is None)
        self.assertTrue(user.password_hash is None)

        # Test the social sign in details of the user created
        social_sign_in_details = UserDAO.get_social_sign_in_details(user.id, "test_type")
        self.assertEqual(social_sign_in_details.id_token, user_data["id_token"])
        self.assertEqual(social_sign_in_details.associated_email, user_data["email"])
        self.assertEqual(social_sign_in_details.full_name, user_data["name"])

if __name__ == "__main__":
    unittest.main()