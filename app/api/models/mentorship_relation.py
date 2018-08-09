from flask_restplus import fields, Model

from app.utils.enum_utils import MentorshipRelationState


def add_models_to_namespace(api_namespace):
    api_namespace.models[send_mentorship_request_body.name] = send_mentorship_request_body
    api_namespace.models[mentorship_request_response_body.name] = mentorship_request_response_body
    api_namespace.models[relation_user_response_body.name] = relation_user_response_body


send_mentorship_request_body = Model('Send mentorship relation request model', {
    'mentor_id': fields.Integer(required=True, description='Mentorship relation mentor ID'),
    'mentee_id': fields.Integer(required=True, description='Mentorship relation mentee ID'),
    'end_date': fields.Float(required=True, description='Mentorship relation end date in UNIX timestamp format'),
    'notes': fields.String(required=True, description='Mentorship relation notes')
})

relation_user_response_body = Model('User', {
    'id': fields.Integer(required=True, description='User ID'),
    'name': fields.String(required=True, description='User name'),
})

mentorship_request_response_body = Model('List mentorship relation request model', {
    'id': fields.Integer(required=True, description='Mentorship relation ID'),
    'action_user_id': fields.Integer(required=True, description='Mentorship relation requester user ID'),
    'sent_by_me': fields.Boolean(required=True, description='Mentorship relation sent by current user indication'),
    'mentor': fields.Nested(relation_user_response_body),
    'mentee': fields.Nested(relation_user_response_body),
    'creation_date': fields.Float(required=True, description='Mentorship relation creation date in UNIX timestamp format'),
    'accept_date': fields.Float(required=True, description='Mentorship relation acceptance date in UNIX timestamp format'),
    'start_date': fields.Float(required=True, description='Mentorship relation start date in UNIX timestamp format'),
    'end_date': fields.Float(required=True, description='Mentorship relation end date in UNIX timestamp format'),
    'state': fields.Integer(required=True, enum=MentorshipRelationState.values, description='Mentorship relation state'),
    'notes': fields.String(required=True, description='Mentorship relation notes')
})
