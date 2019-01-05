# pylint: disable=duplicate-code
from flask_restplus import fields, Model

from app.utils.enum_utils import MentorshipRelationState


def add_models_to_namespace(api_namespace):
    api_namespace.models[
        SEND_MENTORSHIP_REQUEST_BODY.name
    ] = SEND_MENTORSHIP_REQUEST_BODY
    api_namespace.models[
        MENTORSHIP_REQUEST_RESPONSE_BODY.name
    ] = MENTORSHIP_REQUEST_RESPONSE_BODY
    api_namespace.models[
        RELATION_USER_RESPONSE_BODY.name
    ] = RELATION_USER_RESPONSE_BODY
    api_namespace.models[
        CREATE_TASK_REQUEST_BODY.name
    ] = CREATE_TASK_REQUEST_BODY
    api_namespace.models[
        LIST_TASKS_RESPONSE_BODY.name
    ] = LIST_TASKS_RESPONSE_BODY


SEND_MENTORSHIP_REQUEST_BODY = Model(
    "Send mentorship relation request model",
    {
        "mentor_id": fields.Integer(
            required=True, description="Mentorship relation mentor ID"
        ),
        "mentee_id": fields.Integer(
            required=True, description="Mentorship relation mentee ID"
        ),
        "end_date": fields.Float(
            required=True,
            description="Mentorship relation end date "
            "in UNIX timestamp format",
        ),
        "notes": fields.String(
            required=True, description="Mentorship relation notes"
        ),
    },
)

RELATION_USER_RESPONSE_BODY = Model(
    "User",
    {
        "id": fields.Integer(required=True, description="User ID"),
        "name": fields.String(required=True, description="User name"),
    },
)

MENTORSHIP_REQUEST_RESPONSE_BODY = Model(
    "List mentorship relation request model",
    {
        "id": fields.Integer(
            required=True, description="Mentorship relation ID"
        ),
        "action_user_id": fields.Integer(
            required=True, description="Mentorship relation requester user ID"
        ),
        "sent_by_me": fields.Boolean(
            required=True,
            description="Mentorship relation sent by current user indication",
        ),
        "mentor": fields.Nested(RELATION_USER_RESPONSE_BODY),
        "mentee": fields.Nested(RELATION_USER_RESPONSE_BODY),
        "creation_date": fields.Float(
            required=True,
            description="Mentorship relation creation date "
            "in UNIX timestamp format",
        ),
        "accept_date": fields.Float(
            required=True,
            description="Mentorship relation acceptance date "
            "in UNIX timestamp format",
        ),
        "start_date": fields.Float(
            required=True,
            description="Mentorship relation start date "
            "in UNIX timestamp format",
        ),
        "end_date": fields.Float(
            required=True,
            description="Mentorship relation end date "
            "in UNIX timestamp format",
        ),
        "state": fields.Integer(
            required=True,
            enum=MentorshipRelationState.values,
            description="Mentorship relation state",
        ),
        "notes": fields.String(
            required=True, description="Mentorship relation notes"
        ),
    },
)

CREATE_TASK_REQUEST_BODY = Model(
    "Create task request model",
    {
        "description": fields.String(
            required=True, description="Mentorship relation task description"
        )
    },
)

LIST_TASKS_RESPONSE_BODY = Model(
    "List tasks response model",
    {
        "id": fields.Integer(required=True, description="Task ID"),
        "description": fields.String(
            required=True, description="Mentorship relation task description"
        ),
        "is_done": fields.Boolean(
            required=True,
            description="Mentorship relation task is done indication",
        ),
        "created_at": fields.Float(
            required=True,
            description="Task creation date in UNIX timestamp format",
        ),
        "completed_at": fields.Float(
            required=False,
            description="Task completion date in UNIX timestamp format",
        ),
    },
)
