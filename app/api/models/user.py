from flask_restplus import fields, Model
from app.api.models.mentorship_relation import list_tasks_response_body


def add_models_to_namespace(api_namespace):
    api_namespace.models[public_user_api_model.name] = public_user_api_model
    api_namespace.models[full_user_api_model.name] = full_user_api_model
    api_namespace.models[register_user_api_model.name] = register_user_api_model
    api_namespace.models[change_password_request_data_model.name] = change_password_request_data_model
    api_namespace.models[update_user_request_body_model.name] = update_user_request_body_model
    api_namespace.models[login_request_body_model.name] = login_request_body_model
    api_namespace.models[login_response_body_model.name] = login_response_body_model
    api_namespace.models[refresh_response_body_model.name] = refresh_response_body_model
    api_namespace.models[resend_email_request_body_model.name] = resend_email_request_body_model
    api_namespace.models[home_response_body_model.name] = home_response_body_model
    api_namespace.models[dashboard_relation_body_mentee_model.name] = dashboard_relation_body_mentee_model
    api_namespace.models[dashboard_relation_body_mentor_model.name] = dashboard_relation_body_mentor_model
    api_namespace.models[dashboard_relation_states_body_mentee_model.name] = dashboard_relation_states_body_mentee_model
    api_namespace.models[dashboard_relation_states_body_mentor_model.name] = dashboard_relation_states_body_mentor_model
    api_namespace.models[dashboard_mentorship_requests_model.name] = dashboard_mentorship_requests_model
    api_namespace.models[list_tasks_inherited_model.name] = list_tasks_inherited_model
    api_namespace.models[dashboard_tasks_model.name] = dashboard_tasks_model
    api_namespace.models[dashboard_response_body_model.name] = dashboard_response_body_model


public_user_api_model = Model('User list model', {
    'id': fields.Integer(
        readOnly=True,
        description='The unique identifier of a user'
    ),
    'username': fields.String(
        required=True,
        description='User username'
    ),
    'name': fields.String(
        required=True,
        description='User name'
    ),
    'slack_username': fields.String(
        required=True,
        description='User Slack username'
    ),
    'bio': fields.String(
        required=True,
        description='User bio'
    ),
    'location': fields.String(
        required=True,
        description='User location'
    ),
    'occupation': fields.String(
        required=True,
        description='User occupation'
    ),
    'organization': fields.String(
        required=True,
        description='User organization'
    ),
    'interests': fields.String(
        required=True,
        description='User interests'
    ),
    'skills': fields.String(
        required=True,
        description='User skills'
    ),
    'need_mentoring': fields.Boolean(
        required=True,
        description='User need to be mentored indication'
    ),
    'available_to_mentor': fields.Boolean(
        required=True,
        description='User availability to mentor indication'
    )
})

full_user_api_model = Model('User Complete model used in listing', {
    'id': fields.Integer(
        readOnly=True,
        description='The unique identifier of a user'
    ),
    'name': fields.String(
        required=True,
        description='User name'
    ),
    'username': fields.String(
        required=True,
        description='User username'
    ),
    'email': fields.String(
        required=True,
        description='User email'
    ),
    'password_hash': fields.String(
        required=True,
        description='User password hash'
    ),
    'terms_and_conditions_checked': fields.Boolean(
        required=True,
        description='User Terms and Conditions check state'
    ),
    'is_admin': fields.Boolean(
        required=True,
        description='User admin status'
    ),
    'registration_date': fields.Float(
        required=True,
        description='User registration date'
    ),
    'is_email_verified': fields.Boolean(
        required=True,
        description='User email verification status'
    ),
    'email_verification_date': fields.DateTime(
        required=False,
        description='User email verification date'
    ),
    'bio': fields.String(
        required=False,
        description='User bio'
    ),
    'location': fields.String(required=False, description='User location'),
    'occupation': fields.String(required=False, description='User occupation'),
    'organization': fields.String(required=False, description='User organization'),
    'slack_username': fields.String(required=False, description='User slack username'),
    'social_media_links': fields.String(
        required=False,
        description='User social media links'
    ),
    'skills': fields.String(required=False, description='User skills'),
    'interests': fields.String(required=False, description='User interests'),
    'resume_url': fields.String(required=False, description='User resume url'),
    'photo_url': fields.String(required=False, description='User photo url'),
    'need_mentoring': fields.Boolean(
        required=False,
        description='User need mentoring indication'
    ),
    'available_to_mentor': fields.Boolean(
        required=False,
        description='User availability to mentor indication'
    ),
    'current_mentorship_role': fields.Integer(required=False, description='User current role'),
    'membership_status': fields.Integer(required=False, description='User membershipstatus')
})

