import unittest
from flask import json

from app import messages
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header

class TestDeleteTaskApi(TasksBaseTestCase):

    def test_delete_task_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.delete('/mentorship_relation/%s/task/%s'
                                             % (self.mentorship_relation_w_second_user.id, 2),
                                             follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_full_task_deletion_api(self):

        existent_task = self.tasks_list_1.find_task_by_id(2)
        self.assertIsNotNone(existent_task)

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_WAS_DELETED_SUCCESSFULLY
        actual_response = self.client.delete('/mentorship_relation/%s/task/%s'
                                             % (self.mentorship_relation_w_second_user.id, 2),
                                             follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

        deleted_task = self.tasks_list_1.find_task_by_id(2)
        self.assertIsNone(deleted_task)


if __name__ == "__main__":
    unittest.main()
