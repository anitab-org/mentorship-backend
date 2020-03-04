import json
import unittest
from datetime import datetime, timedelta

from flask_restplus import marshal

from app.api.models.mentorship_relation import mentorship_request_response_body
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestListMentorshipRelationsApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestListMentorshipRelationsApi, self).setUp()

        self.notes_example = "description of a good mentorship relation"
        self.now_datetime = datetime.now()
        self.past_end_date_example = self.now_datetime - timedelta(weeks=5)
        self.future_end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.past_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.past_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        self.future_pending_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        self.future_accepted_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        self.admin_only_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.admin_user.id,
            mentor_user=self.admin_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        db.session.add(self.past_mentorship_relation)
        db.session.add(self.future_pending_mentorship_relation)
        db.session.add(self.future_accepted_mentorship_relation)
        db.session.commit()

    def test_list_past_mentorship_relations(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations/past",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = [
                marshal(self.past_mentorship_relation, mentorship_request_response_body)
            ]

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    def test_list_pending_mentorship_relations(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations/pending",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = [
                marshal(
                    self.future_pending_mentorship_relation,
                    mentorship_request_response_body,
                )
            ]

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    def test_list_current_mentorship_relation(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations/current",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = marshal(
                self.future_accepted_mentorship_relation,
                mentorship_request_response_body,
            )

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    def test_list_all_mentorship_relations(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations",
                headers=get_test_request_header(self.admin_user.id),
            )
            expected_response = [
                marshal(
                    self.admin_only_mentorship_relation,
                    mentorship_request_response_body,
                )
            ]

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    def test_list_current_mentorship_relation_sent_by_current_user(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations/current",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = marshal(
                self.future_accepted_mentorship_relation,
                mentorship_request_response_body,
            )

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))
            self.assertFalse(self.future_accepted_mentorship_relation.sent_by_me)

    def test_list_current_mentorship_relation_sent_by_another_user(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations/current",
                headers=get_test_request_header(self.first_user.id),
            )
            expected_response = marshal(
                self.future_accepted_mentorship_relation,
                mentorship_request_response_body,
            )

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))
            self.assertTrue(self.future_accepted_mentorship_relation.sent_by_me)

    # The following test cases are concerned with the filtering of mentorship relations by the query param(relation_state) value.
    # When relation_state = ''.
    def test_list_filter_mentorship_relations_empty(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations?relation_state=%s" % "",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = [
                marshal(
                    self.past_mentorship_relation, mentorship_request_response_body
                ),
                marshal(
                    self.future_pending_mentorship_relation,
                    mentorship_request_response_body,
                ),
                marshal(
                    self.future_accepted_mentorship_relation,
                    mentorship_request_response_body,
                ),
                marshal(
                    self.admin_only_mentorship_relation,
                    mentorship_request_response_body,
                ),
            ]

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    # When relation_state = 'accepted'.
    def test_list_filter_mentorship_relations_accepted(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations?relation_state=%s" % "accepted",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = [
                marshal(
                    self.future_accepted_mentorship_relation,
                    mentorship_request_response_body,
                )
            ]

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    # When relation_state = 'pending'.
    def test_list_filter_mentorship_relations_pending(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations?relation_state=%s" % "pending",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = [
                marshal(
                    self.past_mentorship_relation, mentorship_request_response_body
                ),
                marshal(
                    self.future_pending_mentorship_relation,
                    mentorship_request_response_body,
                ),
            ]

            self.assertEqual(200, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))

    # When relation_state = 'invalid_param'.
    def test_list_filter_mentorship_relations_invalid(self):
        with self.client:
            response = self.client.get(
                "/mentorship_relations?relation_state=%s" % "invalid_param",
                headers=get_test_request_header(self.second_user.id),
            )
            expected_response = []

            self.assertEqual(400, response.status_code)
            self.assertEqual(expected_response, json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
