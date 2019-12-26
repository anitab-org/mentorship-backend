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
from app.database.models.user import UserModel
from tests.test_data import user3


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
        
        #creates a third user not involved in the relationship
        self.third_user = UserModel(
            name=user3['name'],
            email=user3['email'],
            username=user3['username'],
            password=user3['password'],
            terms_and_conditions_checked=user3['terms_and_conditions_checked']
        )
        self.third_user.is_email_verified = True
        
        db.session.add(self.third_user)
        db.session.commit()
    #cancellation successful

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
    
    #missing authorisation token
    
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
            
    #expired authorisation token
            
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
        
    #not involved in mentorship    
        
    def test__user_not_in_mentorship(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.third_user.id))
            
            self.assertEqual(400, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.CANT_CANCEL_UNINVOLVED_REQUEST, json.loads(response.data))
            

if __name__ == "__main__":
    unittest.main()