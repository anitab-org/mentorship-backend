import unittest

from flask import json

from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel


# Testing User API resources
#
# TODO tests:
#     - authenticate when User table does not exist
#     - Users GET/POST/PUT/DELETE
#     - Check admin and non admin actions
from tests.test_data import user1


class TestUserApi(BaseTestCase):

    # Tests

    def test_user_registration(self):
        # Ensure user registration behaves correctly.

        with self.client:
            response = self.client.post('/register', data=json.dumps(dict(
                name=user1['name'],
                username=user1['username'],
                password=user1['password'],
                email=user1['email'],
                terms_and_conditions_checked=user1['terms_and_conditions_checked']
            )), follow_redirects=True, content_type='application/json')

            # print(response)
            # print(response.data)
            user = UserModel.query.filter_by(email=user1['email']).first()
            # print(user.json())
            if user is None:
                self.fail('POST /register failed to register Testing User! with error code = %d' % response.status_code)
            else:
                self.assertEqual(user1['name'], user.name)
                self.assertEqual(user1['username'], user.username)
                self.assertEqual(user1['email'], user.email)
                self.assertEqual(user1['terms_and_conditions_checked'], user.terms_and_conditions_checked)
                self.assertFalse(user.is_admin)

    def test_list_users_api_resource(self):

        response = self.client.get('/users', follow_redirects=True)
        self.assertTrue(response.status_code == 201)
        # print(response)
        # print(response.data)



if __name__ == "__main__":
    unittest.main()
