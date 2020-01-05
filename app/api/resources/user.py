from datetime import datetime

from flask import request
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restplus import Resource, marshal, Namespace

from app import messages
from app.api.validations.user import *
from app.api.email_utils import send_email_verification_message
from app.api.models.user import *
from app.api.dao.user import UserDAO
from app.api.resources.common import auth_header_parser

users_ns = Namespace('Users', description='Operations related to users')
add_models_to_namespace(users_ns)

DAO = UserDAO()  # User data access object


@users_ns.route('users')
class UserList(Resource):

    @classmethod
    @jwt_required
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(public_user_api_model)
    @users_ns.expect(auth_header_parser)
    @users_ns.response(200, messages.RETURNED_USERS_SUCCESSFULLY['message'])
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    def get(cls):
        """
        Returns list of all the users.
        """
        user_id = get_jwt_identity()
        return DAO.list_users(user_id)


@users_ns.route('users/<int:user_id>')
@users_ns.param('user_id', 'The user identifier')
class OtherUser(Resource):

    @classmethod
    @jwt_required
    @users_ns.doc('get_user')
    @users_ns.expect(auth_header_parser)
    @users_ns.response(201, messages.SUCCESSFUL_RESPONSE['message'], public_user_api_model)
    @users_ns.response(400, messages.USER_ID_IS_NOT_VALID['message'])
    @users_ns.response(404, messages.USER_DOES_NOT_EXIST['message'])
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    def get(cls, user_id):
        """
        Returns a user.
        """
        # Validate arguments
        if not OtherUser.validate_param(user_id):
            return messages.USER_ID_IS_NOT_VALID, 400

        requested_user = DAO.get_user(user_id)
        if requested_user is None:
            return messages.USER_DOES_NOT_EXIST, 404
        else:
            return marshal(requested_user, public_user_api_model), 201

    @staticmethod
    def validate_param(user_id):
        return isinstance(user_id, int)


@users_ns.route('user')
@users_ns.response(404, messages.USER_NOT_FOUND['message'])
class MyUserProfile(Resource):

    @classmethod
    @jwt_required
    @users_ns.doc('get_user')
    @users_ns.expect(auth_header_parser, validate=True)
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    @users_ns.marshal_with(full_user_api_model)  # , skip_none=True
    def get(cls):
        """
        Returns a user.
        """
        user_id = get_jwt_identity()
        return DAO.get_user(user_id)

    @classmethod
    @jwt_required
    @users_ns.doc('update_user_profile')
    @users_ns.expect(auth_header_parser, update_user_request_body_model)
    @users_ns.response(200, messages.USER_SUCCESSFULLY_UPDATED['message'])
    @users_ns.response(404, messages.USER_NOT_FOUND['message'])
    @users_ns.response(400, messages.NEW_USERNAME_INPUT_BY_USER_IS_INVALID['message'] + '\n' +
                       messages.NAME_INPUT_BY_USER_IS_INVALID['message'] + '\n' +
                       messages.FIELD_NEED_MENTORING_IS_NOT_VALID['message'] + '\n' +
                       messages.FIELD_AVAILABLE_TO_MENTOR_IS_INVALID['message'] + '\n' +
                       messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS['message'])
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    def put(cls):
        """
        Updates user profile
        """

        data = request.json

        is_valid = validate_update_profile_request_data(data)

        if is_valid != {}:
            return is_valid, 400

        user_id = get_jwt_identity()
        return DAO.update_user_profile(user_id, data)

    @classmethod
    @jwt_required
    @users_ns.doc('delete_user')
    @users_ns.expect(auth_header_parser, validate=True)
    @users_ns.response(200, messages.USER_SUCCESSFULLY_DELETED['message'])
    @users_ns.response(404, messages.USER_NOT_FOUND['message'])
    @users_ns.response(400, messages.USER_CANT_DELETE['message'])
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    def delete(cls):
        """
        Deletes user.
        """
        user_id = get_jwt_identity()
        return DAO.delete_user(user_id)


