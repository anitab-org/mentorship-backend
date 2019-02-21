from datetime import datetime

from app.utils.decorator_utils import email_verification_required
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.user import UserModel
from app.utils.enum_utils import MentorshipRelationState

class TaskDAO:

    @staticmethod
    @email_verification_required
    def create_task(user_id, mentorship_relation_id, data):
        description = data['description']

        user = UserModel.find_by_id(user_id)
        if user == None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(_id=mentorship_relation_id)
        if relation == None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        if relation.state is not MentorshipRelationState.ACCEPTED:
            return {'message': 'Mentorship relation is not in the accepted state.'}, 400

        now_timestamp = datetime.now().timestamp()
        relation.tasks_list.add_task(description=description, created_at=now_timestamp)
        relation.tasks_list.save_to_db()

        return {"message": "Task was created successfully."}, 200

    @staticmethod
    @email_verification_required
    def list_tasks(user_id, mentorship_relation_id):

        user = UserModel.find_by_id(user_id)
        if user == None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation == None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return {'message': 'You are not involved in this mentorship relation.'}, 401

        all_tasks = relation.tasks_list.tasks

        return all_tasks

    @staticmethod
    @email_verification_required
    def delete_task(user_id, mentorship_relation_id, task_id):

        user = UserModel.find_by_id(user_id)
        if user == None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation == None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        task = relation.tasks_list.find_task_by_id(task_id)
        if task == None:
            return {'message': 'Task does not exist.'}, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return {'message': 'You are not involved in this mentorship relation.'}, 401

        relation.tasks_list.delete_task(task_id)

        return {'message': 'Task was deleted successfully.'}, 200

    @staticmethod
    @email_verification_required
    def complete_task(user_id, mentorship_relation_id, task_id):

        user = UserModel.find_by_id(user_id)
        if user == None:
            return {'message': 'User does not exist.'}, 404

        relation = MentorshipRelationModel.find_by_id(mentorship_relation_id)
        if relation == None:
            return {'message': 'Mentorship relation does not exist.'}, 404

        if not (user_id == relation.mentee_id or user_id == relation.mentor_id):
            return {'message': 'You are not involved in this mentorship relation.'}, 401

        task = relation.tasks_list.find_task_by_id(task_id)
        if task == None:
            return {'message': 'Task does not exist.'}, 404

        if task.get('is_done'):
            return {'message': 'Task was already achieved.'}, 400
        else:
            relation.tasks_list.update_task(
                task_id=task_id, is_done=True, completed_at=datetime.now().timestamp())

        return {'message': 'Task was achieved successfully.'}, 200
