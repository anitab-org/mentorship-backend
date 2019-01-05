from flask_restplus import fields, Model
from app.api.models.mentorship_relation import LIST_TASKS_RESPONSE_BODY


def add_models_to_namespace(api_namespace):
    api_namespace.models[PUBLIC_USER_API_MODEL.name] = PUBLIC_USER_API_MODEL
    api_namespace.models[FULL_USER_API_MODEL.name] = FULL_USER_API_MODEL
    api_namespace.models[
        REGISTER_USER_API_MODEL.name
    ] = REGISTER_USER_API_MODEL
    api_namespace.models[
        CHANGE_PASSWORD_REQUEST_DATA_MODEL.name
    ] = CHANGE_PASSWORD_REQUEST_DATA_MODEL
    api_namespace.models[
        UPDATE_USER_REQUEST_BODY_MODEL.name
    ] = UPDATE_USER_REQUEST_BODY_MODEL
    api_namespace.models[
        LOGIN_REQUEST_BODY_MODEL.name
    ] = LOGIN_REQUEST_BODY_MODEL
    api_namespace.models[
        LOGIN_RESPONSE_BODY_MODEL.name
    ] = LOGIN_RESPONSE_BODY_MODEL
    api_namespace.models[
        REFRESH_RESPONSE_BODY_MODEL.name
    ] = REFRESH_RESPONSE_BODY_MODEL
    api_namespace.models[
        RESEND_EMAIL_REQUEST_BODY_MODEL.name
    ] = RESEND_EMAIL_REQUEST_BODY_MODEL
    api_namespace.models[
        HOME_RESPONSE_BODY_MODEL.name
    ] = HOME_RESPONSE_BODY_MODEL


PUBLIC_USER_API_MODEL = Model(
    "User list model",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of a user"
        ),
        "username": fields.String(required=True, description="User username"),
        "name": fields.String(required=True, description="User name"),
        "slack_username": fields.String(
            required=True, description="User Slack username"
        ),
        "bio": fields.String(required=True, description="User bio"),
        "location": fields.String(required=True, description="User location"),
        "occupation": fields.String(
            required=True, description="User occupation"
        ),
        "organization": fields.String(
            required=True, description="User organization"
        ),
        "interests": fields.String(
            required=True, description="User interests"
        ),
        "skills": fields.String(required=True, description="User skills"),
        "need_mentoring": fields.Boolean(
            required=True, description="User need to be mentored indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=True, description="User availability to mentor indication"
        ),
    },
)

FULL_USER_API_MODEL = Model(
    "User Complete model used in listing",
    {
        "id": fields.Integer(
            readOnly=True, description="The unique identifier of a user"
        ),
        "name": fields.String(required=True, description="User name"),
        "username": fields.String(required=True, description="User username"),
        "email": fields.String(required=True, description="User email"),
        "password_hash": fields.String(
            required=True, description="User password hash"
        ),
        "terms_and_conditions_checked": fields.Boolean(
            required=True, description="User Terms and Conditions check state"
        ),
        "is_admin": fields.Boolean(
            required=True, description="User admin status"
        ),
        "registration_date": fields.Float(
            required=True, description="User registration date"
        ),
        "is_email_verified": fields.Boolean(
            required=True, description="User email verification status"
        ),
        "email_verification_date": fields.DateTime(
            required=False, description="User email verification date"
        ),
        "bio": fields.String(required=False, description="User bio"),
        "location": fields.String(required=False, description="User location"),
        "occupation": fields.String(
            required=False, description="User occupation"
        ),
        "organization": fields.String(
            required=False, description="User organization"
        ),
        "slack_username": fields.String(
            required=False, description="User slack username"
        ),
        "social_media_links": fields.String(
            required=False, description="User social media links"
        ),
        "skills": fields.String(required=False, description="User skills"),
        "interests": fields.String(
            required=False, description="User interests"
        ),
        "resume_url": fields.String(
            required=False, description="User resume url"
        ),
        "photo_url": fields.String(
            required=False, description="User photo url"
        ),
        "need_mentoring": fields.Boolean(
            required=False, description="User need mentoring indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=False,
            description="User availability to mentor indication",
        ),
        "current_mentorship_role": fields.Integer(
            required=False, description="User current role"
        ),
        "membership_status": fields.Integer(
            required=False, description="User membershipstatus"
        ),
    },
)