@users_ns.route('user/change_password')
class ChangeUserPassword(Resource):

    @classmethod
    @jwt_required
    @users_ns.doc('update_user_password')
    @users_ns.expect(auth_header_parser, change_password_request_data_model, validate=True)
    @users_ns.response(201, messages.PASSWORD_SUCCESSFULLY_UPDATED['message'])
    @users_ns.response(400, messages.CURRENT_PASSWORD_FIELD_IS_MISSING['message'] + '\n' +
                       messages.NEW_PASSWORD_FIELD_IS_MISSING['message'] + '\n' +
                       messages.USER_INPUTS_SPACE_IN_PASSWORD['message'] + '\n' +
                       messages.USER_ENTERED_INCORRECT_PASSWORD['message'])
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    def put(cls):
        """
        Updates the user's password
        """
        user_id = get_jwt_identity()
        data = request.json
        is_valid = validate_new_password(data)
        if is_valid != {}:
            return is_valid, 400
        return DAO.change_password(user_id, data)


@users_ns.route('users/verified')
class VerifiedUser(Resource):

    @classmethod
    @jwt_required
    @users_ns.doc('get_verified_users')
    @users_ns.marshal_list_with(public_user_api_model)  # , skip_none=True
    @users_ns.expect(auth_header_parser)
    @users_ns.response(200, messages.RETURNED_USERS_SUCCESSFULLY['message'])
    def get(cls):
        """
        Returns all verified users.
        """
        user_id = get_jwt_identity()
        return DAO.list_users(user_id, is_verified=True)


@users_ns.route('register')
class UserRegister(Resource):

    @classmethod
    @users_ns.doc('create_user')
    @users_ns.response(201, messages.USER_SUCCESSFULLY_CREATED['message'])
    @users_ns.response(200, messages.USER_WAS_CREATED_SUCCESSFULLY['message'])
    @users_ns.response(400, messages.NAME_FIELD_IS_MISSING['message'] + '\n' +
                       messages.USERNAME_FIELD_IS_MISSING['message'] + '\n' +
                       messages.PASSWORD_FIELD_IS_MISSING['message'] + '\n' +
                       messages.EMAIL_FIELD_IS_MISSING['message'] + '\n' +
                       messages.TERMS_AND_CONDITIONS_FIELD_IS_MISSING['message'] + '\n' +
                       messages.NAME_USERNAME_AND_PASSWORD_NOT_IN_STRING_FORMAT['message'] + '\n' +
                       messages.TERMS_AND_CONDITIONS_ARE_NOT_CHECKED['message'] + '\n' +
                       messages.NAME_INPUT_BY_USER_IS_INVALID['message'] + '\n' +
                       messages.EMAIL_INPUT_BY_USER_IS_INVALID['message'] + '\n' +
                       messages.USERNAME_INPUT_BY_USER_IS_INVALID['message'] + '\n' +
                       messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS['message'] + '\n' +
                       messages.USER_USES_AN_EMAIL_ID_THAT_ALREADY_EXISTS['message'])
    @users_ns.expect(register_user_api_model, validate=True)
    def post(cls):
        """
        Creates a new user.
        """

        data = request.json

        is_valid = validate_user_registration_request_data(data)

        if is_valid != {}:
            return is_valid, 400

        result = DAO.create_user(data)

        if result[1] is 200:
            send_email_verification_message(data['name'], data['email'])

        return result


@users_ns.route('user/confirm_email/<string:token>')
@users_ns.param('token', 'Token sent to the user\'s email')
@users_ns.response(200, messages.ACCOUNT_ALREADY_CONFIRMED['message'] + '\n' +
                   messages.ACCOUNT_ALREADY_CONFIRMED_AND_THANKS['message'])
@users_ns.response(400, messages.EMAIL_EXPIRED_OR_TOKEN_IS_INVALID['message'])
class UserEmailConfirmation(Resource):

    @classmethod
    def get(cls, token):
        """Confirms the user's account."""

        return DAO.confirm_registration(token)


