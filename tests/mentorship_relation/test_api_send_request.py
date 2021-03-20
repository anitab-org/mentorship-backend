import json
import unittest
from datetime import datetime, timedelta
from http import HTTPStatus

from app import messages
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestSendRequestApi(MentorshipRelationBaseTestCase):
    def setUp(self):
        super().setUp()

    def test_created_error_code_for_send_request(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY
        test_payload = {
            "mentor_id": self.first_user.id,
            "mentee_id": self.second_user.id,
            "end_date": int((datetime.utcnow() + timedelta(days=40)).timestamp()),
            "notes": "some notes",
        }
        actual_response = self.client.post(
            "/mentorship_relation/send_request",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(test_payload),
        )
        self.assertEqual(HTTPStatus.CREATED, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_fail_send_request_bad_mentee_id(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MENTEE_DOES_NOT_EXIST
        test_payload = {
            "mentor_id": self.first_user.id,
            "mentee_id": 1234,
            "end_date": int((datetime.utcnow() + timedelta(days=40)).timestamp()),
            "notes": "some notes",
        }
        actual_response = self.client.post(
            "/mentorship_relation/send_request",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(test_payload),
        )
        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_fail_send_request_bad_mentor_id(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MENTOR_DOES_NOT_EXIST
        test_payload = {
            "mentor_id": 1234,
            "mentee_id": self.first_user.id,
            "end_date": int((datetime.utcnow() + timedelta(days=40)).timestamp()),
            "notes": "some notes",
        }
        actual_response = self.client.post(
            "/mentorship_relation/send_request",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(test_payload),
        )
        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    # In case if a user tries to send request on behalf of some other user
    def test_fail_send_request_bad_user_id(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MATCH_EITHER_MENTOR_OR_MENTEE
        test_payload = {
            "mentor_id": self.second_user.id,
            "mentee_id": 4321,
            "end_date": int((datetime.utcnow() + timedelta(days=40)).timestamp()),
            "notes": "some notes",
        }
        actual_response = self.client.post(
            "/mentorship_relation/send_request",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(test_payload),
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
