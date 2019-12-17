import unittest
from flask import json

from app import messages
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header


class TestCreateTaskApi(TasksBaseTestCase):

    def test_create_task_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_full_task_creation_api(self):

        non_existent_task = self.tasks_list_1.find_task_by_id(4)
        self.assertIsNone(non_existent_task)

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_WAS_CREATED_SUCCESSFULLY
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True, headers=auth_header, content_type='application/json',
                                           data=json.dumps(dict(description=self.test_description)))

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

        new_task = self.tasks_list_1.find_task_by_id(4)
        self.assertIsNotNone(new_task)
        self.assertEqual(self.test_description, new_task.get('description'))
        self.assertEqual(self.test_is_done, new_task.get('is_done'))


if __name__ == "__main__":
    unittest.main()
