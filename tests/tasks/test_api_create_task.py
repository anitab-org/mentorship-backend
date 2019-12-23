import unittest
from flask import json

from app import messages
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header

from datetime import timedelta


class TestCreateTaskApi(TasksBaseTestCase):

    def test_create_task_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True)

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

# This case tests whether the user is in a mentorship relation or not while creating a new task.
# If the user is not in a mentorship relation and he tries to create a task, then
# '404:Not found' error would be given displaying the message that 'Mentorship relation does not exist'.
    def test_create_task_api_user_not_in_mentorship_relation(self):
        auth_header=get_test_request_header(self.first_user.id)
        expected_response=messages.MENTORSHIP_RELATION_DOES_NOT_EXIST
        actual_response = self.client.post('/mentorship_relation/%s/task' % 123123,
                                            follow_redirects=True, headers=auth_header, content_type='application/json',
                                            data=json.dumps(dict(description=self.test_description)))

        self.assertEqual(404,actual_response.status_code)
        self.assertDictEqual(expected_response,json.loads(actual_response.data))

# This case tests the creation of task without description field.
# If a user creates a task without a description field, then
# '400:Bad Request' error would be given displaying the message that 'Description field is missing'.
    def test_create_task_api_empty_description_field(self):
        auth_header=get_test_request_header(self.first_user.id)
        expected_response=messages.DESCRIPTION_FIELD_IS_MISSING
        actual_response=self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                         follow_redirects=True, headers=auth_header, content_type='application/json',
                                         data=json.dumps(dict()))

        self.assertEqual(400,actual_response.status_code)
        self.assertDictEqual(expected_response,json.loads(actual_response.data))

# This case tests the creation of task with an expired authentication token.
# If a user creates a task with an expired authentication token, then
# '401:Unauthorised' error would be given displaying the message that 'The token has expired! Please, login again or refresh it.'.
    def test_create_task_api_with_token_expired(self):
        auth_header=get_test_request_header(self.first_user.id,token_expiration_delta=timedelta(minutes=-5))
        expected_response=messages.TOKEN_HAS_EXPIRED
        actual_response = self.client.post('/mentorship_relation/%s/task' % self.mentorship_relation_w_second_user.id,
                                           follow_redirects=True, headers=auth_header, content_type='application/json',
                                           data=json.dumps(dict(description=self.test_description)))

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

if __name__ == "__main__":
    unittest.main()
