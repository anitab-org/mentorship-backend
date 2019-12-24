import json
import unittest
from datetime import datetime, timedelta

from app import messages
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header

class TestAcceptMentorshipRequestApi(MentorshipRelationBaseTestCase):

    def setUp(self):
        super(TestAcceptMentorshipRequestApi, self).setUp()

        self.notes_example = 'description of a good mentorship relation'

        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test_accept_mentorship_request(self):
        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY,
                             json.loads(response.data))

    # This case tests the accept request api.
    # If the receiver tries to accepts a request while he is in another mentorship relation, then
    # '400:Bad Request' error would be given displaying the message that 'You are currently involved in a mentorship relation'.
    def test_accept_mentorship_request_receiver_involved_in_other_relation(self):
        if (not(self.second_user.current_mentorship_role is None)):
            self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
            auth_header=get_test_request_header(self.second_user.id)
            expected_response=messages.USER_IS_INVOLVED_IN_A_MENTORSHIP_RELATION
            actual_response=self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                                            headers=auth_header)

            self.assertEqual(400,actual_response.status_code)
            self.assertDictEqual(expected_response,json.loads(actual_response.data))
            self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.id)

    # This case tests the accept request api.
    # If a user tries to accepts a request where he is not involved, then
    # '400:Bad Request' error would be given displaying the message that 'You cannot accept a mentorship relation where you are not involved.'.
    def test_accept_mentorship_request_acceptor_not_involved_in_relation(self):
        if (self.mentorship_relation.mentor_id != self.first_user.id and self.mentorship_relation.mentee_id != self.first_user.id):
            self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
            auth_header=get_test_request_header(self.first_user.id)
            expected_response=messages.CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION
            actual_response = self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                                            headers=auth_header)

            self.assertEqual(400, actual_response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
            self.assertDictEqual(expected_response, json.loads(actual_response.data))

    # This case tests the accept request api.
    # If a user tries to accepts a request sent by him, then
    # '400:Bad Request' error would be given displaying the message that 'You cannot accept a mentorship request sent by yourself.'.
    def test_accept_mentorship_request_by_sender(self):
        if (self.mentorship_relation.action_user_id == self.first_user.id):
            self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
            auth_header=get_test_request_header(self.first_user.id)
            expected_response=messages.CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER
            actual_response = self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                                            headers=auth_header)

            self.assertEqual(400, actual_response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
            self.assertDictEqual(expected_response, json.loads(actual_response.data))

    # This case tests the accept request api with authentication token missing.
    # If a user tries to accepts a request without an authentication token, then
    # '401:Unauthorised' error would be given displaying the message that 'The authorization token is missing!.'.
    def test_accept_mentorship_request_without_auth_token(self):
        self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
        expected_response=messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    # This case tests the accept request api with an expired authentication token.
    # If a user tries to accepts a request with an expired authentication token, then
    # '401:Unauthorised' error would be given displaying the message that 'The token has expired! Please, login again or refresh it.'.
    def test_accept_mentorship_request_with_token_expired(self):
        self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
        auth_header=get_test_request_header(self.second_user.id,token_expiration_delta=timedelta(minutes=-5))
        expected_response=messages.TOKEN_HAS_EXPIRED
        actual_response = self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                                            headers=auth_header)

        self.assertEqual(401, actual_response.status_code)
        self.assertEqual(MentorshipRelationState.PENDING,self.mentorship_relation.state)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))



if __name__ == "__main__":
    unittest.main()
