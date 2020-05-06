import unittest

from tests.task_comments.task_comments_base_setup import TaskCommentsBaseTestCase
from app import messages
from app.api.dao.task_comment import TaskCommentDAO


class TestFindByTaskIdDao(TaskCommentsBaseTestCase):

    def test_dao_find_by_task_id(self):
        # Verify that find_all_by_task_id() function is working properly
        task_comments = TaskCommentDAO.get_all_task_comments_by_task_id(
            user_id=1, task_id=1, relation_id=2
        )[0]
        task_comment = self.task_comment.json()
        self.assertEqual(task_comment, task_comments)


if __name__ == "__main__":
    unittest.main()
