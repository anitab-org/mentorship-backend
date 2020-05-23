import unittest
from flask import json

from app import messages
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header


class TestDeleteTaskApi(TasksBaseTestCase):
    def test_delete_task_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.delete(
            "/mentorship_relation/%s/task/%s"
            % (self.mentorship_relation_w_second_user.id, 2),
            follow_redirects=True,
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_delete_task_api_w_user_not_belonging_to_mentorship_relation_1(self):
        expected_response = messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION
        auth_header = get_test_request_header(self.admin_user.id)
        actual_response = self.client.delete(
            "/mentorship_relation/%s/task/%s"
            % (self.mentorship_relation_w_second_user.id, 1),
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_delete_task_api_w_user_not_belonging_to_mentorship_relation_2(self):
        expected_response = messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION
        auth_header = get_test_request_header(self.second_user.id)
        actual_response = self.client.delete(
            "/mentorship_relation/%s/task/%s"
            % (self.mentorship_relation_w_admin_user.id, 1),
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_full_task_deletion_api(self):

        existent_task = self.tasks_list_1.find_task_by_id(2)
        self.assertIsNotNone(existent_task)

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_WAS_DELETED_SUCCESSFULLY
        actual_response = self.client.delete(
            "/mentorship_relation/%s/task/%s"
            % (self.mentorship_relation_w_second_user.id, 2),
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

        deleted_task = self.tasks_list_1.find_task_by_id(2)
        self.assertIsNone(deleted_task)

    def test_delete_task_api_non_existing_task(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_DOES_NOT_EXIST
        actual_response = self.client.delete(
            "/mentorship_relation/%s/task/%s"
            % (self.mentorship_relation_w_second_user.id, 0),
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(404, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
