from datetime import datetime, timedelta

from app.database.models.mentorship_relation import MentorshipRelationModel
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

        mentorship_relation = MentorshipRelationModel(action_user_id=action_user_id,
                                                      mentor_user=mentor_user,
                                                      mentee_user=mentee_user,
                                                      creation_date=datetime.now().timestamp(),
                                                      end_date=end_date_timestamp,
                                                      state=MentorshipRelationState.PENDING,
                                                      notes=notes)

        mentorship_relation.save_to_db()

        return {'message': 'Mentorship relation was sent successfully.'}, 200

    @staticmethod
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
        all_relations = user.mentor_relations + user.mentee_relations

        return all_relations
