from enum import unique, Enum

from app.database.db_types.JsonCustomType import JsonCustomType
from app.database.sqlalchemy_extension import db
from datetime import date


class TasksListModel(db.Model):
    """Model representation of a list of tasks.

    Attributes:
        id: Id of the list of tasks.
        tasks: A list of tasks, using JSON format.
        next_task_id: Id of the next task added to the list of tasks.
    """

    __tablename__ = "tasks_list"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(JsonCustomType)
    next_task_id = db.Column(db.Integer)

    def __init__(self, tasks: "TasksListModel" = None):
        """Initializes tasks.

        Args:
            tasks: A list of tasks.

        Raises:
            A Value Error if the task is not initialized.
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

    def add_task(
        self, description: str, created_at: date, is_done=False, completed_at=None
    ) -> None:
        """Adds a task to the list of tasks.

        Args:
            description: A description of the task added.
            created_at: Date on which the task is created.
            is_done: Boolean specifying completion of the task.
            completed_at: Date on which task is completed.
        """

        task = {
            TasksFields.ID.value: self.next_task_id,
            TasksFields.DESCRIPTION.value: description,
            TasksFields.IS_DONE.value: is_done,
            TasksFields.CREATED_AT.value: created_at,
            TasksFields.COMPLETED_AT.value: completed_at,
        }
        self.next_task_id += 1
        self.tasks = self.tasks + [task]

    def delete_task(self, task_id: int) -> None:
        """Deletes a task from the list of tasks.

        Args:
            task_id: Id of the task to be deleted.
        """

        new_list = list(
            filter(lambda task: task[TasksFields.ID.value] != task_id, self.tasks)
        )

        self.tasks = new_list
        self.save_to_db()

    def update_task(
        self,
        task_id: int,
        description: str = None,
        is_done: bool = None,
        completed_at: date = None,
    ) -> None:
        """Updates a task.

        Args:
            task_id: Id of the task to be updated.
            description: A description of the task.
            created_at: Date on which the task is created.
            is_done: Boolean specifying completion of the task.
            completed_at: Date on which task is completed.
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

    def find_task_by_id(self, task_id: int):
        """Returns the task that has the specified id.

        Args:
            task_id: Id of the task.

        Returns:
            The task instance.
        """
        task = list(
            filter(lambda task: task[TasksFields.ID.value] == task_id, self.tasks)
        )
        if len(task) == 0:
            return None
        else:
            return task[0]

    def is_empty(self) -> bool:
        """Checks if the list of tasks is empty.

        Returns:
            Boolean; True if the task is empty, False otherwise.
        """

        return len(self.tasks) == 0

    def json(self):
        """Creates json object of the attributes of list of tasks.

        Returns:
            Json objects of attributes of list of tasks.
        """

        return {
            "id": self.id,
            "mentorship_relation_id": self.mentorship_relation_id,
            "tasks": self.tasks,
            "next_task_id": self.next_task_id,
        }

    def __repr__(self):
        """Creates a representation of an object.

        Returns:
            A string representation of the task object.
        """

        return f"Task | id = {self.id}; tasks = {self.tasks}; next task id = {self.next_task_id}"

    @classmethod
    def find_by_id(cls, _id: int):
        """Finds a task with the specified id.

        Returns:
            The task with the specified id.
        """

        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        """Adds a task to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        """Deletes a task from the database."""
        db.session.delete(self)
        db.session.commit()


@unique
class TasksFields(Enum):
    """Represents a task attributes' name.

    Attributes:
        ID: Id of a task.
        DESCRIPTION: Description of a task.
        IS_DONE: Boolean specifying the completion of the task.
        COMPLETED_AT: The date on which the task is completed.
        CREATED_AT: The date on which the task was created.
    """

    ID = "id"
    DESCRIPTION = "description"
    IS_DONE = "is_done"
    COMPLETED_AT = "completed_at"
    CREATED_AT = "created_at"

    def values(self):
        """Returns a list containing a task."""
        return list(map(str, self))
