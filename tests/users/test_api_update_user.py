import unittest
from flask import json
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_data import user1
from tests.test_utils import get_test_request_header


class TestUpdateUserApi(BaseTestCase):

    def test_update_user_api_resource_non_auth(self):
        expected_response = {'message': 'The authorization token is missing!'}
        actual_response = self.client.put('/user', follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_update_username_already_taken(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.commit()

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = {"message": "That username is already taken by another user."}
        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(username=self.admin_user.username)),
                                          content_type='application/json')

        self.assertEqual(400, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_update_username_not_taken(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.commit()

        user1_new_username = "new_username"
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = {"message": "User was updated successfully"}
        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(username=user1_new_username)),
                                          content_type='application/json')

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))
        self.assertEqual(user1_new_username, self.first_user.username)


if __name__ == "__main__":
    unittest.main()
