from app.database.sqlalchemy_extension import db
from datetime import datetime
from app.database.db_types.JsonCustomType import JsonCustomType
from enum import unique, Enum


class TaskCommentModel(db.Model):
    """Data Model representation of a task comment.

    Attributes:
        id: integer primary key that defines the task comment.
        user_id: integer indicates id of user.
        task_id: integer indicates id of task.
        creation_date: float that defines the date of creation of the task comment.
        modification_date: float that defines the latest date of modification of the task comment.
        comment: string that defines the comment of task comment.
    """

    # Specifying database table used for Task comment model
    __tablename__ = 'task_comments'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    task_comments = db.Column(JsonCustomType)
    next_task_comment_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    relation_id = db.Column(db.Integer, db.ForeignKey('mentorship_relations.id'))

    def __init__(self, relation_id, task_id, task_comments=None):

        self.relation_id = relation_id
        self.task_id = task_id

        if task_comments is None:
            self.task_comments = []
            self.next_task_comment_id = 1
        else:
            if isinstance(task_comments, list):
                self.task_comments = []
                self.next_task_comment_id = len(task_comments) + 1
            else:
                raise ValueError(TypeError)

    def json(self):
        """Returns information of task comment as a json object."""
        return {
            'id': self.id,
            'task_comments': self.task_comments,
            'next_task_comment_id': self.next_task_comment_id
        }

    @classmethod
    def find_task_comments_list_by_task_id(cls, relation_id, task_id):
        """returns a task_comment_model
           Args:
            relation_id: id of the mentorship relation.
            task_id: id of the task
        """
        comment_list = cls.query.filter_by(relation_id=relation_id, task_id=task_id).first()

        #because task comment is added before a task is created, this creates a new comment_list for pre-existing tasks
        if comment_list is None:
            new_comment_list = TaskCommentModel(relation_id=relation_id, task_id=task_id)
            new_comment_list.save_to_db()

        return cls.query.filter_by(relation_id=relation_id, task_id=task_id).first()

    def add_task_comment(self, comment, user_id, task_id):
        """Adds a new task comment.
           Args:
            task_id: id of the task.
            user_id: id of the user.
            comment: the new comment value.
        """
        task_comment = {
            TaskCommentsFields.ID.value: self.next_task_comment_id,
            TaskCommentsFields.COMMENT.value: comment,
            TaskCommentsFields.CREATION_DATE.value: datetime.now().timestamp(),
            TaskCommentsFields.USER_ID.value: user_id,
            TaskCommentsFields.TASK_ID.value: task_id
        }
        self.next_task_comment_id += 1
        self.task_comments = self.task_comments + [task_comment]
        self.save_to_db()

    def delete_task_comment(self, task_comment_id):
        """deletes a task comment.
           Args:
            task_comment_id: id of the task comment.
        """
        new_list = []
        for task_comment in self.task_comments:
            if task_comment[TaskCommentsFields.ID.value] != task_comment_id:
                new_list = new_list + [task_comment]

        self.task_comments = new_list
        self.save_to_db()

    def find_task_comment_by_id(self, task_comment_id):
        """returns a task comment
           Args:
            task_comment_id: id of the task comment.
        """
        for task_comment in self.task_comments:
            if task_comment[TaskCommentsFields.ID.value] == task_comment_id:
                return task_comment
        return None

    def modify_task_comment(self, task_comment_id, comment):
        """changes the task comment and modification date.
           Args:
            task_comment_id: id of the task comment.
            comment: the new comment value.
        """
        new_list = []
        for task_comment in self.task_comments:
            if task_comment[TaskCommentsFields.ID.value] == task_comment_id:
                new_task_comment = task_comment.copy()
                if comment is not None:
                    new_task_comment[TaskCommentsFields.COMMENT.value] = comment
                    new_task_comment[TaskCommentsFields.MODIFICATION_DATE.value] = datetime.now().timestamp()
                    new_list = new_list + [new_task_comment]
                    continue
            new_list = new_list + [task_comment]

        self.task_comments = new_list
        self.save_to_db()

    def is_empty(self):
        """Returns True if the task comment model is empty, and False otherwise."""
        return len(self.task_comments) == 0

    @classmethod
    def find_by_id(cls, _id):
        """Returns the task comment that has the passed id.
           Args:
                _id: The id of a task comment.
        """
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        """Saves the model to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes the record of task comment from the database."""
        db.session.delete(self)
        db.session.commit()


@unique
class TaskCommentsFields(Enum):
    """Represents a task comment attributes' name.

    Attributes:
        ID: Id of a task comment.
        COMMENT: comment value of a task comment.
        USER_ID: Id of the user who made the comment.
        TASK_ID: Id of the task.
        CREATION_DATE: The date on which the task comment was created.
        MODIFICATION_DATE: The latest date on which the task comment was modified.
    """

    ID = 'id'
    COMMENT = 'comment'
    USER_ID = 'user_id'
    TASK_ID = 'task_id'
    CREATION_DATE = 'creation_date'
    MODIFICATION_DATE = 'modification_date'

    def values(self):
        """Returns a list containing a task."""
        return list(map(str, self))