register_user_api_model = Model('User registration model', {
    'name': fields.String(required=True, description='User name'),
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password'),
    'email': fields.String(required=True, description='User email'),
    'terms_and_conditions_checked': fields.Boolean(required=True, description='User check Terms and Conditions value'),
    'need_mentoring': fields.Boolean(required=False, description='User need mentoring indication'),
    'available_to_mentor': fields.Boolean(required=False, description='User availability to mentor indication')
})

change_password_request_data_model = Model('Change password request data model', {
    'current_password': fields.String(required=True, description='User\'s current password'),
    'new_password': fields.String(required=True, description='User\'s new password')
})

login_request_body_model = Model('Login request data model', {
    'username': fields.String(required=True, description='User\'s username'),
    'password': fields.String(required=True, description='User\'s password')
})

# TODO: Remove 'expiry' after the android app refactoring.
login_response_body_model = Model('Login response data model', {
    'access_token': fields.String(required=True, description='User\'s access token'),
    'expiry': fields.Float(required=True, description='Access token expiry UNIX timestamp'),
    'access_expiry': fields.Float(required=True, description='Access token expiry UNIX timestamp'),
    'refresh_token': fields.String(required=True, description='User\'s refresh token'),
    'refresh_expiry': fields.Float(required=True, description='Refresh token expiry UNIX timestamp')
})

refresh_response_body_model = Model('Refresh response data model', {
    'access_token': fields.String(required=True, description='User\'s access token'),
    'access_expiry': fields.Float(required=True, description='Access token expiry UNIX timestamp')
})

update_user_request_body_model = Model('Update User request data model', {
    'name': fields.String(required=False, description='User name'),
    'username': fields.String(required=False, description='User username'),
    'bio': fields.String(required=False, description='User bio'),
    'location': fields.String(required=False, description='User location'),
    'occupation': fields.String(required=False, description='User occupation'),
    'organization': fields.String(required=False, description='User organization'),
    'slack_username': fields.String(required=False, description='User slack username'),
    'social_media_links': fields.String(required=False, description='User social media links'),
    'skills': fields.String(required=False, description='User skills'),
    'interests': fields.String(required=False, description='User interests'),
    # TODO: This url is generated by the backend
    'resume_url': fields.String(required=False, description='User resume url'),
    # TODO: This url is generated by the backend
    'photo_url': fields.String(required=False, description='User photo url'),
    'need_mentoring': fields.Boolean(required=False, description='User need mentoring indication'),
    'available_to_mentor': fields.Boolean(required=False, description='User availability to mentor indication')
})

resend_email_request_body_model = Model('Resend email request data model', {
    'email': fields.String(required=True, description='User\'s email'),
})

home_response_body_model = Model('Get statistics on the app usage of the current user', {
    'name': fields.String(required=True, description='The name of the user'),
    'pending_requests': fields.Integer(required=True, description='Number of pending requests'),
    'accepted_requests': fields.Integer(required=True, description='Number of accepted requests'),
    'completed_relations': fields.Integer(required=True, description='Number of completed relations'),
    'cancelled_relations': fields.Integer(required=True, description='Number of cancelled relations'),
    'rejected_requests': fields.Integer(required=True, description='Number of rejected relations'),
    'achievements': fields.List(fields.Nested(list_tasks_response_body))
})