REGISTER_USER_API_MODEL = Model(
    "User registration model",
    {
        "name": fields.String(required=True, description="User name"),
        "username": fields.String(required=True, description="User username"),
        "password": fields.String(required=True, description="User password"),
        "email": fields.String(required=True, description="User email"),
        "terms_and_conditions_checked": fields.Boolean(
            required=True, description="User check Terms and Conditions value"
        ),
        "need_mentoring": fields.Boolean(
            required=False, description="User need mentoring indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=False,
            description="User availability to mentor indication",
        ),
    },
)

CHANGE_PASSWORD_REQUEST_DATA_MODEL = Model(
    "Change password request data model",
    {
        "current_password": fields.String(
            required=True, description="User's current password"
        ),
        "new_password": fields.String(
            required=True, description="User's new password"
        ),
    },
)

LOGIN_REQUEST_BODY_MODEL = Model(
    "Login request data model",
    {
        "username": fields.String(
            required=True, description="User's username"
        ),
        "password": fields.String(
            required=True, description="User's password"
        ),
    },
)

# TODO: Remove 'expiry' after the android app refactoring.
LOGIN_RESPONSE_BODY_MODEL = Model('Login response data model', {
    "access_token": fields.String(required=True, description="User\'s access token"),
    "expiry": fields.Float(required=True, description="Access token expiry UNIX timestamp"),
    "access_expiry": fields.Float(required=True, description="Access token expiry UNIX timestamp"),
    "refresh_token": fields.String(required=True, description="User\'s refresh token"),
    "refresh_expiry": fields.Float(required=True, description="Refresh token expiry UNIX timestamp")
})

REFRESH_RESPONSE_BODY_MODEL = Model(
    "Refresh response data model", {
        "access_token": fields.String(
            required=True, description="User\'s access token"), "access_expiry": fields.Float(
                required=True, description="Access token expiry UNIX timestamp")})

UPDATE_USER_REQUEST_BODY_MODEL = Model(
    "Update User request data model",
    {
        "name": fields.String(required=False, description="User name"),
        "username": fields.String(required=False, description="User username"),
        "bio": fields.String(required=False, description="User bio"),
        "location": fields.String(required=False, description="User location"),
        "occupation": fields.String(
            required=False, description="User occupation"
        ),
        "organization": fields.String(
            required=False, description="User organization"
        ),
        "slack_username": fields.String(
            required=False, description="User slack username"
        ),
        "social_media_links": fields.String(
            required=False, description="User social media links"
        ),
        "skills": fields.String(required=False, description="User skills"),
        "interests": fields.String(
            required=False, description="User interests"
        ),
        # TODO: This url is generated by the backend
        "resume_url": fields.String(
            required=False, description="User resume url"
        ),
        # TODO: This url is generated by the backend
        "photo_url": fields.String(
            required=False, description="User photo url"
        ),
        "need_mentoring": fields.Boolean(
            required=False, description="User need mentoring indication"
        ),
        "available_to_mentor": fields.Boolean(
            required=False,
            description="User availability to mentor indication",
        ),
    },
)

RESEND_EMAIL_REQUEST_BODY_MODEL = Model(
    "Resend email request data model",
    {"email": fields.String(required=True, description="User's email")},
)

HOME_RESPONSE_BODY_MODEL = Model(
    "Get statistics on the app usage of the current user",
    {
        "name": fields.String(
            required=True, description="The name of the user"
        ),
        "pending_requests": fields.Integer(
            required=True, description="Number of pending requests"
        ),
        "accepted_requests": fields.Integer(
            required=True, description="Number of accepted requests"
        ),
        "completed_relations": fields.Integer(
            required=True, description="Number of completed relations"
        ),
        "cancelled_relations": fields.Integer(
            required=True, description="Number of cancelled relations"
        ),
        "rejected_requests": fields.Integer(
            required=True, description="Number of rejected relations"
        ),
        "achievements": fields.List(fields.Nested(LIST_TASKS_RESPONSE_BODY)),
    },
)
