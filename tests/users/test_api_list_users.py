import unittest
from flask import json
from flask_restplus import marshal
from app.api.models.user import public_user_api_model
from tests.base_test_case import BaseTestCase
from tests.test_utils import get_test_request_header


class TestListUsersApi(BaseTestCase):

    def test_list_users_api_resource_non_auth(self):
        expected_response = {'message': 'The authorization token is missing!'}
        actual_response = self.client.get('/users', follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = [marshal(self.admin_user, public_user_api_model)]
        actual_response = self.client.get('/users', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
