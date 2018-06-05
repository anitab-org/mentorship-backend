from flask import request
from flask_restplus import Resource, marshal
from flask_jwt import jwt_required, current_identity
from run import api, jwt
from app.api.models.user import *
from app.api.dao.user import UserDAO
from app.api.resources.common import auth_header_parser

users_ns = api.namespace('Users', description='Operations related to users')
add_models_to_namespace(users_ns)

DAO = UserDAO()  # User data access object


@users_ns.route('users/')
class UserList(Resource):

    @classmethod
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(full_user_api_model)
    def get(cls):
        """
        Returns list of all the users.
        """

        return DAO.list_users()


@users_ns.route('users/<int:user_id>')
@users_ns.param('user_id', 'The user identifier')
class OtherUser(Resource):

    @classmethod
    @jwt_required()
    @users_ns.doc('get_user')
    @users_ns.expect(auth_header_parser)
    @api.response(201, 'Success.', public_user_api_model)
    @api.response(400, 'User id is not valid.')
    @api.response(404, 'User does not exist.')
    def get(cls, user_id):
        """
        Returns a user.
        """
        # Validate arguments
        if not OtherUser.validate_param(user_id):
            return {"message": "User id is not valid."}, 400

        requested_user = DAO.get_user(user_id)
        if requested_user is None:
            return {"message": "User does not exist."}, 404
        else:
            return marshal(requested_user, public_user_api_model), 201

    @staticmethod
    def validate_param(user_id):
        return isinstance(user_id, int)


@users_ns.route('user')
@users_ns.response(404, 'User not found.')
class MyUserProfile(Resource):

    @classmethod
    @jwt_required()
    @users_ns.doc('get_user')
    @users_ns.expect(auth_header_parser, validate=True)
    @users_ns.marshal_with(public_user_api_model)  # , skip_none=True
    def get(cls):
        """
        Returns a user.
        """
        user_id = current_identity.id
        return DAO.get_user(user_id)

    @classmethod
    @jwt_required()
    @users_ns.doc('update_user_profile')
    @users_ns.expect(auth_header_parser, update_user_request_body_model)
    @users_ns.response(204, 'User successfully updated.')
    def put(cls):
        """
        Updates user profile
        """

        data = request.json
        user_id = current_identity.id
        return DAO.update_user_profile(user_id, data)

    @classmethod
    @jwt_required()
    @users_ns.doc('delete_user')
    @users_ns.expect(auth_header_parser, validate=True)
    @users_ns.response(204, 'User successfully deleted.')
    def delete(cls):
        """
        Deletes user.
        """
        user_id = current_identity.id
        return DAO.delete_user(user_id)


@users_ns.route('user/change_password')
class ChangeUserPassword(Resource):

    @classmethod
    @jwt_required()
    @users_ns.doc('update_user_password')
    @users_ns.expect(auth_header_parser, change_password_request_data_model, validate=True)
    def put(cls):
        """
        Updates the user's password
        """
        user_id = current_identity.id
        data = request.json
        return DAO.change_password(user_id, data)


@users_ns.route('users/verified')
class VerifiedUser(Resource):

    @classmethod
    @users_ns.doc('get_verified_users')
    @users_ns.marshal_with(public_user_api_model)  # , skip_none=True
    def get(cls):
        """
        Returns all verified users.
        """
        return DAO.list_users(is_verified=True)


@users_ns.route('register')
class UserRegister(Resource):

    @classmethod
    @users_ns.doc('create_user')
    @users_ns.response(201, 'User successfully created.')
    @users_ns.expect(register_user_api_model)
    def post(cls):
        """
        Creates a new user.
        """

        data = request.json
        user = DAO.create_user(data)

        if user is None:
            return {"message": "User was created successfully"}, 201
        else:
            return {"message": "A user with that username already exists"}, 400


@users_ns.route('login')
class LoginUser(Resource):

    @classmethod
    @users_ns.doc('login')
    @users_ns.expect(login_request_body_model)  # , skip_none=True
    def post(cls):
        """
        Login user.
        """
        # pass
        return jwt.request_handler()
