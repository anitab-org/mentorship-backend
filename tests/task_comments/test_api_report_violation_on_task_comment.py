import json
import unittest

from flask_restx import marshal

from app import messages
from app.api.dao.task_comment import TaskCommentDAO
from app.api.models.mentorship_relation import task_comments_model
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header

class TestReportViolationOnTaskCommentAPI(TasksBaseTestCase):
    def setUp(self):
        super().setUp()
        self.relation_id = self.mentorship_relation_w_admin_user.id
        self.task_id = 1

        TaskCommentDAO().create_task_comment(
            user_id=1, task_id=1, relation_id=self.relation_id, comment="comment"
        )

    def test_report_violation_without_auth_header(self):
        # Call API without header
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}/comment/{1}/report",
            follow_redirects=True,
            content_type="application/json",
        )
        # Test
        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_report_violation_self_comment(self):
        # Set headers, expected response, and actual response.
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.USER_CANT_REPORT_THEIR_OWN_COMMENT
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}/comment/{1}/report",
            follow_redirects=True,
            content_type="application/json",
            headers=auth_header
        )
        # Test
        self.assertEqual(actual_response.status_code, 403)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_report_violation_other_comment_success(self):
        # Create new task comment from other user id; so that we can report it
        TaskCommentDAO().create_task_comment(
            user_id=2, task_id=1, relation_id=self.relation_id, comment="comment"
        )
        # Set headers, expected response, and actual response.
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.VIOLATION_WAS_REPORTED_SUCCESSFULLY
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}/comment/{2}/report",
            follow_redirects=True,
            content_type="application/json",
            headers=auth_header
        )
        # Test
        self.assertEqual(actual_response.status_code, 200)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    if __name__ == "__main__":
        unittest.main()