from datetime import datetime

from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.user import UserModel
from app.utils.enum_utils import MentorshipRelationState


class TaskDAO:
    """Data Access Object for Task functionalities."""

    @staticmethod
    def create_task(user_id, mentorship_relation_id, data):
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

        description = data['description']

        user = UserModel.find_by_id(user_id)
        if user is None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(_id=mentorship_relation_id)
        if relation is None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        if relation.state is not MentorshipRelationState.ACCEPTED:
            return {'message': 'Mentorship relation is not in the accepted state.'}, 400

        now_timestamp = datetime.now().timestamp()
        relation.tasks_list.add_task(description=description, created_at=now_timestamp)
        relation.tasks_list.save_to_db()

        return {"message": "Task was created successfully."}, 200

    @staticmethod
    def list_tasks(user_id, mentorship_relation_id):
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
        if user is None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        if not (user_id is relation.mentee_id or user_id is relation.mentor_id):
            return {'message': 'You are not involved in this mentorship relation.'}, 401

        all_tasks = relation.tasks_list.tasks

        return all_tasks

    @staticmethod
    def delete_task(user_id, mentorship_relation_id, task_id):
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
        if user is None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return {'message': 'Task does not exist.'}, 404

        if not (user_id is relation.mentee_id or user_id is relation.mentor_id):
            return {'message': 'You are not involved in this mentorship relation.'}, 401

        relation.tasks_list.delete_task(task_id)

        return {'message': 'Task was deleted successfully.'}, 200

    @staticmethod
    def complete_task(user_id, mentorship_relation_id, task_id):
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
        if user is None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        if not (user_id is relation.mentee_id or user_id is relation.mentor_id):
            return {'message': 'You are not involved in this mentorship relation.'}, 401

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return {'message': 'Task does not exist.'}, 404

        if task.get('is_done'):
            return {'message': 'Task was already achieved.'}, 400
        else:
            relation.tasks_list.update_task(
                task_id=task_id, is_done=True, completed_at=datetime.now().timestamp())

        return {'message': 'Task was achieved successfully.'}, 200
