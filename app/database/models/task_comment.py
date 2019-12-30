from app.database.sqlalchemy_extension import db
from datetime import datetime


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

    # personal data
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks_list.id'))
    creation_date = db.Column(db.Float, nullable=False)
    modification_date = db.Column(db.Float)
    comment = db.Column(db.String(500), nullable=False)

    def __init__(self, user_id, task_id, comment):
        self.user_id = user_id
        self.task_id = task_id
        self.comment = comment

        self.creation_date = datetime.now().timestamp()

    def json(self):
        """Returns information of task comment as a json object."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'task_id': self.mentor_id,
            'creation_date': self.creation_date,
            'modification_date': self.modification_date,
            'comment': self.comment
        }

    @classmethod
    def find_by_id(cls, _id):
        """Returns the task comment that has the passed id.
           Args:
                _id: The id of a task comment.
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_user_id(cls, user_id):
        """Returns all task comments that has the passed user id.
           Args:
                user_id: The id of the user.
        """
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_task_id(cls, task_id):
        """Returns all task comments that has the passed task id.
           Args:
                task_id: The id of the task.
        """
        return cls.query.filter_by(task_id=task_id).all()

    def modify_task_comment(self, comment):
        """changes the task comment and modification date.
           Args:
                comment: the new comment value.
        """
        self.comment = comment
        self.modification_date = datetime.now().timestamp()

    @classmethod
    def is_empty(cls):
        """Returns True if the task comment model is empty, and False otherwise."""
        return cls.query.first() is None

    def save_to_db(self):
        """Saves the model to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes the record of task comment from the database."""
        db.session.delete(self)
        db.session.commit()
