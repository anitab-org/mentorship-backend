import json
import unittest
from datetime import datetime, timedelta
from http import HTTPStatus

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestRejectMentorshipRequestApi(MentorshipRelationBaseTestCase):
    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super().setUp()

        self.notes_example = "description of a good mentorship relation"
        self.now_datetime = datetime.utcnow()
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
            tasks_list=TasksListModel(),
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test_reject_mentorship_request(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/reject",
                headers=get_test_request_header(self.second_user.id),
            )

            self.assertEqual(HTTPStatus.OK, response.status_code)
            self.assertEqual(
                MentorshipRelationState.REJECTED, self.mentorship_relation.state
            )
            self.assertEqual(
                messages.MENTORSHIP_RELATION_WAS_REJECTED_SUCCESSFULLY,
                json.loads(response.data),
            )

    def test_reject_request_by_uninvolved_user(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            # admin_user acts as uninvolved 3rd user
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/reject",
                headers=get_test_request_header(self.admin_user.id),
            )
            self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.CANT_REJECT_UNINVOLVED_RELATION_REQUEST,
                json.loads(response.data),
            )

    def test_reject_request_token_missing(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/reject"
            )
            self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.AUTHORISATION_TOKEN_IS_MISSING,
                json.loads(response.data),
            )

    def test_reject_request_token_expired(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            # generate token that expired 10 seconds ago
            auth_header = get_test_request_header(
                self.second_user.id, token_expiration_delta=timedelta(seconds=-10)
            )
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/reject",
                headers=auth_header,
            )
            self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.TOKEN_HAS_EXPIRED,
                json.loads(response.data),
            )


if __name__ == "__main__":
    unittest.main()
