from datetime import datetime

from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.user import UserModel
from app.utils.enum_utils import MentorshipRelationState
from app import constants


class TaskDAO:

    @staticmethod
    def create_task(user_id, mentorship_relation_id, data):
        description = data['description']

        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"message": USER_DOES_NOT_EXIST }, 404

        relation = MentorshipRelationModel.find_by_id(_id=mentorship_relation_id)
        if relation is None:
            return {"message": MENTORSHIP_RELATION_DOES_NOT_EXIST }, 404

        if relation.state is not MentorshipRelationState.ACCEPTED:
            return {"message": MENTORSHIP_RELATION_IS_NOT_IN_ACCEPTED_STATE }, 400

        now_timestamp = datetime.now().timestamp()
        relation.tasks_list.add_task(description=description, created_at=now_timestamp)
        relation.tasks_list.save_to_db()

        return {"message": TASK_WAS_CREATED_SUCCESSFULLY }, 200

    @staticmethod
    def list_tasks(user_id, mentorship_relation_id):

        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"message": USER_DOES_NOT_EXIST }, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return {"message": MENTORSHIP_RELATION_DOES_NOT_EXIST }, 404

        if not (user_id is relation.mentee_id or user_id is relation.mentor_id):
            return {"message": USER_IS_NOT_INVOLVED_IN_THIS_MENTORSHIP_RELATION }, 401

        all_tasks = relation.tasks_list.tasks

        return all_tasks

    @staticmethod
    def delete_task(user_id, mentorship_relation_id, task_id):

        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"message": USER_DOES_NOT_EXIST }, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return {"message": MENTORSHIP_RELATION_DOES_NOT_EXIST }, 404

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return {"message": TASK_DOES_NOT_EXIST }, 404

        if not (user_id is relation.mentee_id or user_id is relation.mentor_id):
            return {"message": USER_IS_NOT_INVOLVED_IN_THIS_MENTORSHIP_RELATION }, 401

        relation.tasks_list.delete_task(task_id)

        return {"message": TASK_WAS_DELETED_SUCCESSFULLY }, 200

    @staticmethod
    def complete_task(user_id, mentorship_relation_id, task_id):

        user = UserModel.find_by_id(user_id)
        if user is None:
            return {"message": USER_DOES_NOT_EXIST }, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation is None:
            return {"message": MENTORSHIP_RELATION_DOES_NOT_EXIST }, 404

        if not (user_id is relation.mentee_id or user_id is relation.mentor_id):
            return {"message": USER_IS_NOT_INVOLVED_IN_THIS_MENTORSHIP_RELATION }, 401

        task = relation.tasks_list.find_task_by_id(task_id)
        if task is None:
            return {"message": TASK_DOES_NOT_EXIST }, 404

        if task.get('is_done'):
            return {"message": TASK_WAS_ALREADY_ACHIEVED }, 400
        else:
            relation.tasks_list.update_task(
                task_id=task_id, is_done=True, completed_at=datetime.now().timestamp())

        return {"message": TASK_WAS_ALREADY_ACHIEVED_SUCCESSFULLY }, 200
