import datetime
import json
import time
import unittest

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header

class TestAcceptMentorshipRequestApi(MentorshipRelationBaseTestCase):

    def setUp(self):
        super(TestAcceptMentorshipRequestApi, self).setUp()

        self.notes_example = 'description of a good mentorship relation'

        self.now_datetime = datetime.datetime.now()
        self.end_date_example = self.now_datetime + datetime.timedelta(weeks=5)

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
            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                                       headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertDictEqual(messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY,
                                 json.loads(response.data))

    def test_accept_mentorship_request_token_missing(self):
        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
        with self.client:
            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                                       headers=None)

            self.assertEqual(401, response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
            self.assertDictEqual(messages.AUTHORISATION_TOKEN_IS_MISSING,
                                 json.loads(response.data))

    def test_accept_mentorship_request_token_expired(self):
        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
        with self.client:
            auth_header = get_test_request_header(self.first_user.id,
                                                  token_expiration_delta=datetime.timedelta(milliseconds=1))

            time.sleep(1)

            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                                       headers=auth_header)

            self.assertEqual(401, response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
            self.assertDictEqual(messages.TOKEN_HAS_EXPIRED,
                                 json.loads(response.data))

    def test_accept_mentorship_request_user_already_in_relation(self):
        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)

        self.mentorship_relation_2 = MentorshipRelationModel(
            action_user_id=self.second_user.id,
            mentor_user=self.admin_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

        db.session.add(self.mentorship_relation_2)
        db.session.commit()

        with self.client:
            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation_2.id}/accept",
                                       headers=get_test_request_header(self.admin_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation_2.state)
            self.assertDictEqual(messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY,
                                 json.loads(response.data))

            # Main part of the test - user 2 tries to accept relation request again
            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                                       headers=get_test_request_header(self.second_user.id))

            self.assertEqual(400, response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
            self.assertDictEqual(messages.USER_IS_INVOLVED_IN_A_MENTORSHIP_RELATION,
                                 json.loads(response.data))

    def test_accept_not_valid_user(self):
        """Assuming User1 sent request X to User2, User1 accepts this request"""

        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
        with self.client:
            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                                       headers=get_test_request_header(self.first_user.id))

            self.assertEqual(400, response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
            self.assertDictEqual(messages.CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER,
                                 json.loads(response.data))

    def test_accept_user_not_involved_in_relation(self):
        """AdminUser accepts a mentorship relation which the AdminUser is not involved with"""

        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
        with self.client:
            response = self.client.put(f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                                       headers=get_test_request_header(self.admin_user.id))

            self.assertEqual(400, response.status_code)
            self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
            self.assertDictEqual(messages.CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION,
                                 json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
