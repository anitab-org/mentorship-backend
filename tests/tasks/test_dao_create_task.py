import unittest

from app import messages
from app.api.dao.task import TaskDAO
from app.utils.enum_utils import MentorshipRelationState
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestListTasksDao(TasksBaseTestCase):
    def test_create_task(self):

        expected_response = messages.TASK_WAS_CREATED_SUCCESSFULLY, 201

        non_existent_task = self.tasks_list_1.find_task_by_id(3)
        self.assertIsNone(non_existent_task)

        actual_response = TaskDAO.create_task(
            user_id=self.first_user.id,
            mentorship_relation_id=self.mentorship_relation_w_second_user.id,
            data=dict(description=self.test_description, is_done=self.test_is_done),
        )
        self.assertEqual(expected_response, actual_response)

        new_task = self.tasks_list_1.find_task_by_id(3)
        self.assertIsNotNone(new_task)
        self.assertEqual(self.test_description, new_task.get("description"))
        self.assertEqual(self.test_is_done, new_task.get("is_done"))

    def test_create_task_with_non_existing_mentorship_relation(self):

        expected_response = messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        actual_response = TaskDAO.create_task(
            user_id=self.first_user.id,
            mentorship_relation_id=123123,
            data=dict(description=self.test_description, is_done=self.test_is_done),
        )

        self.assertEqual(expected_response, actual_response)

    def test_create_task_with_mentorship_relation_non_accepted_state(self):

        expected_response = messages.UNACCEPTED_STATE_RELATION, 400
        self.mentorship_relation_w_second_user.state = MentorshipRelationState.CANCELLED

        actual_response = TaskDAO.create_task(
            user_id=self.first_user.id,
            mentorship_relation_id=self.mentorship_relation_w_second_user.id,
            data=dict(description=self.test_description, is_done=self.test_is_done),
        )

        self.assertEqual(expected_response, actual_response)


if __name__ == "__main__":
    unittest.main()
