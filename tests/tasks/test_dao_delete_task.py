import unittest
from http import HTTPStatus

from app import messages
from app.api.dao.task import TaskDAO
from http import HTTPStatus
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestDeleteTasksDao(TasksBaseTestCase):
    def test_delete_existent_task(self):

        expected_response = messages.TASK_WAS_DELETED_SUCCESSFULLY, HTTPStatus.OK
        first_task_id = 1

        not_deleted_yet_task = self.tasks_list_1.find_task_by_id(task_id=first_task_id)
        self.assertIsNotNone(not_deleted_yet_task)

        actual_response = TaskDAO.delete_task(
            self.first_user.id, self.mentorship_relation_w_second_user.id, first_task_id
        )
        self.assertEqual(expected_response, actual_response)

        deleted_task = self.tasks_list_1.find_task_by_id(task_id=first_task_id)
        self.assertIsNone(deleted_task)

    def test_delete_task_from_non_existing_relation(self):
        expected_response = (
            messages.MENTORSHIP_RELATION_DOES_NOT_EXIST,
            HTTPStatus.NOT_FOUND,
        )
        second_task_id = 2

        second_task = self.tasks_list_1.find_task_by_id(task_id=second_task_id)
        self.assertIsNotNone(second_task)

        actual_response = TaskDAO.delete_task(
            user_id=self.first_user.id,
            mentorship_relation_id=100,
            task_id=second_task_id,
        )

        self.assertEqual(expected_response, actual_response)

    def test_delete_non_existent_task(self):

        expected_response = messages.TASK_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND
        actual_response = TaskDAO.delete_task(
            self.first_user.id, self.mentorship_relation_w_second_user.id, 123123
        )

        self.assertEqual(expected_response, actual_response)


if __name__ == "__main__":
    unittest.main()
