import unittest

from app.api.dao.task import TaskDAO
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestCompleteTasksDao(TasksBaseTestCase):

    def test_achieve_not_achieved_task(self):
        self.assertFalse(self.tasks_list_1.find_task_by_id(1).get('is_done'))

        expected_response = {'message': 'Task was achieved successfully.'}, 200
        actual_response = TaskDAO.complete_task(self.first_user.id,
                                               self.mentorship_relation_w_second_user.id,
                                               1)

        self.assertTrue(self.tasks_list_1.find_task_by_id(1).get('is_done'))
        self.assertEqual(expected_response, actual_response)

    def test_achieve_achieved_task(self):
        self.assertTrue(self.tasks_list_1.find_task_by_id(2).get('is_done'))

        expected_response = {'message': 'Task was already achieved.'}, 400
        actual_response = TaskDAO.complete_task(self.first_user.id,
                                               self.mentorship_relation_w_second_user.id,
                                               2)

        self.assertTrue(self.tasks_list_1.find_task_by_id(2).get('is_done'))
        self.assertEqual(expected_response, actual_response)

    def test_achieve_not_existent_task(self):

        expected_response = {'message': 'Task does not exist.'}, 404
        actual_response = TaskDAO.complete_task(self.first_user.id,
                                               self.mentorship_relation_w_second_user.id,
                                               123123)

        self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
