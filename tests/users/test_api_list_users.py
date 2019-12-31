import unittest
from datetime import timedelta, datetime

from flask import json
from flask_restplus import marshal

from app import messages
from app.api.models.user import public_user_api_model
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2, user3
from tests.test_utils import get_test_request_header


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
        self.third_user = UserModel(
            name=user3['name'],
            email=user3['email'],
            username=user3['username'],
            password=user3['password'],
            terms_and_conditions_checked=user3['terms_and_conditions_checked']
        )

        self.verified_user.is_email_verified = True

        # Here, 'third_user' is not available_for_relation (False),
        # as the user is neither available as a mentor nor as a mentee.
        self.verified_user.is_available_for_relation = True
        self.other_user.is_available_for_relation = True
        self.third_user.is_available_for_relation = False

        db.session.add(self.verified_user)
        db.session.add(self.other_user)
        db.session.add(self.third_user)
        db.session.commit()

        # Creating a mentorship relation between the verified_user and the other_user.
        self.create_datetime = datetime.now()
        self.end_datetime = self.create_datetime + timedelta(weeks=4)
        self.notes = "This is a test mentorship relation."

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.verified_user.id,
            mentor_user=self.verified_user,
            mentee_user=self.other_user,
            creation_date=self.create_datetime.timestamp(),
            end_date=self.end_datetime.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes,
            tasks_list=TasksListModel()
        )
        db.session.add(self.mentorship_relation)
        db.session.commit()

        # For precise testing results.
        self.third_user.need_mentoring = True

        # 'verified_user' and 'other_user' are now in a relationship -> not available for new relationship.
        self.verified_user.is_available_for_relation = False
        self.other_user.is_available_for_relation = False
        # 'third_user' is now available for a relation since now,the user is available as a mentee.
        self.third_user.is_available_for_relation = True

    def test_list_users_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.get('/users', follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_auth(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = [marshal(self.verified_user, public_user_api_model), marshal(self.other_user, public_user_api_model), marshal(self.third_user, public_user_api_model)]
        actual_response = self.client.get('/users', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_verified_users(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = [marshal(self.verified_user, public_user_api_model)]
        actual_response = self.client.get('/users/verified', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_users_api_resource_user_available_for_relation(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = [marshal(self.verified_user, public_user_api_model), marshal(self.other_user, public_user_api_model), marshal(self.third_user, public_user_api_model)]
        actual_response = self.client.get('/users', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

if __name__ == "__main__":
    unittest.main()
