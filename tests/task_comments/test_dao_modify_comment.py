import unittest

from tests.task_comments.task_comments_base_setup import TaskCommentsBaseTestCase
from app import messages
from app.api.dao.task_comment import TaskCommentDAO


class TestModifyCommentDao(TaskCommentsBaseTestCase):

    def test_dao_modify_comment(self):
        TaskCommentDAO.modify_comment(
            user_id=1, _id=1, task_id=1, relation_id=2, comment="modified comment"
        )

        # Verify that task comment was modified
        self.assertTrue(self.task_comment is not None)
        self.assertTrue(self.task_comment.id is not None)
        self.assertTrue(self.task_comment.task_id == 1)
        self.assertIsNotNone(self.task_comment.creation_date)
        self.assertEqual(self.task_comment.comment, "modified comment")


if __name__ == "__main__":
    unittest.main()
