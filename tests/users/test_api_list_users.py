import unittest
from flask import json
from flask_restplus import marshal

from app import messages
from app.api.models.user import public_user_api_model
from app.api.dao.user import UserDAO
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_utils import get_test_request_header
from tests.test_data import user1, user2
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel

class TestListUsersApi(BaseTestCase):
    def setUp(self):
        super(TestListUsersApi, self).setUp()

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

    def test_list_users_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.get('/users', follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.verified_user.id)
        if not isinstance(current_relation_response,MentorshipRelationModel):
            if (self.verified_user.need_mentoring or self.verified_user.available_to_mentor):
                self.verified_user.is_available = True

        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.other_user.id)
        if not isinstance(current_relation_response,MentorshipRelationModel):
            if (self.other_user.need_mentoring or self.other_user.available_to_mentor):
                self.other_user.is_available = True

        expected_response = [marshal(self.verified_user, public_user_api_model), marshal(self.other_user, public_user_api_model)]
        actual_response = self.client.get('/users', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_verified_users(self):
        auth_header = get_test_request_header(self.admin_user.id)
        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.verified_user.id)
        if not isinstance(current_relation_response,MentorshipRelationModel):
            if (self.verified_user.need_mentoring or self.verified_user.available_to_mentor):
                self.verified_user.is_available = True

        expected_response = [marshal(self.verified_user, public_user_api_model)]
        actual_response = self.client.get('/users/verified', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    """
    admin_user and verified_user are available for mentorship
    """
    def test_list_users_api_is_available_true(self):
        self.verified_user.need_mentoring = True
        self.verified_user.available_to_mentor = True
        db.session.add(self.verified_user)
        self.admin_user.need_mentoring = True
        self.admin_user.available_to_mentor = True
        db.session.add(self.admin_user)
        db.session.commit()
        auth_header = get_test_request_header(self.admin_user.id)

        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.verified_user.id)
        if not isinstance(current_relation_response, MentorshipRelationModel):
            if (self.verified_user.need_mentoring or self.verified_user.available_to_mentor):
                self.verified_user.is_available = True

        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.other_user.id)
        if not isinstance(current_relation_response, MentorshipRelationModel):
            if (self.other_user.need_mentoring or self.other_user.available_to_mentor):
                self.other_user.is_available = True

        expected_response = [marshal(self.verified_user, public_user_api_model), marshal(self.other_user, public_user_api_model)]
        actual_response = self.client.get('/users', follow_redirects=True, headers=auth_header)
        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        #Check status with POST /mentorship_relation/send_request
        send_request_response = self.client.post('/mentorship_relation/send_request',
            follow_redirects = True, headers = auth_header, content_type = 'application/json',
            data = json.dumps(dict(
                mentor_id = self.admin_user.id,
                mentee_id = self.verified_user.id,
                end_date = 1585679400,
                notes = "notes"
            )))
        self.assertEqual(messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY,
            json.loads(send_request_response.data))

    """
    admin_user is available for mentorship, verified_user is not
    """
    def test_list_users_api_is_available_false(self):
        self.verified_user.need_mentoring = False
        self.verified_user.available_to_mentor = False
        db.session.add(self.verified_user)
        self.admin_user.need_mentoring = True
        self.admin_user.available_to_mentor = True
        db.session.add(self.admin_user)
        db.session.commit()
        auth_header = get_test_request_header(self.admin_user.id)

        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.verified_user.id)
        if not isinstance(current_relation_response, MentorshipRelationModel):
            if (self.verified_user.need_mentoring or self.verified_user.available_to_mentor):
                self.verified_user.is_available = True

        current_relation_response = MentorshipRelationDAO.list_current_mentorship_relation(
            self.other_user.id)
        if not isinstance(current_relation_response, MentorshipRelationModel):
            if (self.other_user.need_mentoring or self.other_user.available_to_mentor):
                self.other_user.is_available = True

        expected_response = [marshal(self.verified_user, public_user_api_model), marshal(self.other_user, public_user_api_model)]
        actual_response = self.client.get('/users', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        #Check status with POST /mentorship_relation/send_request
        send_request_response = self.client.post('/mentorship_relation/send_request',
            follow_redirects = True, headers = auth_header, content_type = 'application/json',
            data=json.dumps(dict(
                mentor_id = self.admin_user.id,
                mentee_id = self.verified_user.id,
                end_date = 1585679400,
                notes = "notes"
            )))
        self.assertNotEqual(messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY,
            json.loads(send_request_response.data))

if __name__ == "__main__":
    unittest.main()
