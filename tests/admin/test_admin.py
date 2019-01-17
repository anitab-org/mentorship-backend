import unittest
from flask import json
from flask_restplus import marshal
from app.api.models.admin import add_models_to_namespace
from app.api.models.user import public_user_api_model
from app.database.models.user import UserModel
from app.api.dao import admin
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_utils import get_test_request_header
from tests.test_data import user1, user2, test_admin_user


class TestListAdminsApi(BaseTestCase):
    def setUp(self):
        super(TestListAdminsApi, self).setUp()

        self.verified_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.other_user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )

        self.verified_user.is_email_verified = True
        db.session.add(self.verified_user)
        db.session.add(self.other_user)
        db.session.commit()

    def test_revoke_admin_admin(self):
        if (self.verified_user.is_admin and self.other_user.is_admin):
            expected_response = {'message': 'User admin status was revoked.'}
            actual_response = self.client.get('/admin/remove', follow_redirects=True)

            self.assertEqual(200, actual_response.status_code)
            self.assertEqual(expected_response, json.loads(actual_response.data))


    def test_revoke_user(self):
        if(self.verified_user.is_admin and self.other_user.is_admin == 0):
            expected_response = {'message': 'User is not an Admin.'}
            actual_response = self.client.post('/admin/remove', follow_redirects=True)

            self.assertEqual(400, actual_response.status_code)
            self.assertEqual(expected_response, json.loads(actual_response.data))


    # def test_revoke_non_user(self):
    #     if(self.other_user.):
    #     expected_response = {'message': 'User does not exist.'}
    #     actual_response = self.client.get('/admin/remove', follow_redirects=True)
    #
    #     self.assertEqual(404, actual_response.status_code)
    #     self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_revoke_self_admin(self):
        if(self.verified_user.is_admin and self.verified_user==self.other_user):
            expected_response = {'message': 'You cannot revoke your admin status.'}
            actual_response = self.client.get('/admin/remove', follow_redirects=True)

            self.assertEqual(403, actual_response.status_code)
            self.assertEqual(expected_response, json.loads(actual_response.data))

# def test_revoke_self_admin(self):
# 	expected_response = {'message': 'You cannot revoke your admin status.'}
# 	actual_response = self.client.get('/admin/remove', follow_redirects=True)

# 	self.assertEqual(403, actual_response.status_code)
# 	self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()