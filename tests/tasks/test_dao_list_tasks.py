import unittest

from app.api.dao.task import TaskDAO
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestListTasksDao(TasksBaseTestCase):

    def test_list_tasks(self):

        expected_response = self.tasks_list_1.tasks
        actual_response = TaskDAO.list_tasks(self.first_user.id, self.mentorship_relation_w_second_user.id)

        self.assertEqual(expected_response, actual_response)

    def test_list_empty_tasks(self):

        expected_response = []
        actual_response = TaskDAO.list_tasks(self.admin_user.id, self.mentorship_relation_without_first_user.id)

        self.assertEqual(expected_response, actual_response)

    def test_list_tasks_with_non_existent_relation(self):

        expected_response = {'message': 'Mentorship relation does not exist.'}, 404
        actual_response = TaskDAO.list_tasks(self.first_user.id, 123123)

        self.assertEqual(expected_response, actual_response)

    def test_list_tasks_with_non_existent_user(self):

        expected_response = {'message': 'User does not exist.'}, 404
        actual_response = TaskDAO.list_tasks(123123, self.mentorship_relation_w_second_user.id)

        self.assertEqual(expected_response, actual_response)

    def test_list_tasks_with_user_not_involved(self):

        expected_response = {'message': 'You are not involved in this mentorship relation.'}, 401
        actual_response = TaskDAO.list_tasks(self.admin_user.id, self.mentorship_relation_w_second_user.id)

        self.assertEqual(expected_response, actual_response)


if __name__ == '__main__':
    unittest.main()
