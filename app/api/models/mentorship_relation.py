from flask_restplus import fields, Model

from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState


def add_models_to_namespace(api_namespace):
    api_namespace.models[send_mentorship_request_body.name] = send_mentorship_request_body
    api_namespace.models[mentorship_request_response_body.name] = mentorship_request_response_body
    api_namespace.models[relation_user_response_body.name] = relation_user_response_body
    api_namespace.models[create_task_request_body.name] = create_task_request_body
    api_namespace.models[list_tasks_response_body.name] = list_tasks_response_body
    api_namespace.models[dashboard_mentorship_request_response_body.name] = dashboard_mentorship_request_response_body

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

dashboard_mentorship_request_response_body = Model('List mentorship relation request model', {
    'id': fields.Integer(required=True, description='Mentorship relation ID'),
    'action_user_id': fields.Integer(required=True, description='Mentorship relation requester user ID'),
    'sent_by_me': fields.Boolean(required=True, description='Mentorship relation sent by current user indication'),
    'mentor_id': fields.Integer(required=True, description='Unique ID of mentor user'),
    'mentor_name': fields.String(required=True, description="Name of mentor user"),
    'mentor_photo_url': fields.String(required=True, description='Profile photo URL of mentor user'),
    'mentee_id': fields.Integer(required=True, description='Unique ID of mentee user'),
    'mentee_name': fields.String(required=True, description='Name of mentee user'),
    'mentee_photo_url': fields.String(required=True, description='Profile photo URL of mentee user'),
    'creation_date': fields.Float(required=True, description='Mentorship relation creation date in UNIX timestamp format'),
    'accept_date': fields.Float(required=True, description='Mentorship relation acceptance date in UNIX timestamp format'),
    'start_date': fields.Float(required=True, description='Mentorship relation start date in UNIX timestamp format'),
    'end_date': fields.Float(required=True, description='Mentorship relation end date in UNIX timestamp format'),
    'state': fields.Integer(required=True, enum=MentorshipRelationState.values, description='Mentorship relation state'),
    'notes': fields.String(required=True, description='Mentorship relation notes')
})

create_task_request_body = Model('Create task request model', {
    'description': fields.String(required=True, description='Mentorship relation task description')
})

list_tasks_response_body = Model('List tasks response model', {
    'id': fields.Integer(required=True, description='Task ID'),
    'description': fields.String(required=True, description='Mentorship relation task description'),
    'is_done': fields.Boolean(required=True, description='Mentorship relation task is done indication'),
    'created_at': fields.Float(required=True, description='Task creation date in UNIX timestamp format'),
    'completed_at': fields.Float(required=False, description='Task completion date in UNIX timestamp format')
})


class DashboardMentorshipRelation:
    """Convenience class which represents relations  returned by /dashboard endpoint"""

    def __init__(self, rel: MentorshipRelationModel):
        self.id = rel.id
        self.action_user_id = rel.action_user_id
        self.mentor_id = rel.mentor.id
        self.mentor_name = rel.mentor.name
        self.mentor_photo_url = rel.mentor.photo_url
        self.mentee_id = rel.mentee.id
        self.mentee_name = rel.mentee.name
        self.mentee_photo_url = rel.mentee.photo_url
        self.creation_date = rel.creation_date
        self.accept_date = rel.accept_date
        self.start_date = rel.start_date
        self.end_date = rel.end_date
        self.state = rel.state
        self.notes = rel.notes
        self.tasks_list = rel.tasks_list

    def json(self):
        """Returns information of mentorship as a json object."""
        return {
            'id': self.id,
            'action_user_id': self.action_user_id,
            'mentor_id': self.mentor_id,
            'mentor_name': self.mentor_name,
            'mentor_photo_url': self.mentor_photo_url,
            'mentee_id': self.mentee_id,
            'mentee_name': self.mentee_name,
            'mentee_photo_url': self.mentee_photo_url,
            'creation_date': self.creation_date,
            'accept_date': self.accept_date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'state': self.state,
            'notes': self.notes
        }
