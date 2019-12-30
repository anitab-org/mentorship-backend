from datetime import datetime

from app import messages
from app.database.models.task_comment import TaskCommentModel
from app.utils.decorator_utils import email_verification_required


class TaskCommentDAO:
    """Data Access Object for Task comment functionalities."""

    @staticmethod
    @email_verification_required
    def create_task_comment(user_id, task_id, data):
        """Creates a new task.

        Creates a new task comment,

        Args:
            user_id: The id of the user.
            task_id: The id of the task relation.
            data: A list containing the comment of the task comment.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if the task comment creation was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        comment = data['comment']

        task_comment = TaskCommentModel(user_id=user_id, task_id=task_id, comment=comment)
        if task_comment:
            task_comment.save_to_db()

        return messages.TASK_COMMENT_WAS_CREATED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def get_task_comment(user_id, _id):
        """Gets task comment of specified id

        Gets task comment.

        Args:
            user_id: The id of the user.
            _id: The id of the task comment.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if retrieving the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        task_comment = TaskCommentModel.find_by_id(_id)

        if task_comment:
            return task_comment, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404

    @staticmethod
    @email_verification_required
    def get_task_comments_by_user_id(user_id):
        """Gets task comment of specified user_id

        Gets task comment.

        Args:
            user_id: The id of the user.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if retrieving the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        task_comment = TaskCommentModel.find_by_user_id(user_id)

        if task_comment:
            return task_comment, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404

    @staticmethod
    @email_verification_required
    def get_task_comments_by_task_id(user_id, task_id):
        """Gets task comment of specified task_id

        Gets task comment.

        Args:
            user_id: The id of the user.
            task_id: The id of the task.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if retrieving the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        task_comment = TaskCommentModel.find_by_task_id(task_id)

        if task_comment:
            return task_comment, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404

    @staticmethod
    @email_verification_required
    def modify_comment(user_id, _id, comment):
        """Modifies task comment to new comment

        Modifies task comment to new task comment.

        Args:
            user_id: The id of the user.
            _id: id of task comment.
            comment: new comment value.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if modifying the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        task_comment = TaskCommentModel.find_by_id(_id)

        if task_comment:
            task_comment.modify_task_comment(comment)
            task_comment.save_to_db()
            return messages.TASK_COMMENT_WAS_MODIFIED_SUCCESSFULLY, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404

    @staticmethod
    @email_verification_required
    def delete_comment(user_id, _id):
        """Deletes the specified task comment

        Deletes task comment with specified id.

        Args:
            user_id: The id of the user.
            _id: id of task comment.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if deleting the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        task_comment = TaskCommentModel.find_by_id(_id)

        if task_comment:
            task_comment.delete_from_db()
            return messages.TASK_COMMENT_WAS_DELETED_SUCCESSFULLY, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404
