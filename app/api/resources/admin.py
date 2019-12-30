from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import messages
from app.api.dao.user import UserDAO
from app.api.models.admin import *
from app.api.dao.admin import AdminDAO
from app.api.resources.common import auth_header_parser

admin_ns = Namespace('Admins', description='Operations related to Admin users')
add_models_to_namespace(admin_ns)


@admin_ns.route('admin/new')
class AssignNewUserAdmin(Resource):

    @classmethod
    @jwt_required
    @admin_ns.expect(auth_header_parser, assign_and_revoke_user_admin_request_body, validate=True)
    @admin_ns.response(400, 'User is already an admin.')
    @admin_ns.response(403, 'Assigning user is not an admin.')
    @admin_ns.response(404, 'User not found.')
    def post(cls):
        """
        Assigns a User as a new Admin.
        """
        user_id = get_jwt_identity()
        user = UserDAO.get_user(user_id)
        if user.is_admin:
            data = request.json
            return AdminDAO.assign_new_user(user.id, data)

        else:
            return messages.USER_ASSIGN_NOT_ADMIN, 403


@admin_ns.route('admin/remove')
class RevokeUserAdmin(Resource):

    @classmethod
    @jwt_required
    @admin_ns.expect(auth_header_parser, assign_and_revoke_user_admin_request_body, validate=True)
    @admin_ns.response(400, 'User is not an admin.')
    @admin_ns.response(403, 'Revoking user is not an admin.')
    @admin_ns.response(404, 'User not found.')
    def post(cls):
        """
        Revoke admin status from another User Admin.
        """
        user_id = get_jwt_identity()
        user = UserDAO.get_user(user_id)
        if user.is_admin:
            data = request.json
            return AdminDAO.revoke_admin_user(user.id, data)

        else:
            return messages.USER_REVOKE_NOT_ADMIN, 403
