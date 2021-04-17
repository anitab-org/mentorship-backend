from flask_restx import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[create_task_request_body.name] = create_task_request_body
    api_namespace.models[list_tasks_response_body.name] = list_tasks_response_body


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
        "created_at": fields.Float(
            required=True, description="Task creation date in UNIX timestamp format"
        ),
        "completed_at": fields.Float(
            required=False, description="Task completion date in UNIX timestamp format"
        ),
    },
)
