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
    @admin_ns.doc(responses={
        200: messages.USER_IS_NOW_AN_ADMIN['message'],
        400: messages.USER_IS_ALREADY_AN_ADMIN['message'],
        401: f"{messages.TOKEN_HAS_EXPIRED['message']}<br>"
             f"{messages.TOKEN_IS_INVALID['message']}<br>"
             f"{messages.AUTHORISATION_TOKEN_IS_MISSING['message']}",
        403: f"{messages.USER_CANNOT_BE_ASSIGNED_ADMIN_BY_USER['message']}<br>"
             f"{messages.USER_ASSIGN_NOT_ADMIN['message']}",
        404: f"{messages.USER_NOT_FOUND['message']}<br>"
             f"{messages.USER_DOES_NOT_EXIST['message']}"})
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
    @admin_ns.doc(responses={
        200: messages.USER_ADMIN_STATUS_WAS_REVOKED['message'],
        400: messages.USER_IS_NOT_AN_ADMIN['message'],
        401: f"{messages.TOKEN_HAS_EXPIRED['message']}<br>"
             f"{messages.TOKEN_IS_INVALID['message']}<br>"
             f"{messages.AUTHORISATION_TOKEN_IS_MISSING['message']}",
        403: f"{messages.USER_CANNOT_REVOKE_ADMIN_STATUS['message']}<br>"
             f"{messages.USER_REVOKE_NOT_ADMIN['message']}",
        404: f"{messages.USER_NOT_FOUND['message']}<br>"
             f"{messages.USER_DOES_NOT_EXIST['message']}"})
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
