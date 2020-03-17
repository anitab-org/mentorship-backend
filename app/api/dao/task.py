from datetime import datetime
from typing import Dict

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.user import UserModel
from app.utils.decorator_utils import email_verification_required
from app.utils.enum_utils import MentorshipRelationState


class TaskDAO:
    """Data Access Object for Task functionalities."""

    @staticmethod
    @email_verification_required
    def create_task(user_id: int, mentorship_relation_id: int, data: Dict[str, str]):
        """Creates a new task.

        Creates a new task in a mentorship relation if the specified user is already involved in it.

        Args:
            user_id: The id of the user.
            mentorship_relation_id: The id of the mentorship relation.
            data: A list containing the description of the task.

        Returns:
            A two element list where the first element is a dictionary containing a key 'message' indicating
            in its value if the task creation was succesful or not as a string. The last element is the HTTP
            response code.
        """

        description = data["description"]

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(_id=mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if relation.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, 400

        now_timestamp = datetime.now().timestamp()
        relation.tasks_list.add_task(description=description, created_at=now_timestamp)
        relation.tasks_list.save_to_db()

        return messages.TASK_WAS_CREATED_SUCCESSFULLY, 201

    @staticmethod
    @email_verification_required
    def list_tasks(user_id: int, mentorship_relation_id: int):
        """Retrieves all tasks of a user in a mentorship relation.

        Lists all tasks from a mentorship relation for the specified user if the user is involved in a current mentorship relation.

        Args:
            user_id: The id of the user.
            mentorship_relation_id: The id of the mentorship relation.

        Returns:
            A list containing all the tasks one user has in a mentorship relation. otherwise, it returns a two element list where the first element is
            a dictionary containing a key 'message' indicating in its value if there were any problem finding user's tasks in the specified
            mentorship relation as a string. The last element is the HTTP response code
        """

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION, 401

        all_tasks = relation.tasks_list.tasks

        return all_tasks

    @staticmethod
    @email_verification_required
    def delete_task(user_id: int, mentorship_relation_id: int, task_id: int):
        """Deletes a specified task from a mentorship relation.

        Deletes a task that belongs to a user who is involved in the specified
        mentorship relation.

        Args:
            user_id: The id of the user.
            mentorship_relation_id: The id of the mentorship relation.
            task_id: The id of the task.

        Returns:
            A two element list where the first element is a dictionary containing a key 'message' indicating in its value if the
            task was deleted succesfully or not as a string. The last element is the HTTP response code.
        """

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION, 401

        relation.tasks_list.delete_task(task_id)

        return messages.TASK_WAS_DELETED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def complete_task(user_id: int, mentorship_relation_id: int, task_id: int):
        """Marks a task as completed.

        Updates the task that belongs to a user who is involved in the specified
        mentorship relation to finished task status.

        Args:
            user_id: The id of the user.
            mentorship_relation_id: The id of the mentorship relation.
            task_id: The id of the task.

        Returns:
            A two element list where the first element is a dictionary containing a key 'message' indicating in its value
            if the task was set to complete succesfully or not as a string. The last element is the HTTP response code.
        """

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION, 401

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, 404

        if task.get("is_done"):
            return messages.TASK_WAS_ALREADY_ACHIEVED, 400
        else:
            relation.tasks_list.update_task(
                task_id=task_id, is_done=True, completed_at=datetime.now().timestamp()
            )

        return messages.TASK_WAS_ACHIEVED_SUCCESSFULLY, 200
