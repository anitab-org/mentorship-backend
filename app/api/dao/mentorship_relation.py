from datetime import datetime, timedelta

from app.utils.decorator_utils import check_mail_confirmation
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.utils.enum_utils import MentorshipRelationState


class MentorshipRelationDAO:

    MAXIMUM_MENTORSHIP_DURATION = timedelta(weeks=24)  # 6 months = approximately 6*4
    MINIMUM_MENTORSHIP_DURATION = timedelta(weeks=4)

    def create_mentorship_relation(self, user_id, data):
        action_user_id = user_id
        mentor_id = data['mentor_id']
        mentee_id = data['mentee_id']
        end_date_timestamp = data['end_date']
        notes = data['notes']

        # user_id has to match either mentee_id or mentor_id
        is_valid_user_ids = action_user_id == mentor_id or action_user_id == mentee_id
        if not is_valid_user_ids:
            return {'message': 'Your ID has to match either Mentor or Mentee IDs.'}, 400

        # mentor_id has to be different from mentee_id
        if mentor_id == mentee_id:
            return {'message': 'You cannot have a mentorship relation with yourself.'}, 400

        end_date_datetime = datetime.fromtimestamp(end_date_timestamp)

        now_datetime = datetime.now()
        if end_date_datetime < now_datetime:
            return {'message': 'End date is invalid since date has passed.'}, 400

        # business logic constraints

        max_relation_duration = end_date_datetime - now_datetime
        if max_relation_duration > self.MAXIMUM_MENTORSHIP_DURATION:
            return {'message': 'Mentorship relation maximum duration is 6 months.'}, 400

        if max_relation_duration < self.MINIMUM_MENTORSHIP_DURATION:
            return {'message': 'Mentorship relation minimum duration is 4 week.'}, 400

        # validate if mentor user exists
        mentor_user = UserModel.find_by_id(mentor_id)
        if mentor_user is None:
            return {'message': 'Mentor user does not exist.'}, 404

        # validate if mentor is available to mentor
        if not mentor_user.available_to_mentor:
            return {'message': 'Mentor user is not available to mentor.'}, 400

        # validate if mentee user exists
        mentee_user = UserModel.find_by_id(mentee_id)
        if mentee_user is None:
            return {'message': 'Mentee user does not exist.'}, 404

        # validate if mentee is wants to be mentored
        if not mentee_user.need_mentoring:
            return {'message': 'Mentee user is not available to be mentored.'}, 400

        # check if both users(mentor and mentee) have verified their email
        if mentee_user.is_email_verified:
            pass
        else:
            return {'message': 'Mentee has not confirmed his email.'}, 400
        if mentor_user.is_email_verified:
            pass
        else:
            return {'message': 'Mentor has not confirmed his email.'}, 400

        # TODO add tests for this portion
        all_mentor_relations = mentor_user.mentor_relations + mentor_user.mentee_relations
        for relation in all_mentor_relations:
            if relation.state is MentorshipRelationState.ACCEPTED:
                return {'message': 'Mentor user is already in a relationship.'}, 400

        all_mentee_relations = mentee_user.mentor_relations + mentee_user.mentee_relations
        for relation in all_mentee_relations:
            if relation.state is MentorshipRelationState.ACCEPTED:
                return {'message': 'Mentee user is already in a relationship.'}, 400

        # All validations were checked

        tasks_list = TasksListModel()
        tasks_list.save_to_db()

        mentorship_relation = MentorshipRelationModel(action_user_id=action_user_id,
                                                      mentor_user=mentor_user,
                                                      mentee_user=mentee_user,
                                                      creation_date=datetime.now().timestamp(),
                                                      end_date=end_date_timestamp,
                                                      state=MentorshipRelationState.PENDING,
                                                      notes=notes,
                                                      tasks_list=tasks_list)

        mentorship_relation.save_to_db()

        return {'message': 'Mentorship relation was sent successfully.'}, 200

    @staticmethod
    @check_mail_confirmation
    def list_mentorship_relations(user_id=None, accepted=None, pending=None, completed=None, cancelled=None, rejected=None):
        if pending is not None:
            return {'message': 'Not implemented.'}, 200
        if completed is not None:
            return {'message': 'Not implemented.'}, 200
        if cancelled is not None:
            return {'message': 'Not implemented.'}, 200
        if accepted is not None:
            return {'message': 'Not implemented.'}, 200
        if rejected is not None:
            return {'message': 'Not implemented.'}, 200

        user = UserModel.find_by_id(user_id)

        if user is None:
            return {'message': 'User does not exist.'}, 404

        all_relations = user.mentor_relations + user.mentee_relations

        # add extra field for api response
        for relation in all_relations:
            setattr(relation, 'sent_by_me', relation.action_user_id == user_id)

        return all_relations, 200

    @staticmethod
    @check_mail_confirmation
    def accept_request(user_id, request_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return {'message': 'This mentorship relation request does not exist.'}, 404

        # verify if request is in pending state
        if request.state is not MentorshipRelationState.PENDING:
            return {'message': 'This mentorship relation is not in the pending state.'}, 400

        # verify if I'm the receiver of the request
        if request.action_user_id is user_id:
            return {'message': 'You cannot accept a mentorship request sent by yourself.'}, 400

        # verify if I'm involved in this relation
        if not (request.mentee_id is user_id or request.mentor_id is user_id):
            return {'message': 'You cannot accept a mentorship relation where you are not involved.'}, 400

        requests = user.mentee_relations + user.mentor_relations

        # verify if I'm on a current relation
        for request in requests:
            if request.state is MentorshipRelationState.ACCEPTED:
                return {'message': 'You are currently involved in a mentorship relation.'}, 400

        # All was checked
        request.state = MentorshipRelationState.ACCEPTED
        request.save_to_db()

        return {'message': 'Mentorship relation was accepted successfully.'}, 200

    @staticmethod
    @check_mail_confirmation
    def reject_request(user_id, request_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return {'message': 'This mentorship relation request does not exist.'}, 404

        # verify if request is in pending state
        if request.state is not MentorshipRelationState.PENDING:
            return {'message': 'This mentorship relation is not in the pending state.'}, 400

        # verify if I'm the receiver of the request
        if request.action_user_id is user_id:
            return {'message': 'You cannot reject a mentorship request sent by yourself.'}, 400

        # verify if I'm involved in this relation
        if not (request.mentee_id is user_id or request.mentor_id is user_id):
            return {'message': 'You cannot reject a mentorship relation where you are not involved.'}, 400

        # All was checked
        request.state = MentorshipRelationState.REJECTED
        request.save_to_db()

        return {'message': 'Mentorship relation was rejected successfully.'}, 200

    @staticmethod
    @check_mail_confirmation
    def cancel_relation(user_id, relation_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        request = MentorshipRelationModel.find_by_id(relation_id)

        # verify if request exists
        if request is None:
            return {'message': 'This mentorship relation request does not exist.'}, 404

        # verify if request is in pending state
        if request.state is not MentorshipRelationState.ACCEPTED:
            return {'message': 'This mentorship relation is not in the accepted state.'}, 400

        # verify if I'm involved in this relation
        if not (request.mentee_id is user_id or request.mentor_id is user_id):
            return {'message': 'You cannot cancel a mentorship relation where you are not involved.'}, 400

        # All was checked
        request.state = MentorshipRelationState.CANCELLED
        request.save_to_db()

        return {'message': 'Mentorship relation was cancelled successfully.'}, 200

    @staticmethod
    @check_mail_confirmation
    def delete_request(user_id, request_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return {'message': 'This mentorship relation request does not exist.'}, 404

        # verify if request is in pending state
        if request.state is not MentorshipRelationState.PENDING:
            return {'message': 'This mentorship relation is not in the pending state.'}, 400

        # verify if user created the mentorship request
        if request.action_user_id is not user_id:
            return {'message': 'You cannot delete a mentorship request that you did not create.'}, 400

        # All was checked
        request.delete_from_db()

        return {'message': 'Mentorship relation was deleted successfully.'}, 200

    @staticmethod
    @check_mail_confirmation
    def list_past_mentorship_relations(user_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        now_timestamp = datetime.now().timestamp()
        past_relations = []
        all_relations = user.mentor_relations + user.mentee_relations

        for relation in all_relations:
            if relation.end_date < now_timestamp:
                setattr(relation, 'sent_by_me', relation.action_user_id == user_id)
                past_relations += [relation]

        return past_relations, 200

    @staticmethod
    @check_mail_confirmation
    def list_current_mentorship_relation(user_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        all_relations = user.mentor_relations + user.mentee_relations

        for relation in all_relations:
            if relation.state is MentorshipRelationState.ACCEPTED:
                setattr(relation, 'sent_by_me', relation.action_user_id == user_id)
                return relation

        return {'message': 'You are not in a current mentorship relation.'}, 200

    @staticmethod
    @check_mail_confirmation
    def list_pending_mentorship_relations(user_id):

        user = UserModel.find_by_id(user_id)

        # verify if user exists
        if user is None:
            return {'message': 'User does not exist.'}, 404

        now_timestamp = datetime.now().timestamp()
        pending_requests = []
        all_relations = user.mentor_relations + user.mentee_relations

        for relation in all_relations:
            if relation.state is MentorshipRelationState.PENDING and relation.end_date > now_timestamp:
                setattr(relation, 'sent_by_me', relation.action_user_id == user_id)
                pending_requests += [relation]

        return pending_requests, 200
