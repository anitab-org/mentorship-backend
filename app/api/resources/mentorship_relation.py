from flask import request
from flask_restplus import Resource, Namespace, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import messages
from app.api.dao.task import TaskDAO
from app.api.resources.common import auth_header_parser
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.api.models.mentorship_relation import *
from app.database.models.mentorship_relation import MentorshipRelationModel

mentorship_relation_ns = Namespace('Mentorship Relation',
                                   description='Operations related to '
                                               'mentorship relations '
                                               'between users')
add_models_to_namespace(mentorship_relation_ns)

DAO = MentorshipRelationDAO()


@mentorship_relation_ns.route('mentorship_relation/send_request')
class SendRequest(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('send_request')
    @mentorship_relation_ns.expect(auth_header_parser, send_mentorship_request_body)
    @mentorship_relation_ns.response(200, 'Mentorship Relation request was sent successfully.')
    @mentorship_relation_ns.response(400, 'Validation error.')
    def post(cls):
        """
        Creates a new mentorship relation request.
        """

        user_id = get_jwt_identity()
        data = request.json

        is_valid = SendRequest.is_valid_data(data)

        if is_valid != {}:
            return is_valid, 400

        response = DAO.create_mentorship_relation(user_id, data)

        return response

    @staticmethod
    def is_valid_data(data):

        # Verify if request body has required fields
        if 'mentor_id' not in data:
            return messages.MENTOR_ID_FIELD_IS_MISSING
        if 'mentee_id' not in data:
            return messages.MENTEE_ID_FIELD_IS_MISSING
        if 'end_date' not in data:
            return messages.END_DATE_FIELD_IS_MISSING
        if 'notes' not in data:
            return messages.NOTES_FIELD_IS_MISSING

        return {}


@mentorship_relation_ns.route('mentorship_relations')
class GetAllMyMentorshipRelation(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('get_all_user_mentorship_relations')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Return all user\'s mentorship relations was successfully.',
                                     model=mentorship_request_response_body)
    @mentorship_relation_ns.marshal_list_with(mentorship_request_response_body)
    def get(cls):
        """
        Lists all mentorship relations of current user.
        """

        user_id = get_jwt_identity()
        response = DAO.list_mentorship_relations(user_id=user_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/accept')
class AcceptMentorshipRelation(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('accept_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Accept mentorship relations with success.')
    def put(cls, request_id):
        """
        Accept a mentorship relation.
        """

        # check if user id is well parsed
        # if it is an integer

        user_id = get_jwt_identity()
        response = DAO.accept_request(user_id=user_id, request_id=request_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/reject')
class RejectMentorshipRelation(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('reject_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Rejected mentorship relations with success.')
    def put(cls, request_id):
        """
        Reject a mentorship relation.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()
        response = DAO.reject_request(user_id=user_id, request_id=request_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/cancel')
class CancelMentorshipRelation(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('cancel_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Cancelled mentorship relations with success.')
    def put(cls, request_id):
        """
        Cancel a mentorship relation.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()
        response = DAO.cancel_relation(user_id=user_id, relation_id=request_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>')
class DeleteMentorshipRelation(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('delete_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Deleted mentorship relation with success.')
    def delete(cls, request_id):
        """
        Delete a mentorship request.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()
        response = DAO.delete_request(user_id=user_id, request_id=request_id)

        return response


@mentorship_relation_ns.route('mentorship_relations/past')
class ListPastMentorshipRelations(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('get_past_mentorship_relations')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Returned past mentorship relations with success.',
                                     model=mentorship_request_response_body)
    @mentorship_relation_ns.marshal_list_with(mentorship_request_response_body)
    def get(cls):
        """
        Lists past mentorship relations of the current user.
        """

        user_id = get_jwt_identity()
        response = DAO.list_past_mentorship_relations(user_id)

        return response


@mentorship_relation_ns.route('mentorship_relations/current')
class ListCurrentMentorshipRelation(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('get_current_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Returned current mentorship relation with success.',
                                     model=mentorship_request_response_body)
    def get(cls):
        """
        Lists current mentorship relation of the current user.
        """

        user_id = get_jwt_identity()
        response = DAO.list_current_mentorship_relation(user_id)

        if isinstance(response, MentorshipRelationModel):
            return marshal(response, mentorship_request_response_body), 200
        else:
            return response


@mentorship_relation_ns.route('mentorship_relations/pending')
class ListPendingMentorshipRequests(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('get_pending_mentorship_relations')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Returned pending mentorship relation with success.',
                                     model=mentorship_request_response_body)
    @mentorship_relation_ns.marshal_list_with(mentorship_request_response_body)
    def get(cls):
        """
        Lists pending mentorship requests of the current user.
        """

        user_id = get_jwt_identity()
        response = DAO.list_pending_mentorship_relations(user_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/task')
class CreateTask(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('create_task_in_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser, create_task_request_body)
    @mentorship_relation_ns.response(200, 'Created task with success.')
    def post(cls, request_id):
        """
        Create a task.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()
        request_body = request.json

        is_valid = CreateTask.is_valid_data(request_body)

        if is_valid != {}:
            return is_valid, 400

        response = TaskDAO.create_task(user_id=user_id, mentorship_relation_id=request_id, data=request_body)

        return response

    @staticmethod
    def is_valid_data(data):

        if 'description' not in data:
            return messages.DESCRIPTION_FIELD_IS_MISSING

        return {}


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/task/<int:task_id>')
class DeleteTask(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('delete_task_in_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Delete task with success.')
    def delete(cls, request_id, task_id):
        """
        Delete a task.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()

        response = TaskDAO.delete_task(user_id=user_id, mentorship_relation_id=request_id, task_id=task_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/tasks')
class ListTasks(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('list_tasks_in_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'List tasks from a mentorship relation with success.',
                                     model=list_tasks_response_body)
    def get(cls, request_id):
        """
        List all tasks from a mentorship relation.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()

        response = TaskDAO.list_tasks(user_id=user_id, mentorship_relation_id=request_id)

        if isinstance(response, tuple):
            return response
        else:
            return marshal(response, list_tasks_response_body), 200


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/task/<int:task_id>/complete')
class UpdateTask(Resource):

    @classmethod
    @jwt_required
    @mentorship_relation_ns.doc('update_task_in_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Updated task with success.')
    def put(cls, request_id, task_id):
        """
        Update a task.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = get_jwt_identity()

        response = TaskDAO.complete_task(user_id=user_id, mentorship_relation_id=request_id, task_id=task_id)

        return response
