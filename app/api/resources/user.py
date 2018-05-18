from flask import request
from flask_restplus import Resource, reqparse, fields
from flask_jwt import jwt_required
from app.run import api, jwt
from app.api.models.user import *
from app.api.dao.user import UserDAO

ns = api.namespace('users', description='Operations related to users')
add_models_to_namespace(ns)

DAO = UserDAO()  # User data access object

@ns.route('/')
class UserList(Resource):

    @ns.doc('list_users')
    @ns.marshal_list_with(full_user_api_model)
    def get(self):
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


@ns.route('/register')
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
    parser.add_argument('security_question',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('security_answer',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('terms_and_conditions_checked',
        type=bool,
        required=True,
        help="This field cannot be blank."
    )

    @ns.doc('create_user')
    @ns.response(201, 'User successfully created.')
    @ns.expect(register_user_api_model)
    def post(self):
        """
        Creates a new user.
        """

        #data = api.payload
        data = UserRegister.parser.parse_args()

        user = DAO.create_user(data)

        if user is None:
            return {"message": "User was created successfully"}, 201
        else:
            return {"message": "A user with that username already exists"}, 400


@ns.route('/<int:id>')
@ns.response(404, 'User not found.')
@ns.param('id', 'The user identifier')
class User(Resource):

    @jwt_required()
    @ns.doc('get_user')
    @ns.marshal_with(public_user_api_model)  # , skip_none=True
    def get(self, id):
        """
        Returns a user.
        """
        return DAO.get_user(id)

    @ns.doc('update_user')
    @ns.expect(public_user_api_model)
    #@ns.marshal_with(public_user_api_model)
    @ns.response(204, 'User successfully updated.')
    def put(self, id):
        """
        Updates User
        JSON body
        ```
        {
          "name": "User name",
          "username": "User username",
          "password": "User password"
        }
        ```
        """

        data = User.parser.parse_args()
        return DAO.update_user(id, data)

    @ns.doc('delete_user')
    @ns.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Deletes user.
        """
        # delete_user(id)
        return DAO.delete_user(id)

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('username',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('email',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('security_question',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('security_answer',
        type=str,
        required=False,
        help="This field cannot be blank."
    )
    parser.add_argument('terms_and_conditions_checked',
        type=bool,
        required=False,
        help="This field cannot be blank."
    )
