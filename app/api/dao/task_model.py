from app import messages
from app.database.models.task_comment import TaskCommentModel
from app.utils.decorator_utils import email_verification_required


class TaskCommentDAO:
    """Data Access Object for task comment functionalities."""

    @staticmethod
    @email_verification_required
    def create_task_comment(user_id, data):
        """Creates a new task comment.

        Creates a new task comment with provided data.

        Arguments:
            user_id: The id of the user.
            data: A list containing the task's id and a comment.

        Returns:
            A tuple with two elements.
            The first element is a dictionary containing a key 'message'
            containing a string which indicates whether or not the task comment
            was created successfully.
            The second is the HTTP response code.
        """

        task_id = data['task_id']
        comment = data['comment']

        task_comment = TaskCommentModel(task_id, user_id, comment)
        task_comment.save_to_db()

        return messages.TASK_COMMENT_WAS_CREATED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def get_task_comment(user_id, _id):
        """Returns the task comment suing specified id.

        Arguments:
            user_id: The id of the user.
            _id: The id of the task comment.

        Returns:
            A tuple with two elements.
            The task comment that has given id and the HTTP response code.
        """

        task_comment = TaskCommentModel.find_by_id(_id)

        if task_comment:
            return task_comment, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404

    @staticmethod
    @email_verification_required
    def get_all_task_comments_by_task_id(user_id, task_id):
        """Returns all the task comments using specified task id.

        Arguments:
            user_id: The id of the user.
            task_id: The id of the task.

        Returns:
            A tuple with two elements.
            The list of task comments that have given task id
            and the HTTP response code.
        """

        return TaskCommentModel.find_all_by_task_id(task_id), 200

    @staticmethod
    @email_verification_required
    def get_all_task_comments_by_user_id(user_id):
        """Returns all the task comments using specified user id.

        Arguments:
            user_id: The id of the user.

        Returns:
            A tuple with two elements.
            The list of task comments that have given user id
            and the HTTP response code.
        """

        return TaskCommentModel.find_all_by_task_id(user_id), 200

    @staticmethod
    @email_verification_required
    def modify_comment(user_id, _id, comment):
        """Modifies comment to a new one.

        Arguments:
            user_id: The id of the user.
            _id: The id of the task comment.
            comment: New comment.

        Returns:
            A tuple with two elements.
            The first element is a dictionary containing a key 'message'
            containing a string which indicates whether or not the task comment
            was updated successfully.
            The second is the HTTP response code.
        """

        task_comment = TaskCommentModel.find_by_id(_id)
        task_comment.modify_comment(comment)
        task_comment.save_to_db()

        return messages.TASK_COMMENT_WAS_UPDATED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def delete_comment(user_id, _id):
        """Deletes comment specified by id.

        Arguments:
            user_id: The id of the user.
            _id: The id of the task comment.

        Returns:
            A tuple with two elements.
            The first element is a dictionary containing a key 'message'
            containing a string which indicates whether or not the task comment
            was deleted successfully.
            The second is the HTTP response code.
        """

        task_comment = TaskCommentModel.find_by_id(_id)

        if task_comment:
            task_comment.delete_from_db()
            return messages.TASK_COMMENT_WAS_DELETED_SUCCESSFULLY, 200

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404
