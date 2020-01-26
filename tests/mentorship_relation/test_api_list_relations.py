import json
import unittest

from flask_restplus import marshal

from app.api.models.mentorship_relation import mentorship_request_response_body
from app.database.models.tasks_list import TasksListModel
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestListMentorshipRelationsApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestListMentorshipRelationsApi, self).setUp()
        super(TestListMentorshipRelationsApi,
              self).create_mentorship_relations()

        # create new mentorship relation

        self.admin_only_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.admin_user.id,
            mentor_user=self.admin_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

    def test_list_past_mentorship_relations(self):
        with self.client:
            response = self.client.get('/mentorship_relations/past',
                                       headers=get_test_request_header(
                                           self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual([marshal(self.past_mentorship_relation,
                                      mentorship_request_response_body)],
                             json.loads(response.data))

    def test_list_pending_mentorship_relations(self):
        with self.client:
            response = self.client.get('/mentorship_relations/pending',
                                       headers=get_test_request_header(
                                           self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual([marshal(self.mentorship_relation,
                                      mentorship_request_response_body),
                              marshal(self.future_pending_mentorship_relation,
                                      mentorship_request_response_body)],
                             json.loads(response.data))

    def test_list_current_mentorship_relation(self):
        with self.client:
            response = self.client.get('/mentorship_relations/current',
                                       headers=get_test_request_header(
                                           self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(marshal(self.future_accepted_mentorship_relation,
                                     mentorship_request_response_body),
                             json.loads(response.data))

    def test_list_all_mentorship_relations(self):
        with self.client:
            response = self.client.get('/mentorship_relations',
                                       headers=get_test_request_header(
                                           self.admin_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual([marshal(self.admin_only_mentorship_relation,
                                      mentorship_request_response_body)],
                             json.loads(response.data))

    def test_list_current_mentorship_relation_sent_by_current_user(self):
        with self.client:
            response = self.client.get('/mentorship_relations/current',
                                       headers=get_test_request_header(
                                           self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(marshal(self.future_accepted_mentorship_relation,
                                     mentorship_request_response_body),
                             json.loads(response.data))
            self.assertFalse(
                self.future_accepted_mentorship_relation.sent_by_me)

    def test_list_current_mentorship_relation_sent_by_another_user(self):
        with self.client:
            response = self.client.get('/mentorship_relations/current',
                                       headers=get_test_request_header(
                                           self.first_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(marshal(self.future_accepted_mentorship_relation,
                                     mentorship_request_response_body),
                             json.loads(response.data))
            self.assertTrue(self.future_accepted_mentorship_relation.sent_by_me)


if __name__ == "__main__":
    unittest.main()
