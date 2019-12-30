import unittest

from app.api.dao.task_comment import TaskCommentDAO
from app.database.models.task_comment import TaskCommentModel
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestTaskCommentDao(TasksBaseTestCase):

    def test_dao_create_task_comment(self):
        dao = TaskCommentDAO()
        data = dict(
            user_id=1,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(1, 1, data)

        # Verify that task comment was inserted in database through DAO
        task_comment = TaskCommentModel.query.filter_by(task_id=1, user_id=1).first()
        self.assertTrue(task_comment is not None)
        self.assertTrue(task_comment.id is not None)
        self.assertTrue(task_comment.task_id == 1)
        self.assertIsNotNone(task_comment.creation_date)
        self.assertEqual(task_comment.comment, 'comment')

    def test_dao_find_by_task_id(self):
        dao = TaskCommentDAO()
        data1 = dict(
            user_id=1,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(1, 1, data1)
        data2 = dict(
            user_id=1,
            task_id=1,
            comment='hello'
        )
        dao.create_task_comment(1, 1, data2)

        # Verify that find_by_task_id() function is working properly
        task_comments = dao.get_task_comments_by_task_id(1)[0]
        for task_comment in task_comments:
            self.assertTrue(task_comment is not None)
            self.assertTrue(task_comment.id is not None)
            self.assertTrue(task_comment.task_id == 1)
            self.assertIsNotNone(task_comment.creation_date)
            self.assertTrue(task_comment.comment == 'comment' or task_comment.comment == 'hello')

    def test_dao_modify_comment(self):
        dao = TaskCommentDAO()
        data1 = dict(
            user_id=1,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(1, 1, data1)

        dao.modify_comment(1, 1, 'modified comment')

        # Verify that task comment was modified
        task_comment = TaskCommentModel.query.filter_by(id=1).first()
        self.assertTrue(task_comment is not None)
        self.assertTrue(task_comment.id is not None)
        self.assertTrue(task_comment.task_id == 1)
        self.assertIsNotNone(task_comment.creation_date)
        self.assertEqual(task_comment.comment, 'modified comment')

    def test_dao_delete_comment(self):
        dao = TaskCommentDAO()
        data1 = dict(
            user_id=1,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(1, 1, data1)

        dao.delete_comment(1, 1)

        # Verify that task comment was deleted
        task_comment = TaskCommentModel.query.filter_by(id=1).first()
        self.assertIsNone(task_comment)


if __name__ == '__main__':
    unittest.main()
