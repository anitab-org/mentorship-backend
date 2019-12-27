import unittest

from flask import json

from app import messages
from tests.base_test_case import BaseTestCase
from tests.test_data import test_admin_user
from tests.test_utils import get_test_request_header

class TestChangePasswordApi(BaseTestCase):

    def test_change_password_api(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.PASSWORD_SUCCESSFULLY_UPDATED
        actual_response = self.client.put('/user/change_password', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(
                                                current_password=test_admin_user["password"],
                                                new_password="newpassword"
                                              )),
                                          content_type='application/json')

        self.assertEqual(201, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_change_password_duplicate_api(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.DUPLICATE_PASSWORD
        actual_response = self.client.put('/user/change_password', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(
                                                current_password=test_admin_user["password"],
                                                new_password=test_admin_user["password"]
                                              )),
                                          content_type='application/json')

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

if __name__ == "__main__":
    unittest.main()
