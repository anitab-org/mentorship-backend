import json
import unittest

from flask_restx import marshal

from app import messages
from app.api.dao.task_comment import TaskCommentDAO
from app.api.models.mentorship_relation import task_comments_model
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header
from http import HTTPStatus


class TestGetTaskCommentsApi(TasksBaseTestCase):
    def setUp(self):
        super().setUp()
        self.relation_id = self.mentorship_relation_w_admin_user.id
        self.relation_id_one = self.mentorship_relation_bw_fourth_fifth_user.id
        self.task_id = 1
        self.task_id_one = 4

        TaskCommentDAO().create_task_comment(
            user_id=1, task_id=1, relation_id=self.relation_id, comment="comment"
        )
        TaskCommentDAO().create_task_comment(
            user_id=1, task_id=1, relation_id=self.relation_id, comment="comment"
        )
        TaskCommentDAO().create_task_comment(
            user_id=1, task_id=1, relation_id=self.relation_id, comment="comment"
        )

    def test_task_comment_listing_api_without_auth_header(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.get(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}/comments/",
            follow_redirects=True,
            content_type="application/json",
        )

        self.assertEqual(HTTPStatus.UNAUTHORIZED, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_listing_api_with_task_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_DOES_NOT_EXIST
        actual_response = self.client.get(
            f"mentorship_relation/{self.relation_id}/task/0/comments/",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_listing_api_with_relation_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.MENTORSHIP_RELATION_DOES_NOT_EXIST
        actual_response = self.client.get(
            f"mentorship_relation/0/task/{self.task_id}/comments",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_listing_api_with_unaccepted_relation(self):
        auth_header = get_test_request_header(self.fourth_user.id)
        expected_response = messages.UNACCEPTED_STATE_RELATION
        actual_response = self.client.get(
            f"mentorship_relation/{self.relation_id_one}/task/{self.task_id_one}/comments",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_listing_api(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = marshal(
            TaskCommentDAO.get_all_task_comments_by_task_id(1, 1, 2),
            task_comments_model,
        )
        actual_response = self.client.get(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}/comments",
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertEqual(json.loads(actual_response.data), expected_response)

    if __name__ == "__main__":
        unittest.main()
