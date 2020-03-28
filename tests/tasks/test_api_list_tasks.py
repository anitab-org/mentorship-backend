import unittest
from flask import json
from flask_restplus import marshal

from app import messages
from app.api.models.mentorship_relation import list_tasks_response_body
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header


class TestListTasksApi(TasksBaseTestCase):
    def test_list_tasks_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.get(
            "/mentorship_relation/%s/tasks" % self.mentorship_relation_w_second_user.id,
            follow_redirects=True,
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_list_tasks_api_first_mentorship_relation(self):

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = marshal(self.tasks_list_1.tasks, list_tasks_response_body)
        actual_response = self.client.get(
            "/mentorship_relation/%s/tasks" % self.mentorship_relation_w_second_user.id,
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_tasks_api_second_mentorship_relation(self):

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = marshal(self.tasks_list_2.tasks, list_tasks_response_body)
        actual_response = self.client.get(
            "/mentorship_relation/%s/tasks" % self.mentorship_relation_w_admin_user.id,
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_list_tasks_api_w_user_not_belonging_to_mentorship_relation(self):

        auth_header = get_test_request_header(self.second_user.id)
        expected_response = messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION
        actual_response = self.client.get(
            "/mentorship_relation/%s/tasks" % self.mentorship_relation_w_admin_user.id,
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_list_tasks_api_mentorship_relation_without_tasks(self):

        auth_header = get_test_request_header(self.second_user.id)
        expected_response = []
        actual_response = self.client.get(
            "/mentorship_relation/%s/tasks"
            % self.mentorship_relation_without_first_user.id,
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))


if __name__ == "__main__":
    unittest.main()
