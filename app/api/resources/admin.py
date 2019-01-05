from flask import request
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.dao.user import UserDAO
from app.api.models.admin import (
    add_models_to_namespace,
    ASSIGN_AND_REVOKE_USER_ADMIN_REQUEST_BODY,
)
from app.api.dao.admin import AdminDAO
from app.api.resources.common import AUTH_HEADER_PARSER

ADMIN_NS = Namespace("Admins", description="Operations related to Admin users")
add_models_to_namespace(ADMIN_NS)


@ADMIN_NS.route("admin/new")
class AssignNewUserAdmin(Resource):
    @classmethod
    @jwt_required
    @ADMIN_NS.expect(
        AUTH_HEADER_PARSER,
        ASSIGN_AND_REVOKE_USER_ADMIN_REQUEST_BODY,
        validate=True,
    )
    def post(cls):
        """
        Assigns a User as a new Admin.
        """
        user_id = get_jwt_identity()
        user = UserDAO.get_user(user_id)
        if user.is_admin:
            data = request.json
            return AdminDAO.assign_new_user(user.id, data)

        return (
            {
                "message": "You don't have admin status. "
                           "You can't assign other user as admin."
            },
            403,
        )


@ADMIN_NS.route("admin/remove")
class RevokeUserAdmin(Resource):
    @classmethod
    @jwt_required
    @ADMIN_NS.expect(
        AUTH_HEADER_PARSER,
        ASSIGN_AND_REVOKE_USER_ADMIN_REQUEST_BODY,
        validate=True,
    )
    def post(cls):
        """
        Revoke admin status from another User Admin.
        """
        user_id = get_jwt_identity()
        user = UserDAO.get_user(user_id)
        if user.is_admin:
            data = request.json
            return AdminDAO.revoke_admin_user(user.id, data)

        return (
            {
                "message": "You don't have admin status. "
                           "You can't revoke other admin user."
            },
            403,
        )
