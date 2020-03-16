import json
import unittest

from app import messages
from app.api.dao.task_comment import TaskCommentDAO
from app.api.validations.task_comment import COMMENT_MAX_LENGTH
from app.utils.validation_utils import get_length_validation_error_message
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header


class TestCreateTaskCommentApi(TasksBaseTestCase):
    def setUp(self):
        super().setUp()
        self.relation_id = self.mentorship_relation_w_admin_user.id
        self.task_id = 1

    def test_task_comment_creation_api_without_comment(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.COMMENT_FIELD_IS_MISSING
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}" f"/comment",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(example="example")),
        )

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_creation_api_with_comment_not_string(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.COMMENT_NOT_IN_STRING_FORMAT
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}" f"/comment",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment=5)),
        )

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_creation_api_with_comment_too_long(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = {
            "message": get_length_validation_error_message(
                "comment", None, COMMENT_MAX_LENGTH
            )
        }
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}" f"/comment",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="a" * 500)),
        )

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_creation_api_with_relation_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.MENTORSHIP_RELATION_DOES_NOT_EXIST
        actual_response = self.client.post(
            f"mentorship_relation/0/task/{self.task_id}/comment",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(404, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_creation_api_with_task_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_DOES_NOT_EXIST
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/0/comment",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(404, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_full_task_comment_creation_api(self):
        non_existent_task_comment = TaskCommentDAO.get_task_comment(1, 1)
        self.assertEqual(non_existent_task_comment[1], 404)

        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_COMMENT_WAS_CREATED_SUCCESSFULLY
        actual_response = self.client.post(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}" f"/comment",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(201, actual_response.status_code)
        self.assertDictEqual(expected_response,
                             json.loads(actual_response.data))

        new_comment = TaskCommentDAO.get_task_comment(1, 1)[0]
        self.assertIsNotNone(new_comment)
        self.assertEqual(self.relation_id, new_comment.relation_id)
        self.assertEqual("comment", new_comment.comment)

    if __name__ == "__main__":
        unittest.main()
