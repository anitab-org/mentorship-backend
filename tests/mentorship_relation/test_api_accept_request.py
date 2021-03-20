import json
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from http import HTTPStatus

from app import messages
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestAcceptMentorshipRequestApi(MentorshipRelationBaseTestCase):
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

    def mail_send_mocked(self):
        return self

    # mocking mail.send function which connects with smtp server
    @patch("flask_mail._MailMixin.send", side_effect=mail_send_mocked)
    def test_accept_mentorship_request(self, send_email_function):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                headers=get_test_request_header(self.second_user.id),
            )

            self.assertEqual(HTTPStatus.OK, response.status_code)
            self.assertEqual(
                MentorshipRelationState.ACCEPTED, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY,
                json.loads(response.data),
            )

    # Assuming User1 sent request X to User2, User2 accepts this request, while
    # User2 is involved in a current mentorship relation
    # 400, USER_IS_INVOLVED_IN_A_MENTORSHIP_RELATION response
    def test_recepient_already_in_relation_accept_request(self):
        # create existing relation between admin_user and second_user
        mentorship_relation_current = MentorshipRelationModel(
            action_user_id=self.admin_user.id,
            mentor_user=self.admin_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )
        db.session.add(mentorship_relation_current)
        db.session.commit()
        self.assertEqual(
            MentorshipRelationState.ACCEPTED, mentorship_relation_current.state
        )  # current
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )  # new
        with self.client:
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                headers=get_test_request_header(self.second_user.id),
            )
            self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
            self.assertEqual(
                MentorshipRelationState.ACCEPTED, mentorship_relation_current.state
            )  # current
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )  # new
            self.assertDictEqual(
                messages.USER_IS_INVOLVED_IN_A_MENTORSHIP_RELATION,
                json.loads(response.data),
            )

    # Assuming User1 sent request X to User2, User1 accepts this request
    # 400, CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER response
    def test_accept_own_request(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                headers=get_test_request_header(self.first_user.id),
            )
            self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER, json.loads(response.data)
            )

    # User1 accepts a mentorship relation which the User1 is not involved with
    # 500, Internal server error: fix add "messages.CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION"
    # in mentorship_relation.py
    # 400, CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION response
    def test_accept_request_by_uninvolved_user(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            # admin_user acts as uninvolved 3rd user
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                headers=get_test_request_header(self.admin_user.id),
            )
            self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION,
                json.loads(response.data),
            )

    # Valid user tries to accept valid task with authentication token missing
    # 401, AUTHORISATION_TOKEN_IS_MISSING response
    def test_accept_request_token_missing(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/accept"
            )
            self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(
                messages.AUTHORISATION_TOKEN_IS_MISSING, json.loads(response.data)
            )

    # Valid user tries to accept valid task with authentication token expired
    # 401, TOKEN_HAS_EXPIRED response
    def test_accept_request_token_expired(self):
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )
        with self.client:
            # generate token that expired 10 seconds ago
            auth_header = get_test_request_header(
                self.second_user.id, token_expiration_delta=timedelta(seconds=-10)
            )
            response = self.client.put(
                f"/mentorship_relation/{self.mentorship_relation.id}/accept",
                headers=auth_header,
            )
            self.assertEqual(HTTPStatus.UNAUTHORIZED, response.status_code)
            self.assertEqual(
                MentorshipRelationState.PENDING, self.mentorship_relation.state
            )
            self.assertDictEqual(messages.TOKEN_HAS_EXPIRED, json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
