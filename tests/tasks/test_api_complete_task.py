import unittest
from flask import json

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from tests.test_utils import get_test_request_header


class TestCompleteTaskApi(TasksBaseTestCase):
    def test_complete_task_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.put(
            "/mentorship_relation/%s/task/%s/complete"
            % (self.mentorship_relation_w_second_user.id, 2),
            follow_redirects=True,
        )

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_complete_task_api(self):

        relation = MentorshipRelationModel.find_by_id(
            self.mentorship_relation_w_second_user.id
        )
        incomplete_task = relation.tasks_list.find_task_by_id(1)
        self.assertIsNotNone(incomplete_task)
        self.assertIsNone(incomplete_task.get("completed_at"))
        self.assertFalse(incomplete_task.get("is_done"))

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.TASK_WAS_ACHIEVED_SUCCESSFULLY
        actual_response = self.client.put(
            "/mentorship_relation/%s/task/%s/complete"
            % (self.mentorship_relation_w_second_user.id, 1),
            follow_redirects=True,
            headers=auth_header,
        )

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

        relation = MentorshipRelationModel.find_by_id(
            self.mentorship_relation_w_second_user.id
        )
        complete_task = relation.tasks_list.find_task_by_id(1)
        self.assertIsNotNone(complete_task)
        self.assertIsNotNone(complete_task.get("completed_at"))
        self.assertTrue(complete_task.get("is_done"))


if __name__ == "__main__":
    unittest.main()
