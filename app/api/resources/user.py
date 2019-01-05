from datetime import datetime
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required,
)
from flask_restplus import Resource, marshal, Namespace

from app.api.validations.user import (
    validate_new_password,
    validate_resend_email_request_data,
    validate_update_profile_request_data,
    validate_user_registration_request_data,
)
from app.api.email_utils import send_email_verification_message
from app.api.models.user import (
    LOGIN_RESPONSE_BODY_MODEL,
    add_models_to_namespace,
    CHANGE_PASSWORD_REQUEST_DATA_MODEL,
    FULL_USER_API_MODEL,
    HOME_RESPONSE_BODY_MODEL,
    LOGIN_REQUEST_BODY_MODEL,
    PUBLIC_USER_API_MODEL,
    REFRESH_RESPONSE_BODY_MODEL,
    REGISTER_USER_API_MODEL,
    RESEND_EMAIL_REQUEST_BODY_MODEL,
    UPDATE_USER_REQUEST_BODY_MODEL,
)
from app.api.dao.user import UserDAO
from app.api.resources.common import AUTH_HEADER_PARSER

USERS_NS = Namespace("Users", description="Operations related to users")
add_models_to_namespace(USERS_NS)

DAO = UserDAO()  # User data access object


@USERS_NS.route("users")
class UserList(Resource):
    @classmethod
    @jwt_required
    @USERS_NS.doc("list_users")
    @USERS_NS.marshal_list_with(PUBLIC_USER_API_MODEL)
    @USERS_NS.expect(AUTH_HEADER_PARSER)
    def get(cls):
        """
        Returns list of all the users.
        """
        user_id = get_jwt_identity()
        return DAO.list_users(user_id)


@USERS_NS.route("users/<int:user_id>")
@USERS_NS.param("user_id", "The user identifier")
class OtherUser(Resource):
    @classmethod
    @jwt_required
    @USERS_NS.doc("get_user")
    @USERS_NS.expect(AUTH_HEADER_PARSER)
    @USERS_NS.response(201, "Success.", PUBLIC_USER_API_MODEL)
    @USERS_NS.response(400, "User id is not valid.")
    @USERS_NS.response(404, "User does not exist.")
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
        return marshal(requested_user, PUBLIC_USER_API_MODEL), 201

    @staticmethod
    def validate_param(user_id):
        return isinstance(user_id, int)


@USERS_NS.route("user")
@USERS_NS.response(404, "User not found.")
class MyUserProfile(Resource):
    @classmethod
    @jwt_required
    @USERS_NS.doc("get_user")
    @USERS_NS.expect(AUTH_HEADER_PARSER, validate=True)
    @USERS_NS.marshal_with(FULL_USER_API_MODEL)  # , skip_none=True
    def get(cls):
        """
        Returns a user.
        """
        user_id = get_jwt_identity()
        return DAO.get_user(user_id)

    @classmethod
    @jwt_required
    @USERS_NS.doc("update_user_profile")
    @USERS_NS.expect(AUTH_HEADER_PARSER, UPDATE_USER_REQUEST_BODY_MODEL)
    @USERS_NS.response(200, "User successfully updated.")
    @USERS_NS.response(404, "User not found.")
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
    @USERS_NS.doc("delete_user")
    @USERS_NS.expect(AUTH_HEADER_PARSER, validate=True)
    @USERS_NS.response(200, "User successfully deleted.")
    @USERS_NS.response(404, "User not found.")
    def delete(cls):
        """
        Deletes user.
        """
        user_id = get_jwt_identity()
        return DAO.delete_user(user_id)


@USERS_NS.route("user/change_password")
class ChangeUserPassword(Resource):
    @classmethod
    @jwt_required
    @USERS_NS.doc("update_user_password")
    @USERS_NS.expect(
        AUTH_HEADER_PARSER, CHANGE_PASSWORD_REQUEST_DATA_MODEL, validate=True
    )
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


