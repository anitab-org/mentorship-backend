from flask_restplus import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from app.run import api, jwt
from app.api.models.user import *
from app.api.dao.admin import AdminDAO

admin_ns = api.namespace('Admins', description='Operations related to Admin users')
add_models_to_namespace(admin_ns)

DAO = AdminDAO()  # User data access object


@admin_ns.route('admin/new')
class AssignNewUserAdmin(Resource):

    @jwt_required()
    @admin_ns.doc('assign_new_admin_user')
    def post(self):
        """
        Assigns a User as a new Admin.
        """

        if current_identity.is_admin:
            data = AssignNewUserAdmin.assign_new_admin_parser.parse_args()
            return DAO.assign_new_user(data)

        else:
            return {
                       "message": "You don't have admin status. You can't assign another admin"
                   }, 401

    assign_new_admin_parser = reqparse.RequestParser()
    assign_new_admin_parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be blank."
                        )