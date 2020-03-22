from flask_restplus import fields, Model

from app.utils.enum_utils import MentorshipRelationState


def add_models_to_namespace(api_namespace):
    api_namespace.models[
        send_mentorship_request_body.name
    ] = send_mentorship_request_body
    api_namespace.models[
        mentorship_request_response_body.name
    ] = mentorship_request_response_body
    api_namespace.models[relation_user_response_body.name] = relation_user_response_body
    api_namespace.models[create_task_request_body.name] = create_task_request_body
    api_namespace.models[list_tasks_response_body.name] = list_tasks_response_body
    api_namespace.models[
        mentorship_request_response_body_for_user_dashboard_body.name
    ] = mentorship_request_response_body_for_user_dashboard_body
    api_namespace.models[user_dashboard_user_details.name] = user_dashboard_user_details
    api_namespace.models[task_comment_model.name] = task_comment_model
    api_namespace.models[task_comments_model.name] = task_comments_model


send_mentorship_request_body = Model(
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
            description="Mentorship relation end date in UNIX timestamp format",
        ),
        "notes": fields.String(required=True, description="Mentorship relation notes"),
    },
)

relation_user_response_body = Model(
    "User",
    {
        "id": fields.Integer(required=True, description="User ID"),
        "name": fields.String(required=True, description="User name"),
    },
)

mentorship_request_response_body = Model(
    "List mentorship relation request model",
    {
        "id": fields.Integer(required=True, description="Mentorship relation ID"),
        "action_user_id": fields.Integer(
            required=True, description="Mentorship relation requester user ID"
        ),
        "sent_by_me": fields.Boolean(
            required=True,
            description="Mentorship relation sent by current user indication",
        ),
        "mentor": fields.Nested(relation_user_response_body),
        "mentee": fields.Nested(relation_user_response_body),
        "creation_date": fields.Float(
            required=True,
            description="Mentorship relation creation date in UNIX timestamp format",
        ),
        "accept_date": fields.Float(
            required=True,
            description="Mentorship relation acceptance date in UNIX timestamp format",
        ),
        "start_date": fields.Float(
            required=True,
            description="Mentorship relation start date in UNIX timestamp format",
        ),
        "end_date": fields.Float(
            required=True,
            description="Mentorship relation end date in UNIX timestamp format",
        ),
        "state": fields.Integer(
            required=True,
            enum=MentorshipRelationState.values,
            description="Mentorship relation state",
        ),
        "notes": fields.String(required=True, description="Mentorship relation notes"),
    },
)

create_task_request_body = Model(
    "Create task request model",
    {
        "description": fields.String(
            required=True, description="Mentorship relation task description"
        )
    },
)

list_tasks_response_body = Model(
    "List tasks response model",
    {
        "id": fields.Integer(required=True, description="Task ID"),
        "description": fields.String(
            required=True, description="Mentorship relation task description"
        ),
        "is_done": fields.Boolean(
            required=True, description="Mentorship relation task is done indication"
        ),
        "created_at": fields.Float(
            required=True, description="Task creation date in UNIX timestamp format"
        ),
        "completed_at": fields.Float(
            required=False, description="Task completion date in UNIX timestamp format"
        ),
    },
)

user_dashboard_user_details = Model(
    "user details for dashboard",
    {
        "id": fields.Integer(required=True, description="user ID"),
        "user_name": fields.String(
            required=True, description="Mentorship relation user name"
        ),
        "photo_url": fields.String(
            required=True, description="Mentorship relation user profile picture URL"
        ),
    },
)

mentorship_request_response_body_for_user_dashboard_body = Model(
    "List mentorship relation request model for user dashboard",
    {
        "id": fields.Integer(required=True, description="Mentorship relation ID"),
        "action_user_id": fields.Integer(
            required=True, description="Mentorship relation requester user ID"
        ),
        "mentor": fields.Nested(user_dashboard_user_details),
        "mentee": fields.Nested(user_dashboard_user_details),
        "creation_date": fields.Float(
            required=True,
            description="Mentorship relation creation date in UNIX timestamp format",
        ),
        "accept_date": fields.Float(
            required=True,
            description="Mentorship relation acceptance date in UNIX timestamp format",
        ),
        "start_date": fields.Float(
            required=True,
            description="Mentorship relation start date in UNIX timestamp format",
        ),
        "end_date": fields.Float(
            required=True,
            description="Mentorship relation end date in UNIX timestamp format",
        ),
        "state": fields.Integer(
            required=True,
            enum=MentorshipRelationState.values,
            description="Mentorship relation state",
        ),
        "notes": fields.String(required=True, description="Mentorship relation notes"),
    },
)

task_comment_model = Model(
    "Task comment model.",
    {"comment": fields.String(required=True, description="Task comment.")},
)

task_comments_model = Model(
    "Task comments model.",
    {
        "id": fields.Integer(required=True, description="Task comment's id."),
        "user_id": fields.Integer(required=True, description="User's id."),
        "task_id": fields.Integer(required=True, description="Task's id."),
        "relation_id": fields.Integer(required=True, description="Relation's id."),
        "creation_date": fields.Float(
            required=True, description="Creation date of the task comment."
        ),
        "modification_date": fields.Float(
            required=False, description="Modification date of the task comment."
        ),
        "comment": fields.String(required=True, description="Task comment."),
    },
)
