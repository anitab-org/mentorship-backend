from enum import unique, Enum

from app.database.db_types.JsonCustomType import JsonCustomType
from app.database.sqlalchemy_extension import db


class TasksListModel(db.Model):
    """Model for mentorship relation tasks functionalities.

    Provides various functions pertaining to mentorship relation tasks.

    Attributes:
        id
        tasks
        next_task_id
    """

    __tablename__ = 'tasks_list'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(JsonCustomType)
    next_task_id = db.Column(db.Integer)

    def __init__(self, tasks=None):
        """Initializes tasks and next_task_id.

        Args:
            tasks: List of mentorship relation tasks.
        """

        if tasks is None:
            self.tasks = []
            self.next_task_id = 1
        else:
            if isinstance(tasks, list):
                self.tasks = []
                self.next_task_id = len(tasks) + 1
            else:
                raise ValueError(TypeError)

    def add_task(self, description, created_at, is_done=False, completed_at=None):
        """Adds a mentorship relation task to the list of tasks.

        Args:
            description: Description of the mentorship relation task to be added.
            created_at: Task creation date.
            is_done: An indication that the task is done.
            completed_at: Task completion date.
        """

        task = {
            TasksFields.ID.value: self.next_task_id,
            TasksFields.DESCRIPTION.value: description,
            TasksFields.IS_DONE.value: is_done,
            TasksFields.CREATED_AT.value: created_at,
            TasksFields.COMPLETED_AT.value: completed_at
        }
        self.next_task_id += 1
        self.tasks = self.tasks + [task]

    def delete_task(self, task_id):
        """Deletes a mentorship relation task from the list of tasks.

        Args:
            task_id: ID of the mentorship relation task to be deleted.
        """

        new_list = []
        for task in self.tasks:
            if task[TasksFields.ID.value] != task_id:
                new_list = new_list + [task]

        self.tasks = new_list
        self.save_to_db()

    def update_task(self, task_id, description=None, is_done=None, completed_at=None):
        """Updates a mentorship relation task.

        Args:
            task_id: ID of the mentorship relation task to be updated.
            description: Description of the mentorship relation task to be updated.
            is_done: An indication that the task is done.
            completed_at: Task completion date.
        """

        new_list = []
        for task in self.tasks:
            if task[TasksFields.ID.value] == task_id:
                new_task = task.copy()
                if description is not None:
                    new_task[TasksFields.DESCRIPTION.value] = description

                if is_done is not None:
                    new_task[TasksFields.IS_DONE.value] = is_done

                if completed_at is not None:
                    new_task[TasksFields.COMPLETED_AT.value] = completed_at

                new_list = new_list + [new_task]
                continue

            new_list = new_list + [task]

        self.tasks = new_list
        self.save_to_db()

    def find_task_by_id(self, task_id):
        """Finds a mentorship relation task.

        Args:
            task_id: ID of the mentorship relation task to be found.

        Returns:
            task: A mentorship relation task corresponding to the task_id.
        """

        for task in self.tasks:
            if task[TasksFields.ID.value] == task_id:
                return task
        return None

    def is_empty(self):
        """Checks if the list of mentorship relation tasks is empty.

        Returns:
            A boolean value; True or False.
        """

        return len(self.tasks) == 0

    def json(self):
        """Creates a json string.

        Returns:
            A json string of the various task attributes.
        """

        return {
            'id': self.id,
            'mentorship_relation_id': self.mentorship_relation_id,
            'tasks': self.tasks,
            'next_task_id': self.next_task_id
        }

    def __repr__(self):
        """Creates a printable representation of an object.

        Returns:
            A string containing a printable representation of a mentorship relation task.
        """
        return "Task | id = %s; tasks = %s; next task id = %s" % (self.id, self.tasks, self.next_task_id)

    @classmethod
    def find_by_id(cls, _id):
        """Finds a mentorship relation task.
        """
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        """Adds a mentorship relation task to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Deletes a mentorship relation task from the database.
        """
        db.session.delete(self)
        db.session.commit()


@unique
class TasksFields(Enum):
    """Represents a database table column.

    Attributes:
        ID
        DESCRIPTION
        IS_DONE
        COMPLETED_AT
        CREATED_AT
    """

    ID = 'id'
    DESCRIPTION = 'description'
    IS_DONE = 'is_done'
    COMPLETED_AT = 'completed_at'
    CREATED_AT = 'created_at'

    def values(self):
        """Returns a list containing a mentorship relation task.
        """
        return list(map(str, self))
