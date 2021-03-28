import unittest
from http import HTTPStatus

from app import messages
from app.api.dao.task import TaskDAO
from http import HTTPStatus
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestCompleteTasksDao(TasksBaseTestCase):
    def test_achieve_not_achieved_task(self):
        self.assertFalse(self.tasks_list_1.find_task_by_id(1).get("is_done"))

        expected_response = messages.TASK_WAS_ACHIEVED_SUCCESSFULLY, HTTPStatus.OK
        actual_response = TaskDAO.complete_task(
            self.first_user.id, self.mentorship_relation_w_second_user.id, 1
        )

        self.assertTrue(self.tasks_list_1.find_task_by_id(1).get("is_done"))
        self.assertEqual(expected_response, actual_response)

    def test_achieve_achieved_task(self):
        self.assertTrue(self.tasks_list_1.find_task_by_id(2).get("is_done"))

        expected_response = (
            messages.TASK_WAS_ALREADY_ACHIEVED,
            HTTPStatus.CONFLICT,
        )
        actual_response = TaskDAO.complete_task(
            self.first_user.id, self.mentorship_relation_w_second_user.id, 2
        )

        self.assertTrue(self.tasks_list_1.find_task_by_id(2).get("is_done"))
        self.assertEqual(expected_response, actual_response)

    def test_achieve_not_existent_task(self):

        expected_response = messages.TASK_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
        actual_response = TaskDAO.complete_task(
            self.first_user.id, self.mentorship_relation_w_second_user.id, 123123
        )

        self.assertEqual(expected_response, actual_response)

    def test_achieve_task_from_non_existing_relation(self):
        task_id = 1

        self.assertFalse(self.tasks_list_2.find_task_by_id(task_id).get("is_done"))
        expected_response = (
            messages.MENTORSHIP_RELATION_DOES_NOT_EXIST,
            HTTPStatus.NOT_FOUND,
        )

        actual_response = TaskDAO.complete_task(
            user_id=self.first_user.id, mentorship_relation_id=123123, task_id=task_id
        )
        self.assertEqual(expected_response, actual_response)
        self.assertFalse(self.tasks_list_2.find_task_by_id(task_id).get("is_done"))


if __name__ == "__main__":
    unittest.main()
