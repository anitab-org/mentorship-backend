from flask import request
from flask_restplus import Resource
from flask_jwt import jwt_required, current_identity
from app.run import api, jwt
from app.api.models.user import *
from app.api.dao.admin import AdminDAO

admin_ns = api.namespace('Admins', description='Operations related to Admin users')
add_models_to_namespace(admin_ns)

DAO = AdminDAO()  # User data access object


@admin_ns.route('admin/new/<int:new_admin_id>')
@admin_ns.param('new_admin_id', 'The identifier of the user that is being assigned as an admin')
class OtherUser(Resource):

    @jwt_required()
    @admin_ns.doc('assign_new_admin_user')
    def post(self, new_admin_id):
        """
        Assigns a User as a new Admin.
        """

        if current_identity.is_admin:
            return DAO.assign_new_user(new_admin_id)

        else:
            return {
                       "message": "You don't have admin status. You can't assign another admin"
                   }, 401
