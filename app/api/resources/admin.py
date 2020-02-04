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
@admin_ns.response(200, '%s'%messages.USER_IS_NOW_AN_ADMIN)
@admin_ns.response(400, '%s'%messages.USER_IS_ALREADY_AN_ADMIN)
@admin_ns.response(401, '%s\n%s\n%s'%(
        messages.TOKEN_HAS_EXPIRED,
        messages.TOKEN_IS_INVALID,
        messages.AUTHORISATION_TOKEN_IS_MISSING
        )
    )
@admin_ns.response(403, '%s'%messages.USER_ASSIGN_NOT_ADMIN)
@admin_ns.response(404, '%s'%messages.USER_DOES_NOT_EXIST)
class AssignNewUserAdmin(Resource):

    @classmethod
    @jwt_required
    @admin_ns.expect(auth_header_parser, assign_and_revoke_user_admin_request_body, validate=True)
    def post(cls):
        """
        Assigns a User as a new Admin.

        An existing admin can use this endpoint to designate another user as an admin.
        This is done by passing "user_id" of that particular user.
        """
        user_id = get_jwt_identity()
        user = UserDAO.get_user(user_id)
        if user.is_admin:
            data = request.json
            return AdminDAO.assign_new_user(user.id, data)

        else:
            return messages.USER_ASSIGN_NOT_ADMIN, 403


@admin_ns.route('admin/remove')
@admin_ns.response(200, '%s'%messages.USER_ADMIN_STATUS_WAS_REVOKED)
@admin_ns.response(400, '%s'%messages.USER_IS_NOT_AN_ADMIN)
@admin_ns.response(401, '%s\n%s\n%s'%(
        messages.TOKEN_HAS_EXPIRED,
        messages.TOKEN_IS_INVALID,
        messages.AUTHORISATION_TOKEN_IS_MISSING
        )
    )
@admin_ns.response(403, '%s'%messages.USER_REVOKE_NOT_ADMIN)
@admin_ns.response(404, '%s'%messages.USER_DOES_NOT_EXIST)
class RevokeUserAdmin(Resource):

    @classmethod
    @jwt_required
    @admin_ns.expect(auth_header_parser, assign_and_revoke_user_admin_request_body, validate=True)
    def post(cls):
        """
        Revoke admin status from another User Admin.

        An existing admin can use this endpoint to revoke admin status of another user.
        This is done by passing "user_id" of that particular user.
        """
        user_id = get_jwt_identity()
        user = UserDAO.get_user(user_id)
        if user.is_admin:
            data = request.json
            return AdminDAO.revoke_admin_user(user.id, data)

        else:
            return messages.USER_REVOKE_NOT_ADMIN, 403