@USERS_NS.route("users/verified")
class VerifiedUser(Resource):
    @classmethod
    @jwt_required
    @USERS_NS.doc("get_verified_users")
    @USERS_NS.marshal_list_with(PUBLIC_USER_API_MODEL)  # , skip_none=True
    @USERS_NS.expect(AUTH_HEADER_PARSER)
    def get(cls):
        """
        Returns all verified users.
        """
        user_id = get_jwt_identity()
        return DAO.list_users(user_id, is_verified=True)


@USERS_NS.route("register")
class UserRegister(Resource):
    @classmethod
    @USERS_NS.doc("create_user")
    @USERS_NS.response(201, "User successfully created.")
    @USERS_NS.expect(REGISTER_USER_API_MODEL, validate=True)
    def post(cls):
        """
        Creates a new user.
        """

        data = request.json

        is_valid = validate_user_registration_request_data(data)

        if is_valid != {}:
            return is_valid, 400

        result = DAO.create_user(data)

        if result[1] == 200:
            send_email_verification_message(data["name"], data["email"])

        return result


@USERS_NS.route("user/confirm_email/<string:token>")
@USERS_NS.param("token", "Token sent to the user's email")
class UserEmailConfirmation(Resource):
    @classmethod
    def get(cls, token):
        """Confirms the user's account."""

        return DAO.confirm_registration(token)


@USERS_NS.route("user/resend_email")
class UserResendEmailConfirmation(Resource):
    @classmethod
    @USERS_NS.expect(RESEND_EMAIL_REQUEST_BODY_MODEL)
    def post(cls):
        """Sends the user a new verification email."""

        data = request.json

        is_valid = validate_resend_email_request_data(data)

        if is_valid != {}:
            return is_valid, 400

        user = DAO.get_user_by_email(data["email"])
        if user is None:
            return {"message": "You are not registered in the system."}, 404

        if user.is_email_verified:
            return {"message": "You already confirm your email."}, 403

        send_email_verification_message(user.name, data["email"])

        return (
            {
                "message": "Check your email, "
                           "a new verification email was sent."
            },
            200,
        )


@USERS_NS.route('refresh')
class RefreshUser(Resource):

    @classmethod
    @jwt_refresh_token_required
    @USERS_NS.doc('refresh')
    @USERS_NS.response(200, 'Successful refresh', REFRESH_RESPONSE_BODY_MODEL)
    @USERS_NS.expect(AUTH_HEADER_PARSER)
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


@USERS_NS.route('login')
class LoginUser(Resource):
    @classmethod
    @USERS_NS.doc("login")
    @USERS_NS.response(200, "Successful login", LOGIN_RESPONSE_BODY_MODEL)
    @USERS_NS.expect(LOGIN_REQUEST_BODY_MODEL)
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

        username = request.json.get("username", None)
        password = request.json.get("password", None)

        if not username:
            return {"message": "The field username is missing."}, 400
        if not password:
            return {"message": "The field password is missing."}, 400

        user = DAO.authenticate(username, password)

        if not user:
            return {"message": "Username or password is wrong."}, 404

        if not user.is_email_verified:
            return {"message": "Please verify your email before login."}, 403

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        from run import application

        access_expiry = datetime.utcnow() + application.config.get('JWT_ACCESS_TOKEN_EXPIRES')
        refresh_expiry = datetime.utcnow() + application.config.get('JWT_REFRESH_TOKEN_EXPIRES')

        return {
            "access_token": access_token,
            "access_expiry": access_expiry.timestamp(),
            "refresh_token": refresh_token,
            "refresh_expiry": refresh_expiry.timestamp(),
        }, 200


@USERS_NS.route("home")
@USERS_NS.expect(AUTH_HEADER_PARSER, validate=True)
@USERS_NS.response(200, "Successful response", HOME_RESPONSE_BODY_MODEL)
@USERS_NS.response(404, "User not found")
class UserHomeStatistics(Resource):
    @classmethod
    @jwt_required
    @USERS_NS.expect(AUTH_HEADER_PARSER)
    def get(cls):
        """Get Statistics regarding the current user

        Returns:
            A dict containing user stats
        """
        user_id = get_jwt_identity()
        stats = DAO.get_user_statistics(user_id)
        if not stats:
            return {"message": "User not found"}, 404

        return stats, 200
