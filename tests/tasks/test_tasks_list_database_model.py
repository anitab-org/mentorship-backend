import unittest
from datetime import datetime

from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase


class TestTasksListModel(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.empty_tasks_list = TasksListModel()
        self.tasks_list_1 = TasksListModel()
        db.session.add(self.empty_tasks_list)
        db.session.add(self.tasks_list_1)
        db.session.commit()

        self.now_timestamp = datetime.utcnow().timestamp()
        self.test_description_1 = "test description number one"
        self.test_description_2 = "test description number two"

        self.tasks_list_1.add_task(self.test_description_1, self.now_timestamp)

    def test_tasks_list_creation(self):

        tasks_list_one = TasksListModel.query.filter_by(id=1).first()

        self.assertIsNotNone(tasks_list_one)
        self.assertEqual([], tasks_list_one.tasks)
        self.assertEqual(1, tasks_list_one.next_task_id)
        self.assertEqual(1, tasks_list_one.id)

    def test_add_task_to_tasks_list(self):

        tasks_list_one = TasksListModel.query.filter_by(id=1).first()

        self.assertEqual([], tasks_list_one.tasks)

        tasks_list_one.add_task(self.test_description_1, self.now_timestamp)

        expected_task_1 = dict(
            completed_at=None,
            created_at=self.now_timestamp,
            description=self.test_description_1,
            id=1,
            is_done=False,
        )

        self.assertEqual([expected_task_1], tasks_list_one.tasks)

        tasks_list_one.add_task(self.test_description_1, self.now_timestamp)

        expected_task_2 = dict(
            completed_at=None,
            created_at=self.now_timestamp,
            description=self.test_description_1,
            id=2,
            is_done=False,
        )

        self.assertEqual([expected_task_1, expected_task_2], tasks_list_one.tasks)

    def test_remove_task_from_tasks_list(self):

        tasks_list_one = TasksListModel.query.filter_by(id=1).first()

        self.assertEqual([], tasks_list_one.tasks)

        tasks_list_one.add_task(self.test_description_1, self.now_timestamp)

        expected_task_1 = dict(
            completed_at=None,
            created_at=self.now_timestamp,
            description=self.test_description_1,
            id=1,
            is_done=False,
        )

        self.assertEqual([expected_task_1], tasks_list_one.tasks)

        tasks_list_one.delete_task(task_id=1)

        self.assertEqual([], tasks_list_one.tasks)

    def test_remove_task_from_pre_filled_list(self):

        tasks_list_two = TasksListModel.query.filter_by(id=2).first()

        expected_task_1 = dict(
            completed_at=None,
            created_at=self.now_timestamp,
            description=self.test_description_1,
            id=1,
            is_done=False,
        )

        self.assertEqual([expected_task_1], tasks_list_two.tasks)
        self.assertFalse(tasks_list_two.is_empty())

        tasks_list_two.delete_task(task_id=1)

        self.assertEqual([], tasks_list_two.tasks)
        self.assertTrue(tasks_list_two.is_empty())

    def test_empty_tasks_list_function(self):

        tasks_list_one = TasksListModel.query.filter_by(id=1).first()
        self.assertTrue(tasks_list_one.is_empty())

    def test_find_task_by_id(self):

        tasks_list_one = TasksListModel.query.filter_by(id=1).first()

        expected_task_1 = dict(
            completed_at=None,
            created_at=self.now_timestamp,
            description=self.test_description_1,
            id=1,
            is_done=False,
        )
        expected_task_2 = dict(
            completed_at=None,
            created_at=self.now_timestamp,
            description=self.test_description_2,
            id=2,
            is_done=False,
        )

        tasks_list_one.add_task(self.test_description_1, self.now_timestamp)
        tasks_list_one.add_task(self.test_description_2, self.now_timestamp)

        found_task_1 = tasks_list_one.find_task_by_id(task_id=1)
        self.assertIsNotNone(found_task_1)
        self.assertEqual(expected_task_1, found_task_1)

        found_task_2 = tasks_list_one.find_task_by_id(task_id=2)
        self.assertIsNotNone(found_task_2)
        self.assertEqual(expected_task_2, found_task_2)

        found_task_3 = tasks_list_one.find_task_by_id(task_id=3)
        self.assertIsNone(found_task_3)

    def test_update_task(self):

        tasks_list_one = TasksListModel.query.filter_by(id=2).first()
        self.assertIsNotNone(tasks_list_one)

        task_1 = tasks_list_one.find_task_by_id(task_id=1)
        self.assertIsNotNone(task_1)
        self.assertFalse(task_1.get("is_done"))

        tasks_list_one.update_task(task_id=1, is_done=True)

        new_task_1 = tasks_list_one.find_task_by_id(task_id=1)
        self.assertTrue(new_task_1.get("is_done"))


if __name__ == "__main__":
    unittest.main()
