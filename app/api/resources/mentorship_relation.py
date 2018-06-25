from flask import request
from flask_restplus import Resource
from flask_jwt import jwt_required, current_identity

from run import api
from app.api.resources.common import auth_header_parser
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.api.models.mentorship_relation import *

mentorship_relation_ns = api.namespace('Mentorship Relation',
                                       description='Operations related to '
                                                   'mentorship relations '
                                                   'between users')
add_models_to_namespace(mentorship_relation_ns)

DAO = MentorshipRelationDAO()


@mentorship_relation_ns.route('mentorship-relation/send_request')
class SendRequest(Resource):

    @classmethod
    @jwt_required()
    @mentorship_relation_ns.doc('send_request')
    @mentorship_relation_ns.expect(auth_header_parser, send_mentorship_request_body)
    @mentorship_relation_ns.response(200, 'Mentorship Relation request was sent successfully.')
    @mentorship_relation_ns.response(400, 'Validation error.')
    def post(cls):
        """
        Creates a new mentorship relation request.
        """

        user_id = current_identity.id
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
            return {"message": "Mentor ID field is missing."}
        if 'mentee_id' not in data:
            return {"message": "Mentee ID field is missing."}
        if 'end_date' not in data:
            return {"message": "End date field is missing."}
        if 'notes' not in data:
            return {"message": "Notes field is missing."}

        return {}


@mentorship_relation_ns.route('mentorship-relations')
class GetAllMyMentorshipRelation(Resource):

    @classmethod
    @jwt_required()
    @mentorship_relation_ns.doc('get_all_user_mentorship_relations')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Return all user\'s mentorship relations was successfully.', model=mentorship_request_response_body)
    @mentorship_relation_ns.marshal_list_with(mentorship_request_response_body)
    def get(cls):
        """
        Lists all mentorship relations.
        """

        user_id = current_identity.id
        response = DAO.list_mentorship_relations(user_id=user_id)

        return response


@mentorship_relation_ns.route('mentorship_relation/<int:request_id>/reject')
class RejectMentorshipRelation(Resource):

    @classmethod
    @jwt_required()
    @mentorship_relation_ns.doc('reject_mentorship_relation')
    @mentorship_relation_ns.expect(auth_header_parser)
    @mentorship_relation_ns.response(200, 'Rejected mentorship relations with success.')
    def put(cls, request_id):
        """
        Reject a mentorship relation.
        """

        # TODO check if user id is well parsed, if it is an integer

        user_id = current_identity.id
        response = DAO.reject_request(user_id=user_id, request_id=request_id)

        return response
