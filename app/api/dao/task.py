from datetime import datetime
from typing import Dict
from http import HTTPStatus
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
            in its value if the task creation was successful or not as a string. The last element is the HTTP
            response code.
        """

        description = data["description"]

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(_id=mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        if relation.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, HTTPStatus.FORBIDDEN

        if (relation.mentor_id != user_id) and (relation.mentee_id != user_id):
            return (
                messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION,
                HTTPStatus.FORBIDDEN,
            )

        now_timestamp = datetime.utcnow().timestamp()
        relation.tasks_list.add_task(description=description, created_at=now_timestamp)
        relation.tasks_list.save_to_db()

        return messages.TASK_WAS_CREATED_SUCCESSFULLY, HTTPStatus.CREATED

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
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return (
                messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION,
                HTTPStatus.UNAUTHORIZED,
            )

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
            task was deleted successfully or not as a string. The last element is the HTTP response code.
        """

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return (
                messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION,
                HTTPStatus.UNAUTHORIZED,
            )

        relation.tasks_list.delete_task(task_id)

        return messages.TASK_WAS_DELETED_SUCCESSFULLY, HTTPStatus.OK

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
            if the task was set to complete successfully or not as a string. The last element is the HTTP response code.
        """

        user = UserModel.find_by_id(user_id)
        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return (
                messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION,
                HTTPStatus.UNAUTHORIZED,
            )

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

        if task.get("is_done"):
            return messages.TASK_WAS_ALREADY_ACHIEVED, HTTPStatus.CONFLICT
        else:
            relation.tasks_list.update_task(
                task_id=task_id,
                is_done=True,
                completed_at=datetime.utcnow().timestamp(),
            )

        return messages.TASK_WAS_ACHIEVED_SUCCESSFULLY, HTTPStatus.OK
