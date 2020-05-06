import unittest

from tests.task_comments.task_comments_base_setup import TaskCommentsBaseTestCase
from app import messages
from app.api.dao.task_comment import TaskCommentDAO


class TestCreateTaskCommentDao(TaskCommentsBaseTestCase):

    def test_dao_create_task_comment(self):
        # Verify that task comment was inserted in database through DAO
        self.assertTrue(self.task_comment is not None)
        self.assertTrue(self.task_comment.id is not None)
        self.assertTrue(self.task_comment.task_id == 1)
        self.assertIsNotNone(self.task_comment.creation_date)
        self.assertEqual(self.task_comment.comment, "comment")


if __name__ == "__main__":
    unittest.main()
