import unittest

from tests.task_comments.task_comments_base_setup import TaskCommentsBaseTestCase
from app import messages
from app.api.dao.task_comment import TaskCommentDAO


class TestModifyCommentDao(TaskCommentsBaseTestCase):

    def test_dao_delete_comment(self):
        TaskCommentDAO.delete_comment(user_id=1, _id=1, task_id=1, relation_id=2)

        expected_response = messages.TASK_COMMENT_DOES_NOT_EXIST, 404
        actual_response = TaskCommentDAO.get_task_comment(1, 1)

        # Verify that task comment was deleted
        self.assertEqual(expected_response, actual_response)


if __name__ == "__main__":
    unittest.main()
