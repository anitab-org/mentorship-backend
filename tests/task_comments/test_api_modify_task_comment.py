import json
import unittest

from app import messages
from app.api.dao.task_comment import TaskCommentDAO
from app.api.validations.task_comment import COMMENT_MAX_LENGTH
from app.database.sqlalchemy_extension import db
from app.utils.validation_utils import get_length_validation_error_message
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header
from http import HTTPStatus


class TestModifyTaskCommentApi(TasksBaseTestCase):
    def setUp(self):
        super().setUp()
        self.relation_id = self.mentorship_relation_w_admin_user.id
        self.relation_id_one = self.mentorship_relation_bw_fourth_fifth_user.id
        self.task_id = 1
        self.task_id_one = 4
        self.comment_id = 1
        TaskCommentDAO().create_task_comment(
            user_id=1, task_id=1, relation_id=self.relation_id, comment="comment"
        )
        self.tasks_list_2.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
        )

        db.session.add(self.tasks_list_2)
        db.session.commit()

    def test_task_comment_modification_api_without_comment(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.COMMENT_FIELD_IS_MISSING
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}"
            f"/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(example="example")),
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_comment_too_long(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = {
            "message": get_length_validation_error_message(
                "comment", None, COMMENT_MAX_LENGTH
            )
        }
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}"
            f"/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="a" * 500)),
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_comment_not_string(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.COMMENT_NOT_IN_STRING_FORMAT
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}"
            f"/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment=5)),
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_not_created_by_user(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_COMMENT_WAS_NOT_CREATED_BY_YOU
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}"
            f"/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(HTTPStatus.FORBIDDEN, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_relation_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.MENTORSHIP_RELATION_DOES_NOT_EXIST
        actual_response = self.client.put(
            f"mentorship_relation/0/task/{self.task_id}/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_unaccepted_relation(self):
        auth_header = get_test_request_header(self.fourth_user.id)
        expected_response = messages.UNACCEPTED_STATE_RELATION
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id_one}/task/{self.task_id_one}/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(HTTPStatus.BAD_REQUEST, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_task_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_DOES_NOT_EXIST
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/0/comment/"
            f"{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_comment_not_existing(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_COMMENT_DOES_NOT_EXIST
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}/comment/0",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_task_comment_modification_api_with_wrong_task_id(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_COMMENT_WITH_GIVEN_TASK_ID_DOES_NOT_EXIST
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/2/comment/"
            f"{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="comment")),
        )

        self.assertEqual(HTTPStatus.NOT_FOUND, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_full_task_comment_modification_api(self):
        auth_header = get_test_request_header(self.admin_user.id)
        expected_response = messages.TASK_COMMENT_WAS_UPDATED_SUCCESSFULLY
        actual_response = self.client.put(
            f"mentorship_relation/{self.relation_id}/task/{self.task_id}"
            f"/comment/{self.comment_id}",
            follow_redirects=True,
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(dict(comment="Modified comment.")),
        )

        self.assertEqual(HTTPStatus.OK, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

        modified_comment = TaskCommentDAO.get_task_comment(1, 1)[0]
        self.assertIsNotNone(modified_comment)
        self.assertEqual(self.relation_id, modified_comment.relation_id)
        self.assertEqual("Modified comment.", modified_comment.comment)

    if __name__ == "__main__":
        unittest.main()
