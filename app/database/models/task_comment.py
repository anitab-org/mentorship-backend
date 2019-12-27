from werkzeug.security import generate_password_hash, check_password_hash
import time
from app.database.sqlalchemy_extension import db

class TaskCommentModel(db.Model):
    """Defines attributes for task comment.

    Attributes:
        id: ID of task comment
        task id: ID of a task
        user id: ID of user commenting on task
        creation time
        modification time
        comment: A string storing comment made on task
    """
    # Specifying database table used for TaskCommentModel
    __tablename__ = 'task_comment'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)
    creation_time = db.Column(db.Float, nullable=False)
    modification_time = db.Column(db.Float)
    comment = db.Column(db.String, nullable=False)

    def __init__(self, task_id, user_id, comment):
        """"Initialises TaskCommentModel class with task_id, user_id, and comment. """
        ## required fields
        self.task_id = task_id
        self.user_id = user_id
        self.creation_time = creation_time
        self.comment = comment
        self.creation_time = time.time()

    def json(self):
        """Returns TaskCommentModel object in json format."""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'creation_time': self.creation_time,
            'modification_time': self.modification_time,
            'comment': self.comment
        }

    def __repr__(self):
        """Creates a representation of an object.

        Returns:
            A string representation of comment.
        """

        return """Comment | id = %s; task_id = %s; user_id = %s; creation_time = %s;
        modification_time = %s; comment = %s""" % (
            self.id, self.task_id, self.user_id, self.creation_time, self.modification_time, self.comment
            )

    @classmethod
    def find_by_id(cls, _id):
        """Finds a comment with the specified id.

        Returns:
            The comment with the specified id.
        """

        return cls.query.filter_by(id=_id).first()

    @classmethod
    def is_empty(cls):
        """Returns a boolean if the TaskCommentModel is empty or not. """
        return cls.query.first() is None

    def save_to_db(self):
        """Adds a comment to the database. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes a comment from the database. """
        db.session.delete(self)
        db.session.commit()

    def edit_comment(self, id, comment):
        """Edits a comment in the database. """
        row = find_by_id(self, id)
        row.comment = comment
        row.modification_time=time.time()
        db.session.commit()
