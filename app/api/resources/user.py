from flask_restplus import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from app.run import api
from app.api.models.user import *
from app.api.dao.user import UserDAO

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

        #### just checking if this works
        # user_test = UserModel("Maria", "MariaJoana", "asdf")
        # user_test.save_to_db()
        #
        # user_test2 = UserModel("JOnh", "JOnhath", "sdfsfd")
        # user_test2.save_to_db()
        ####

        return DAO.list_users()


@users_ns.route('register')
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('terms_and_conditions_checked',
                        type=bool,
                        required=True,
                        help="This field cannot be blank."
                        )

    @classmethod
    @users_ns.doc('create_user')
    @users_ns.response(201, 'User successfully created.')
    @users_ns.expect(register_user_api_model)
    def post(cls):
        """
        Creates a new user.
        """

        data = UserRegister.parser.parse_args()

        user = DAO.create_user(data)

        if user is None:
            return {"message": "User was created successfully"}, 201
        else:
            return {"message": "A user with that username already exists"}, 400


@users_ns.route('users/<int:user_id>')
@users_ns.response(404, 'User not found.')
@users_ns.param('user_id', 'The user identifier')
class OtherUser(Resource):

    @classmethod
    @jwt_required()
    @users_ns.doc('get_user')
    @users_ns.marshal_with(public_user_api_model)  # , skip_none=True
    def get(cls, user_id):
        """
        Returns a user.
        """
        return DAO.get_user(user_id)


@users_ns.route('user')
@users_ns.response(404, 'User not found.')
class MyUserProfile(Resource):

    @classmethod
    @jwt_required()
    @users_ns.doc('get_user')
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
    @users_ns.expect(update_user_request_data_model)
    @users_ns.response(204, 'User successfully updated.')
    def put(cls):
        """
        Updates My User Profile
        JSON body
        ```
        {
          "name": "User name",
          "username": "User username",
          "password": "User password"
        }
        ```
        """

        data = MyUserProfile.update_profile_parser.parse_args()
        user_id = current_identity.id
        return DAO.update_user_profile(user_id, data)

    @classmethod
    @jwt_required()
    @users_ns.doc('delete_user')
    @users_ns.response(204, 'User successfully deleted.')
    def delete(cls):
        """
        Deletes user.
        """
        user_id = current_identity.id
        return DAO.delete_user(user_id)

    update_profile_parser = reqparse.RequestParser()
    update_profile_parser.add_argument('name',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('username',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('bio',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('location',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('occupation',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('slack_username',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('social_media_links',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('skills',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('interests',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('resume_url',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('photo_url',
                                       type=str,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('need_mentoring',
                                       type=bool,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )
    update_profile_parser.add_argument('available_to_mentor',
                                       type=bool,
                                       required=False,
                                       help="This field can be blank.",
                                       nullable=True
                                       )


@users_ns.route('user/change_password')
class ChangeUserPassword(Resource):

    @classmethod
    @jwt_required()
    @users_ns.doc('update_user_password')
    @users_ns.expect(change_password_request_data_model)
    def put(cls):
        """
        Updates the user's password

        Request body:

        ```
        {
          "current_password": "User current password",
          "new_password": "User password"
        }
        ```
        """
        user_id = current_identity.id
        data = ChangeUserPassword.parser.parse_args()
        return DAO.change_password(user_id, data)

    parser = reqparse.RequestParser()
    parser.add_argument('current_password',
                        type=str,
                        required=True,
                        help="Current password field cannot be blank."
                        )
    parser.add_argument('new_password',
                        type=str,
                        required=True,
                        help="New password field cannot be blank."
                        )


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
