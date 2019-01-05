from flask_restplus import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[
        ASSIGN_AND_REVOKE_USER_ADMIN_REQUEST_BODY.name
    ] = ASSIGN_AND_REVOKE_USER_ADMIN_REQUEST_BODY


ASSIGN_AND_REVOKE_USER_ADMIN_REQUEST_BODY = Model(
    "Assign User model",
    {
        "user_id": fields.Integer(
            required=True, description="The unique identifier of a user"
        )
    },
)
