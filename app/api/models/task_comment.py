from flask_restx import fields, Model
from app.api.models.user import public_user_api_model



def add_models_to_namespace(api_namespace):
    api_namespace.models[task_comment_model.name] = task_comment_model
    api_namespace.models[task_comments_model.name] = task_comments_model


task_comment_model = Model(
    "Task comment model",
    {"comment": fields.String(required=True, description="Task comment.")},
)

task_comments_model = Model(
    "Task comments model",
    {
        "id": fields.Integer(required=True, description="Task comment's id."),
        "user": fields.Nested(public_user_api_model),
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
