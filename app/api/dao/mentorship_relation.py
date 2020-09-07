from datetime import datetime, timedelta

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.utils.decorator_utils import email_verification_required
from app.utils.enum_utils import MentorshipRelationState

class MentorshipRelationDAO:
    """Data Access Object for mentorship relation functionalities.

    Provides various functions pertaining to mentorship.

    Attributes:
        MAXIMUM_MENTORSHIP_DURATION
        MINIMUM_MENTORSHIP_DURATION
    """

    MAXIMUM_MENTORSHIP_DURATION = timedelta(weeks=24)  # 6 months = approximately 6*4
    MINIMUM_MENTORSHIP_DURATION = timedelta(weeks=4)

    def create_mentorship_relation(self, user_id, data):
        """Creates a relationship between two users.

        Establishes the mentor-mentee relationship.

        Args:
            user_id: ID of the user initiating this request. Has to be either the mentor or the mentee.
            data: List containing the mentor_id, mentee_id, end_date_timestamp and notes.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relationship is established, failure if otherwise.
        """
        action_user_id = user_id
        mentor_id = data['mentor_id']
        mentee_id = data['mentee_id']
        end_date_timestamp = data['end_date']
        notes = data['notes']

        # user_id has to match either mentee_id or mentor_id
        is_valid_user_ids = action_user_id == mentor_id or action_user_id == mentee_id
        if not is_valid_user_ids:
            return messages.MATCH_EITHER_MENTOR_OR_MENTEE, 400

        # mentor_id has to be different from mentee_id
        if mentor_id == mentee_id:
            return messages.MENTOR_ID_SAME_AS_MENTEE_ID, 400

        end_date_datetime = datetime.fromtimestamp(end_date_timestamp)

        now_datetime = datetime.now()
        if end_date_datetime < now_datetime:
            return messages.END_TIME_BEFORE_PRESENT, 400

        # business logic constraints

        max_relation_duration = end_date_datetime - now_datetime
        if max_relation_duration > self.MAXIMUM_MENTORSHIP_DURATION:
            return messages.MENTOR_TIME_GREATER_THAN_MAX_TIME, 400

        if max_relation_duration < self.MINIMUM_MENTORSHIP_DURATION:
            return messages.MENTOR_TIME_LESS_THAN_MIN_TIME, 400

        # validate if mentor user exists
        mentor_user = UserModel.find_by_id(mentor_id)
        if mentor_user is None:
            return messages.MENTOR_DOES_NOT_EXIST, 404

        # validate if mentor is available to mentor
        if not mentor_user.available_to_mentor:
            return messages.MENTOR_NOT_AVAILABLE_TO_MENTOR, 400

        # validate if mentee user exists
        mentee_user = UserModel.find_by_id(mentee_id)
        if mentee_user is None:
            return messages.MENTEE_DOES_NOT_EXIST, 404

        # validate if mentee is wants to be mentored
        if not mentee_user.need_mentoring:
            return messages.MENTEE_NOT_AVAIL_TO_BE_MENTORED, 400


        # TODO add tests for this portion

        all_mentor_relations = mentor_user.mentor_relations + mentor_user.mentee_relations
        for relation in all_mentor_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTOR_IN_RELATION, 400

        all_mentee_relations = mentee_user.mentor_relations + mentee_user.mentee_relations
        for relation in all_mentee_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                return messages.MENTEE_ALREADY_IN_A_RELATION, 400

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

        return messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def list_mentorship_relations(user_id=None, accepted=None, pending=None, completed=None, cancelled=None, rejected=None):
        """Lists all relationships of a given user.

        Lists all relationships of a given user. Support for filtering not yet implemented.

        Args:
            user_id: ID of the user whose relationships are to be listed.

        Returns:
            message: A message corresponding to the completed action; success if all relationships of a given user are listed, failure if otherwise.
        """
        if pending is not None:
            return messages.NOT_IMPLEMENTED, 200
        if completed is not None:
            return messages.NOT_IMPLEMENTED, 200
        if cancelled is not None:
            return messages.NOT_IMPLEMENTED, 200
        if accepted is not None:
            return messages.NOT_IMPLEMENTED, 200
        if rejected is not None:
            return messages.NOT_IMPLEMENTED, 200

        user = UserModel.find_by_id(user_id)
        all_relations = user.mentor_relations + user.mentee_relations

        # add extra field for api response
        for relation in all_relations:
            setattr(relation, 'sent_by_me', relation.action_user_id == user_id)

        return all_relations, 200

    @staticmethod
    @email_verification_required
    def accept_request(user_id, request_id):
        """Allows a mentorship request.

        Args:
            user_id: ID of the user accepting the request.
            request_id: ID of the request to be accepted.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relation request is accepted, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404

        # verify if request is in pending state
        if request.state != MentorshipRelationState.PENDING:
            return messages.NOT_PENDING_STATE_RELATION, 400

        # verify if I'm the receiver of the request
        if request.action_user_id == user_id:
            return messages.CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER, 400

        # verify if I'm involved in this relation
        if not (request.mentee_id == user_id or request.mentor_id == user_id):
            return CANT_ACCEPT_UNINVOLVED_MENTOR_RELATION, 400

        requests = user.mentee_relations + user.mentor_relations

        # verify if I'm on a current relation
        for request in requests:
            if request.state == MentorshipRelationState.ACCEPTED:
                return messages.USER_IS_INVOLVED_IN_A_MENTORSHIP_RELATION, 400

        # All was checked
        request.state = MentorshipRelationState.ACCEPTED
        request.save_to_db()

        return messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def reject_request(user_id, request_id):
        """Rejects a mentorship request.

        Args:
            user_id: ID of the user rejecting the request.
            request_id: ID of the request to be rejected.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relation request is rejected, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404

        # verify if request is in pending state
        if request.state != MentorshipRelationState.PENDING:
            return messages.NOT_PENDING_STATE_RELATION, 400

        # verify if I'm the receiver of the request
        if request.action_user_id == user_id:
            return messages.USER_CANT_REJECT_REQUEST_SENT_BY_USER, 400

        # verify if I'm involved in this relation
        if not (request.mentee_id == user_id or request.mentor_id == user_id):
            return messages.CANT_REJECT_UNINVOLVED_RELATION_REQUEST, 400

        # All was checked
        request.state = MentorshipRelationState.REJECTED
        request.save_to_db()

        return messages.MENTORSHIP_RELATION_WAS_REJECTED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def cancel_relation(user_id, relation_id):
        """Allows a given user to terminate a particular relationship.

        Args:
            user_id: ID of the user terminating the relationship.
            relation_id: ID of the relationship.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relation is terminated, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        request = MentorshipRelationModel.find_by_id(relation_id)

        # verify if request exists
        if request is None:
            return messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404

        # verify if request is in pending state
        if request.state != MentorshipRelationState.ACCEPTED:
            return messages.UNACCEPTED_STATE_RELATION, 400

        # verify if I'm involved in this relation
        if not (request.mentee_id == user_id or request.mentor_id == user_id):
            return messages.CANT_CANCEL_UNINVOLVED_REQUEST, 400

        # All was checked
        request.state = MentorshipRelationState.CANCELLED
        request.save_to_db()

        return messages.MENTORSHIP_RELATION_WAS_CANCELLED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def delete_request(user_id, request_id):
        """Deletes a mentorship request.

        Deletes a mentorship request if the current user was the one who created it and the request is in the pending state.

        Args:
            user_id: ID of the user that is deleting a request.
            request_id: ID of the request.

        Returns:
            message: A message corresponding to the completed action; success if mentorship relation request is deleted, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        request = MentorshipRelationModel.find_by_id(request_id)

        # verify if request exists
        if request is None:
            return messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404

        # verify if request is in pending state
        if request.state != MentorshipRelationState.PENDING:
            return messages.NOT_PENDING_STATE_RELATION, 400

        # verify if user created the mentorship request
        if request.action_user_id != user_id:
            return messages.CANT_DELETE_UNINVOLVED_REQUEST, 400

        # All was checked
        request.delete_from_db()

        return messages.MENTORSHIP_RELATION_WAS_DELETED_SUCCESSFULLY, 200

    @staticmethod
    @email_verification_required
    def list_past_mentorship_relations(user_id):
        """Lists past mentorship relation details.

        Args:
            user_id: ID of the user listing all previous relationships.

        Returns:
            message: A message corresponding to the completed action; success if past mentorship relation details are listed, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        now_timestamp = datetime.now().timestamp()
        past_relations = []
        all_relations = user.mentor_relations + user.mentee_relations

        for relation in all_relations:
            if relation.end_date < now_timestamp:
                setattr(relation, 'sent_by_me', relation.action_user_id == user_id)
                past_relations += [relation]

        return past_relations, 200

    @staticmethod
    @email_verification_required
    def list_current_mentorship_relation(user_id):
        """Lists current mentorship relation details.

        Args:
            user_id: ID of the user listing all current relationships.

        Returns:
            message: A message corresponding to the completed action; success if current mentorship relation details are listed, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        all_relations = user.mentor_relations + user.mentee_relations

        for relation in all_relations:
            if relation.state == MentorshipRelationState.ACCEPTED:
                setattr(relation, 'sent_by_me', relation.action_user_id == user_id)
                return relation

        return messages.NOT_IN_MENTORED_RELATION_CURRENTLY, 200

    @staticmethod
    @email_verification_required
    def list_pending_mentorship_relations(user_id):
        """Lists mentorship requests in pending state.

        Args:
            user_id: ID of the user listing all pending relationships.

        Returns:
            message: A message corresponding to the completed action; success if pending mentorship relation requests are listed, failure if otherwise.
        """

        user = UserModel.find_by_id(user_id)
        now_timestamp = datetime.now().timestamp()
        pending_requests = []
        all_relations = user.mentor_relations + user.mentee_relations

        for relation in all_relations:
            if relation.state == MentorshipRelationState.PENDING and relation.end_date > now_timestamp:
                setattr(relation, 'sent_by_me', relation.action_user_id == user_id)
                pending_requests += [relation]

        return pending_requests, 200
