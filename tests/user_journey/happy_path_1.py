import unittest
from datetime import datetime, timedelta

from flask import json
from flask_restx import marshal

from app import messages
from app.api.models.user import public_user_api_model
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_utils import get_test_request_header
from tests.test_data import user1, user2, user3
from app.api.models.mentorship_relation import mentorship_request_response_body


class TestHappyPath1(BaseTestCase):
    """
    Scenario: User A (mentor) and User B (mentee) sending 
    a mentorship request until the mentee completes a task

    - User B (mentee) sends a request to User A (mentor)
    - User A (mentor) accepts request
    - User A (mentor) or User B (mentee) creates a task
    - User B (mentee) completes the task
    """

    def setUp(self):
        super(TestHappyPath1, self).setUp()

        self.mentor = UserModel(
            name="Mentor A",
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )  # User A

        self.mentee = UserModel(
            name="Mentee B",
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )  # User B

        self.mentor.is_email_verified = True
        self.mentee.is_email_verified = True

        self.mentor.available_to_mentor = True
        self.mentee.need_mentoring = True

        db.session.add(self.mentor)
        db.session.add(self.mentee)
        db.session.commit()

    def test_happy_path_1(self):

        mentor_auth_header = get_test_request_header(self.mentor.id)
        mentee_auth_header = get_test_request_header(self.mentee.id)

        # - User B (mentee) sends a request to User A (mentor)
        # POST /mentorship_relation/send_request

        request_body = {
            "mentor_id": self.mentor.id,
            "mentee_id": self.mentee.id,
            "end_date": int((datetime.now() + timedelta(days=40)).timestamp()),
            "notes": "some notes",
        }
        send_request_response = self.client.post(
            "/mentorship_relation/send_request",
            headers=mentee_auth_header,
            content_type="application/json",
            data=json.dumps(request_body),
        )

        self.assertEqual(201, send_request_response.status_code)

        request_sent_response = self.client.get(
            "/mentorship_relations",
            headers=mentor_auth_header,
            content_type="application/json",
        )

        requests = json.loads(request_sent_response.data)
        mentorship_request = requests[0]
        request_id = mentorship_request["id"]
        request_state = mentorship_request["state"]

        self.assertIsNotNone(request_id)
        self.assertEqual(MentorshipRelationState.PENDING, request_state)

        # - User A (mentor) accepts request
        # POST /mentorship_relation/{request_id}/accept

        accept_response = self.client.put(
            f"/mentorship_relation/{request_id}/accept", headers=mentor_auth_header
        )

        self.assertEqual(200, accept_response.status_code)

        mentee_current_relation = self.client.get(
            f"/mentorship_relations/current", headers=mentor_auth_header
        )
        mentor_current_relation = self.client.get(
            f"/mentorship_relations/current", headers=mentor_auth_header
        )

        self.assertEqual(200, mentee_current_relation.status_code)
        self.assertEqual(200, mentor_current_relation.status_code)
        self.assertEqual(
            json.loads(mentor_current_relation.data),
            json.loads(mentee_current_relation.data),
        )

        current_relation = json.loads(mentee_current_relation.data)
        request_id = current_relation["id"]
        request_state = current_relation["state"]

        self.assertEqual(MentorshipRelationState.ACCEPTED, request_state)

        # - User A (mentor) or User B (mentee) creates a task
        # POST /mentorship_relationn/{request_id}/task

        # - User B (mentee) completes the task
        # PUT /mentorship_relationn/{request_id}/task/{task_id}/complete


if __name__ == "__main__":
    unittest.main()
