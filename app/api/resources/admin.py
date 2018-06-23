from flask import request
from flask_restplus import Resource
from flask_jwt import jwt_required, current_identity

from run import api
from app.api.models.admin import *
from app.api.dao.admin import AdminDAO
from app.api.resources.common import auth_header_parser

admin_ns = api.namespace('Admins', description='Operations related to Admin users')
add_models_to_namespace(admin_ns)

DAO = AdminDAO()  # User data access object


@admin_ns.route('admin/new')
class AssignNewUserAdmin(Resource):

    @classmethod
    @jwt_required()
    @admin_ns.expect(auth_header_parser, assign_and_revoke_user_admin_request_body, validate=True)
    def post(cls):
        """
        Assigns a User as a new Admin.
        """

        if current_identity.is_admin:
            data = request.json
            return DAO.assign_new_user(current_identity.id, data)

        else:
            return {
                       "message": "You don't have admin status. You can't assign other user as admin."
                   }, 403


@admin_ns.route('admin/remove')
class RevokeUserAdmin(Resource):

    @classmethod
    @jwt_required()
    @admin_ns.expect(auth_header_parser, assign_and_revoke_user_admin_request_body, validate=True)
    def post(cls):
        """
        Revoke admin status from another User Admin.
        """

        if current_identity.is_admin:
            data = request.json
            return DAO.revoke_admin_user(current_identity.id, data)

        else:
            return {
                       "message": "You don't have admin status. You can't revoke other admin user."
                   }, 403
