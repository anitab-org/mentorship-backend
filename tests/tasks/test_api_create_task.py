import unittest
from datetime import timedelta

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

    def test_user_involved_in_mentorship_relation_creates_task(self):
        auth_header = get_test_request_header(self.second_user.id)

        actual_response = self.client.post('/mentorship_relation/3/task',
                                           follow_redirects=True, headers=auth_header, content_type='application/json',
                                           data=json.dumps(dict(description=self.test_description)))
        expected_response = messages.UNACCEPTED_STATE_RELATION

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_user_creates_task_without_descripton(self):
        auth_header = get_test_request_header(self.second_user.id)

        expected_response = messages.DESCRIPTION_FIELD_IS_MISSING
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True, headers=auth_header, content_type='application/json',
                                           data=json.dumps(dict()))

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_user_creates_task_with_expired_token(self):
        auth_header = get_test_request_header(self.second_user.id, token_expiration_delta=timedelta(-10))

        expected_response = messages.TOKEN_HAS_EXPIRED
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True, headers=auth_header, content_type='application/json',
                                           data=json.dumps(dict(description=self.test_description)))

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_full_task_creation_api(self):

        non_existent_task = self.tasks_list_1.find_task_by_id(3)
        self.assertIsNone(non_existent_task)

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_WAS_CREATED_SUCCESSFULLY
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True, headers=auth_header, content_type='application/json',
                                           data=json.dumps(dict(description=self.test_description)))

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

        new_task = self.tasks_list_1.find_task_by_id(3)
        self.assertIsNotNone(new_task)
        self.assertEqual(self.test_description, new_task.get('description'))
        self.assertEqual(self.test_is_done, new_task.get('is_done'))


if __name__ == "__main__":
    unittest.main()
