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


class TestCancelMentorshipRelationApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestCancelMentorshipRelationApi, self).setUp()

        self.notes_example = 'description of a good mentorship relation'

        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id = self.first_user.id,
            mentor_user = self.first_user,
            mentee_user = self.second_user,
            creation_date = self.now_datetime.timestamp(),
            end_date = self.end_date_example.timestamp(),
            state = MentorshipRelationState.ACCEPTED,
            notes = self.notes_example,
            tasks_list = TasksListModel()
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test__mentor_cancel_mentorship_relation(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.first_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.CANCELLED, self.mentorship_relation.state)
            self.assertDictEqual(messages.MENTORSHIP_RELATION_WAS_CANCELLED_SUCCESSFULLY,
                             json.loads(response.data))

    def test__mentee_cancel_mentorship_relation(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.CANCELLED, self.mentorship_relation.state)
            self.assertDictEqual(messages.MENTORSHIP_RELATION_WAS_CANCELLED_SUCCESSFULLY,
                             json.loads(response.data))
    
    def test__mentor_cancel_token_missing(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id) 
            self.assertEqual(401, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.AUTHORISATION_TOKEN_IS_MISSING, 
                                 json.loads(response.data))
            
    def test__mentee_cancel_token_missing(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id) 
            self.assertEqual(401, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.AUTHORISATION_TOKEN_IS_MISSING, 
                                 json.loads(response.data))
            
    def test__mentor_cancel_token_expired(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        header = get_test_request_header(self.first_user.id, timedelta(days=-1))
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id, 
                                       headers = header)
            self.assertEqual(401, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.TOKEN_HAS_EXPIRED, json.loads(response.data))
            
    def test__mentee_cancel_token_expired(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        header = get_test_request_header(self.second_user.id, timedelta(days=-1))
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id, 
                                       headers = header)
            self.assertEqual(401, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.TOKEN_HAS_EXPIRED, json.loads(response.data))
            


if __name__ == "__main__":
    unittest.main()