@users_ns.route('user/resend_email')
class UserResendEmailConfirmation(Resource):

    @classmethod
    @users_ns.expect(resend_email_request_body_model)
    @users_ns.response(200, messages.EMAIL_VERIFICATION_MESSAGE['message'])
    @users_ns.response(400, messages.EMAIL_FIELD_IS_MISSING['message'] + '\n' +
                       messages.EMAIL_INPUT_BY_USER_IS_INVALID['message'])
    @users_ns.response(403, messages.USER_ALREADY_CONFIRMED_ACCOUNT['message'])
    @users_ns.response(404, messages.USER_IS_NOT_REGISTERED_IN_THE_SYSTEM['message'])
    def post(cls):
        """Sends the user a new verification email."""

        data = request.json

        is_valid = validate_resend_email_request_data(data)

        if is_valid != {}:
            return is_valid, 400

        user = DAO.get_user_by_email(data['email'])
        if user is None:
            return messages.USER_IS_NOT_REGISTERED_IN_THE_SYSTEM, 404

        if user.is_email_verified:
            return messages.USER_ALREADY_CONFIRMED_ACCOUNT, 403

        send_email_verification_message(user.name, data['email'])

        return messages.EMAIL_VERIFICATION_MESSAGE, 200


@users_ns.route('refresh')
class RefreshUser(Resource):

    @classmethod
    @jwt_refresh_token_required
    @users_ns.doc('refresh')
    @users_ns.response(200, messages.SUCCESSFUL_REFRESH['message'], refresh_response_body_model)
    @users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                       + messages.TOKEN_IS_INVALID['message'] + '\n'
                       + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
    @users_ns.expect(auth_header_parser)
    def post(cls):
        """Refresh user's access

        The return value is an access token and the expiry timestamp.
        The token is valid for 1 week.
        """
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)

        from run import application
        access_expiry = datetime.utcnow() + application.config.get('JWT_ACCESS_TOKEN_EXPIRES')

        return {
            'access_token': access_token,
            'access_expiry': access_expiry.timestamp(),
        }, 200


@users_ns.route('login')
class LoginUser(Resource):

    @classmethod
    @users_ns.doc('login')
    @users_ns.response(200, messages.SUCCESSFUL_LOGIN['message'], login_response_body_model)
    @users_ns.response(400, messages.USERNAME_FIELD_IS_MISSING['message'] + '\n' +
                       messages.PASSWORD_FIELD_IS_MISSING['message'])
    @users_ns.response(403, messages.USER_HAS_NOT_VERIFIED_EMAIL_BEFORE_LOGIN['message'])
    @users_ns.response(404, messages.WRONG_USERNAME_OR_PASSWORD['message'])
    @users_ns.expect(login_request_body_model)
    def post(cls):
        """
        Login user

        The user can login with (username or email) + password.
        Username field can be either the User's username or the email.
        The return value is an access token and the expiry timestamp.
        The token is valid for 1 week.
        """
        # if not request.is_json:
        #     return {'msg': 'Missing JSON in request'}, 400

        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return messages.USERNAME_FIELD_IS_MISSING, 400
        if not password:
            return messages.PASSWORD_FIELD_IS_MISSING, 400

        user = DAO.authenticate(username, password)

        if not user:
            return messages.WRONG_USERNAME_OR_PASSWORD, 404

        if not user.is_email_verified:
            return messages.USER_HAS_NOT_VERIFIED_EMAIL_BEFORE_LOGIN, 403

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        from run import application
        access_expiry = datetime.utcnow() + application.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        refresh_expiry = datetime.utcnow() + application.config.get('JWT_REFRESH_TOKEN_EXPIRES')

        return {
            'access_token': access_token,
            'access_expiry': access_expiry.timestamp(),
            'refresh_token': refresh_token,
            'refresh_expiry': refresh_expiry.timestamp(),
        }, 200


@users_ns.route('home')
@users_ns.expect(auth_header_parser, validate=True)
@users_ns.response(200, messages.SUCCESSFUL_RESPONSE['message'], home_response_body_model)
@users_ns.response(404, messages.USER_NOT_FOUND['message'])
@users_ns.response(401, messages.TOKEN_HAS_EXPIRED['message'] + '\n'
                   + messages.TOKEN_IS_INVALID['message'] + '\n'
                   + messages.AUTHORISATION_TOKEN_IS_MISSING['message'])
class UserHomeStatistics(Resource):
    @classmethod
    @jwt_required
    @users_ns.expect(auth_header_parser)
    def get(cls):
        """Get Statistics regarding the current user

        Returns:
            A dict containing user stats
        """
        user_id = get_jwt_identity()
        stats = DAO.get_user_statistics(user_id)
        if not stats:
            return messages.USER_NOT_FOUND, 404

        return stats, 200
