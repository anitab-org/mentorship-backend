from tests.tasks.tasks_base_setup import TasksBaseTestCase
from app.database.sqlalchemy_extension import db
from app.api.dao.task_comment import TaskCommentDAO

class TaskCommentsBaseTestCase(TasksBaseTestCase):
    def setUp(self):
        super().setUp()

        dao = TaskCommentDAO()
        self.comment= dao.create_task_comment(user_id=1, task_id=1, relation_id=2, comment="comment")
        self.task_comment = TaskCommentDAO.get_task_comment(1, 1)[0]
        db.session.add(self.task_comment)
        db.session.commit()
