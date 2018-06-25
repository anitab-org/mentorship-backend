from flask_restplus import fields, Model


def add_models_to_namespace(api_namespace):
    api_namespace.models[assign_new_admin_request_body.name] = assign_new_admin_request_body


assign_new_admin_request_body = Model('Assign User model', {
    'user_id': fields.Integer(
        required=True,
        description='The unique identifier of a user'
    )
})