dashboard_relation_body_mentee_model = Model('Mentorship relation displayed on dashboard where other use is mentee', {
    'id': fields.Integer(required=True, description='Mentorship relation ID'),
    'mentee_id': fields.Integer(required=True, description='Other user\'s ID'),
    'username': fields.String(required=True, description='User username'),
    'photo_url': fields.String(required=True, description='User photo url'),
    'creation_date': fields.Float(
        required=True, description='Mentorship relation creation date in UNIX timestamp format'
        ),
    'accept_date': fields.Float(
        required=True, description='Mentorship relation acceptance date in UNIX timestamp format'
        ),
    'start_date': fields.Float(
        required=True, description='Mentorship relation start date in UNIX timestamp format'
        ),
    'end_date': fields.Float(
        required=True, description='Mentorship relation end date in UNIX timestamp format'
        ),
    'notes': fields.String(required=True, description='Mentorship relation notes')
})

dashboard_relation_body_mentor_model = Model('Mentorship relation displayed on dashboard where other use is mentor', {
    'id': fields.Integer(required=True, description='Mentorship relation ID'),
    'mentor_id': fields.Integer(required=True, description='Other user\'s ID'),
    'username': fields.String(required=True, description='User username'),
    'photo_url': fields.String(required=True, description='User photo url'),
    'creation_date': fields.Float(
        required=True, description='Mentorship relation creation date in UNIX timestamp format'
        ),
    'accept_date': fields.Float(
        required=True, description='Mentorship relation acceptance date in UNIX timestamp format'
        ),
    'start_date': fields.Float(
        required=True, description='Mentorship relation start date in UNIX timestamp format'
        ),
    'end_date': fields.Float(
        required=True, description='Mentorship relation end date in UNIX timestamp format'
        ),
    'notes': fields.String(required=True, description='Mentorship relation notes')
})

dashboard_relation_states_body_mentee_model = Model('Mentorship relation states when other person is mentee',{
    'PENDING': fields.List(fields.Nested(dashboard_relation_body_mentee_model)),
    'ACCEPTED': fields.List(fields.Nested(dashboard_relation_body_mentee_model)),
    'REJECTED': fields.List(fields.Nested(dashboard_relation_body_mentee_model)),
    'CANCELLED': fields.List(fields.Nested(dashboard_relation_body_mentee_model)),
    'COMPLETED': fields.List(fields.Nested(dashboard_relation_body_mentee_model))
})

dashboard_relation_states_body_mentor_model = Model('Mentorship relation states when other person is ment',{
    'PENDING': fields.List(fields.Nested(dashboard_relation_body_mentor_model)),
    'ACCEPTED': fields.List(fields.Nested(dashboard_relation_body_mentor_model)),
    'REJECTED': fields.List(fields.Nested(dashboard_relation_body_mentor_model)),
    'CANCELLED': fields.List(fields.Nested(dashboard_relation_body_mentor_model)),
    'COMPLETED': fields.List(fields.Nested(dashboard_relation_body_mentor_model))
})

dashboard_mentorship_requests_model = Model('Display mentorship request details', {
    'received_as_mentee': fields.Nested(dashboard_relation_states_body_mentor_model),
    'sent_as_mentee': fields.Nested(dashboard_relation_states_body_mentor_model),
    'received_as_mentor': fields.Nested(dashboard_relation_states_body_mentee_model),
    'sent_as_mentor': fields.Nested(dashboard_relation_states_body_mentee_model)
})

list_tasks_inherited_model = list_tasks_response_body.inherit('Added request_id field', {
    'request_id': fields.Integer(required=True, description='Request ID')
})

dashboard_tasks_model = Model('Display todo and done tasks', {
    'todo': fields.List(fields.Nested(list_tasks_inherited_model)),
    'done': fields.List(fields.Nested(list_tasks_inherited_model))
})

dashboard_response_body_model = Model('Get dashboard highlights of the current user', {
    'user_details': fields.Nested(full_user_api_model),
    'mentorship_requests': fields.Nested(dashboard_mentorship_requests_model),
    'tasks': fields.Nested(dashboard_tasks_model)
})
