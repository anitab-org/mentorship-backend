import unittest

from flask import json

from app import messages
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase

from app.database.models.user import UserModel
from app.api.dao.user import UserDAO
from http import HTTPStatus

class TestSocialSignInAPI(BaseTestCase):
    def test_create_new_user_for_social_sign_in(self):
        with self.client:
            response = self.client.post(
                "/apple/auth/callback",
                data=json.dumps(
                    dict(id_token="test_token", name="test_name", email="test_email")
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            self.assertIsNotNone(response.json.get("access_token"))
            self.assertIsNotNone(response.json.get("access_expiry"))
            self.assertIsNotNone(response.json.get("refresh_token"))
            self.assertIsNotNone(response.json.get("refresh_expiry"))
    
    def test_another_user_for_id_token_exists(self):
        # Create user (token = test_token)
        user_data = dict(
            id_token="test_token",
            name="test_name",
            email="test_email"
        )
        social_sign_in_type = "test_type"
        UserDAO.create_user_using_social_login(user_data, social_sign_in_type)
        
        # Use API. Keep token same, other information different
        with self.client:
            response = self.client.post(
                "/apple/auth/callback",
                data=json.dumps(
                    dict(id_token="test_token", name="test_name_2", email="test_email_2")
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            self.assertIsNone(response.json.get("access_token"))
            self.assertIsNone(response.json.get("access_expiry"))
            self.assertIsNone(response.json.get("refresh_token"))
            self.assertIsNone(response.json.get("refresh_expiry"))
            self.assertTrue({"message": response.json.get("message")} == messages.ANOTHER_USER_FOR_ID_TOKEN_EXISTS)

    def test_user_email_signed_in_with_different_provider(self):
        # Create user (email = test_email)
        user_data = dict(
            id_token="test_token",
            name="test_name",
            email="test_email"
        )
        social_sign_in_type = "google"
        UserDAO.create_user_using_social_login(user_data, social_sign_in_type)

        # Use API. Keep email same, provider different (apple)
        with self.client:
            response = self.client.post(
                "/apple/auth/callback",
                data=json.dumps(
                    dict(id_token="test_token_2", name="test_name_2", email="test_email")
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            self.assertIsNone(response.json.get("access_token"))
            self.assertIsNone(response.json.get("access_expiry"))
            self.assertIsNone(response.json.get("refresh_token"))
            self.assertIsNone(response.json.get("refresh_expiry"))
            self.assertTrue({"message": response.json.get("message")} == messages.USER_NOT_SIGNED_IN_WITH_THIS_PROVIDER)

    def test_google_auth_token_not_verified(self):
        with self.client:
            response = self.client.post(
                "/google/auth/callback",
                data=json.dumps(
                    dict(id_token="invalid_token", name="test_name", email="test_email")
                ),
                follow_redirects=True,
                content_type="application/json",
            )
            self.assertIsNone(response.json.get("access_token"))
            self.assertIsNone(response.json.get("access_expiry"))
            self.assertIsNone(response.json.get("refresh_token"))
            self.assertIsNone(response.json.get("refresh_expiry"))
            self.assertTrue({"message": response.json.get("message")} == messages.GOOGLE_AUTH_TOKEN_VERIFICATION_FAILED)

if __name__ == "__main__":
    unittest.main()