from datetime import datetime

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.task_comment import TaskCommentModel
from app.utils.decorator_utils import email_verification_required
from app.utils.enum_utils import MentorshipRelationState
from app.database.models.task_comment import TaskCommentsFields


class TaskCommentDAO:
    """Data Access Object for Task comment functionalities."""

    @staticmethod
    @email_verification_required
    def create_task_comment(relation_id, user_id, task_id, data):
        """Creates a new task.

        Creates a new task comment,

        Args:
            relation_id: The id of the mentorship relation.
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

        relation = MentorshipRelationModel.find_by_id(_id=relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if relation.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, 400

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, 404

        comment = data['comment']

        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=relation_id,
                                                                                 task_id=task_id)
        task_comments_list.add_task_comment(comment=comment, user_id=user_id, task_id=task_id)

        return messages.TASK_COMMENT_WAS_CREATED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def get_task_comments_by_task_id(user_id, task_id, relation_id):
        """Gets task comment of specified task_id

        Gets task comment.

        Args:
            user_id: The id of the user.
            relation_id: The id of the mentorship relation.
            task_id: The id of the task.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if retrieving the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        relation = MentorshipRelationModel.find_by_id(_id=relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if relation.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, 400

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION, 401

        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=relation_id,
                                                                                 task_id=task_id)

        return task_comments_list.task_comments

    @staticmethod
    @email_verification_required
    def modify_comment(user_id, _id, comment, relation_id, task_id):
        """Modifies task comment to new comment

        Modifies task comment to new task comment.

        Args:
            relation_id: id of mentorship relation.
            task_id: id of task.
            user_id: id of the user trying to modify the task comment.
            _id: id of task comment.
            comment: new comment value.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if modifying the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        relation = MentorshipRelationModel.find_by_id(_id=relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if relation.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, 400

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION, 401

        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=relation_id,
                                                                                 task_id=task_id)
        task_comment = task_comments_list.find_task_comment_by_id(task_comment_id=_id)

        if task_comment:
            if task_comment[TaskCommentsFields.USER_ID.value] == user_id:
                task_comments_list.modify_task_comment(comment=comment, task_comment_id=_id)
                return messages.TASK_COMMENT_WAS_MODIFIED_SUCCESSFULLY, 200
            else:
                return messages.USER_CANT_MODIFY_TASK_COMMENT_NOT_MADE_BY_USER, 401

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404

    @staticmethod
    @email_verification_required
    def delete_comment(user_id, _id, task_id, relation_id):
        """Deletes the specified task comment

        Deletes task comment with specified id.

        Args:
            relation_id: id of mentorship relation.
            task_id: id of task.
            user_id: id of user trying to delete the task comment.
            _id: id of task comment.

        Returns:
            A two element list where the first element is a dictionary,
            containing a key 'message' indicating in its value
            if deleting the task comment was successful or not as a string.
            The last element is the HTTP
            response code.
        """

        relation = MentorshipRelationModel.find_by_id(_id=relation_id)
        if relation is None:
            return messages.MENTORSHIP_RELATION_DOES_NOT_EXIST, 404

        if relation.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, 400

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return messages.TASK_DOES_NOT_EXIST, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return messages.USER_NOT_INVOLVED_IN_THIS_MENTOR_RELATION, 401

        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=relation_id,
                                                                                 task_id=task_id)
        task_comment = task_comments_list.find_task_comment_by_id(task_comment_id=_id)

        if task_comment:
            if task_comment[TaskCommentsFields.USER_ID.value] == user_id:
                task_comments_list.delete_task_comment(task_comment_id=_id)
                return messages.TASK_COMMENT_WAS_DELETED_SUCCESSFULLY, 200
            else:
                return messages.USER_CANT_DELETE_TASK_COMMENT_NOT_MADE_BY_USER, 401

        return messages.TASK_COMMENT_DOES_NOT_EXIST, 404
