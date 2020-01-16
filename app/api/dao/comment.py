from datetime import datetime, timedelta

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.task_comment import TaskCommentModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.utils.decorator_utils import email_verification_required
from app.utils.enum_utils import MentorshipRelationState
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.api.dao.task import TaskDAO

class CommentDAO:
    """Data Access Object for task comment functionalities.

    Provides various functions pertaining to task comments.
    """

    @staticmethod
    @email_verification_required
    def create_task_comment(user_id, request_id, task_id, data):
        """Creates a comment for a task.

        Args:
            user_id: ID of the user adding comment. Has to be either the mentor or the mentee.
            request_id: ID user's mentorship relation.
            task_id: ID of the task for which comment is added.
            data: Dict containing the comment.

        Returns:
            message: A message corresponding to the completed action; success if comment is added, failure if otherwise.
        """
        comment = data['comment']
        task_list = TaskDAO.list_tasks(user_id, request_id)

        # task_list contains either list of tasks or 401 / 404 errors
        if isinstance(task_list, list):
            for task in task_list:
                # see if task_id exists
                if task["id"] == task_id:
                    task_comment = TaskCommentModel(
                        request_id = request_id,
                        task_id = task_id,
                        user_id = user_id,
                        comment = comment
                    )
                    task_comment.save_to_db()
                    return messages.COMMENT_WAS_CREATED_SUCCESSFULLY, 200

            return messages.TASK_DOES_NOT_EXIST, 404
        return task_list #returns error

    @staticmethod
    @email_verification_required
    def get_task_comments(user_id, request_id, task_id):
        """Gives comments for specified request and task ID

        Args:
            user_id: ID of the user adding comment. Has to be either the mentor or the mentee.
            request_id: ID user's mentorship relation.
            task_id: ID of the task for which comment is added.

        Returns:
            A list containing all the comments one user has in a task. otherwise, it returns a two element list where the first element is
            a dictionary containing a key 'message' indicating in its value if there were any problem finding user's tasks in the specified
            mentorship relation as a string. The last element is the HTTP response code
        """
        #check if task exists, else give error
        task_list = TaskDAO.list_tasks(user_id, request_id)
        # task_list contains either list of tasks or 401 / 404 errors
        if isinstance(task_list, list):
            for task in task_list:
                # see if task_id exists
                if task["id"] == task_id:
                    comments_list = []
                    comments = TaskCommentModel.find_by_request_and_task(request_id, task_id)
                    for comment in comments:
                        comments_list += [comment.json()]
                    return comments_list, 200

            return messages.TASK_DOES_NOT_EXIST, 404
        return task_list #returns error

    @staticmethod
    @email_verification_required
    def get_task_comment(user_id, request_id, task_id, comment_id):
        """Gives comment for specified request, task and comment ID

        Args:
            user_id: ID of the user adding comment. Has to be either the mentor or the mentee.
            request_id: ID user's mentorship relation.
            task_id: ID of the task for which comment is added.
            comment_id: ID of comment to be searched.

        Returns:
            Returns a dictionary containing details of a comment for specified parameters.
            otherwise, it returns a two element list where the first element is
            a dictionary containing a key 'message' indicating in its value if
            there were any problem finding user's tasks in the specified
            mentorship relation as a string. The last element is the HTTP response code
        """

        #check if task exists, else give error
        task_list = TaskDAO.list_tasks(user_id, request_id)
        # task_list contains either list of tasks or 401 / 404 errors
        if isinstance(task_list, list):
            for task in task_list:
                # see if task_id exists
                if task["id"] == task_id:
                    #search only if user_id, request_id and task_id are valid
                    comment = TaskCommentModel.find_by_id(comment_id)
                    if comment is not None:
                        return comment.json(), 200
                    else:
                        return messages.COMMENT_DOES_NOT_EXIST, 404

            return messages.TASK_DOES_NOT_EXIST, 404
        return task_list #returns error

    @staticmethod
    @email_verification_required
    def delete_task_comment(user_id, request_id, task_id, comment_id):
        """Deletes comment for specified request, task and comment ID

        Args:
            user_id: ID of the user adding comment. Has to be either the mentor or the mentee.
            request_id: ID user's mentorship relation.
            task_id: ID of the task for which comment is added.
            comment_id: ID of comment to be searched.

        Returns:
            Returns a two element list with success message and response code for deletion.
            otherwise, it returns a two element list where the first element is
            a dictionary containing a key 'message' indicating in its value if
            there were any problem finding user's tasks in the specified
            mentorship relation as a string. The last element is the HTTP response code
        """

        #check if task exists, else give error
        task_list = TaskDAO.list_tasks(user_id, request_id)
        # task_list contains either list of tasks or 401 / 404 errors
        if isinstance(task_list, list):
            for task in task_list:
                # see if task_id exists
                if task["id"] == task_id:
                    #search only if user_id, request_id and task_id are valid
                    comment = TaskCommentModel.find_by_id(comment_id)

                    if comment is not None:
                        comment.delete_from_db()
                        return messages.COMMENT_WAS_DELETED_SUCCESSFULLY, 200
                    else:
                        return messages.COMMENT_DOES_NOT_EXIST, 404

            return messages.TASK_DOES_NOT_EXIST, 404
        return task_list #returns error

    @staticmethod
    @email_verification_required
    def update_task_comment(user_id, request_id, task_id, comment_id, updated_comment):
        """Updates comment for specified request, task and comment ID

        Args:
            user_id: ID of the user adding comment. Has to be either the mentor or the mentee.
            request_id: ID user's mentorship relation.
            task_id: ID of the task for which comment is added.
            comment_id: ID of comment to be searched.

        Returns:
            Returns a two element list with success message and response code for updation.
            otherwise, it returns a two element list where the first element is
            a dictionary containing a key 'message' indicating in its value if
            there were any problem finding user's tasks in the specified
            mentorship relation as a string. The last element is the HTTP response code
        """

        #check if task exists, else give error
        task_list = TaskDAO.list_tasks(user_id, request_id)
        # task_list contains either list of tasks or 401 / 404 errors
        if isinstance(task_list, list):
            for task in task_list:
                # see if task_id exists
                if task["id"] == task_id:
                    #search only if user_id, request_id and task_id are valid
                    comment = TaskCommentModel.find_by_id(comment_id)
                    if comment is not None:
                        comment.edit_comment(updated_comment)
                        return messages.UPDATED_COMMENT_WITH_SUCCESS, 200
                    else:
                        return messages.COMMENT_DOES_NOT_EXIST, 404

            return messages.TASK_DOES_NOT_EXIST, 404
        return task_list #returns error
