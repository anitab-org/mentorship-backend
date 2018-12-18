from datetime import datetime

from app.api.email_utils import confirm_token
from app.database.models.user import UserModel
from app.utils.validation_utils import is_email_valid


class UserDAO:
    """ Class definition for UserDAO.
    
    Provides various functions pertaining to user.

    Attributes:
        FAIL_USER_ALREADY_EXISTS
        SUCCESS_USER_CREATED
        MIN_NUMBER_OF_ADMINS

    Functions:
        create_user()
        delete_user()
        get_user()
        get_user_by_email()
        get_user_by_username()
        list_users()
        update_user_profile()
        change_password()
        confirm_registration()
        authenticate()
    """ 
    FAIL_USER_ALREADY_EXISTS = "FAIL_USER_ALREADY_EXISTS"
    SUCCESS_USER_CREATED = "SUCCESS_USER_CREATED"
    MIN_NUMBER_OF_ADMINS = 1

    @staticmethod
    def create_user(data):
        """Creates a user.

        Creates a new user if the current username is not taken. Otherwise returns a message.

        Args:
            data: A list containing the name, username, password, email and terms_and_conditions_checked.

        Returns:
            message: A message corresponding to the completed action; success or failure.
        """   
        name = data['name']
        username = data['username']
        password = data['password']
        email = data['email']
        terms_and_conditions_checked = data['terms_and_conditions_checked']

        existing_user = UserModel.find_by_username(data['username'])
        if existing_user:
            return {"message": "A user with that username already exists"}, 400
        else:
            existing_user = UserModel.find_by_email(data['email'])
            if existing_user:
                return {"message": "A user with that email already exists"}, 400

        user = UserModel(name, username, password, email, terms_and_conditions_checked)
        if 'need_mentoring' in data:
            user.need_mentoring = data['need_mentoring']

        if 'available_to_mentor' in data:
            user.available_to_mentor = data['available_to_mentor']

        user.save_to_db()

        return {"message": "User was created successfully. "
                           "A confirmation email has been sent via email. "
                           "After confirming your email you can login."}, 200

    @staticmethod
    def delete_user(user_id):
        """Deletes a user.

        Deletes a user provided the latter exists and deleting them will not cause the number of admins to go below the minimum threshold.

        Args:
            user_id : The user id of the user being deleted.

        Returns:
            message: A message containg a description of the action performed.
        """

        user = UserModel.find_by_id(user_id)

        # check if this user is the only admin
        if user.is_admin:

            admins_list_count = len(UserModel.get_all_admins())
            if admins_list_count <= UserDAO.MIN_NUMBER_OF_ADMINS:
                return {"message": "You cannot delete your account, since you are the only Admin left."}, 400

        if user:
            user.delete_from_db()
            return {"message": "User was deleted successfully"}, 200

        return {"message": "User does not exist"}, 404

    @staticmethod
    def get_user(user_id):
        """Finds a user.

        Returns a user which has been searched by their id.

        Args:
            user_id : The user id of the required user.

        Returns:
            user: The corresponding user.
        """

        return UserModel.find_by_id(user_id)

    @staticmethod
    def get_user_by_email(email):
        """Finds a user by email.

        Returns a user which has been searched by their email.

        Args:
            email : The email of the required user.

        Returns:
            user: The corresponding user.
        """

        return UserModel.find_by_email(email)

    @staticmethod
    def get_user_by_username(username):
        """Finds a user by username.

        Returns a user which has been searched by their username.

        Args:
            username : The username of the required user.

        Returns:
            user: The corresponding user.
        """

        return UserModel.find_by_username(username)

    @staticmethod
    def list_users(user_id, is_verified=None):
        """Lists users.

        Returns a list of users which has been searched by their user_id.

        Args:
            list_of_users : List of user ids.
            is_verified: whether or not the results should contain only verified users.

        Returns:
            users_list: A list of users matching the given criteria.
        """

        users_list = UserModel.query.filter(UserModel.id!=user_id).all()
        list_of_users = []
        if is_verified:
            for user in users_list:
                if user.is_email_verified:
                    list_of_users += [user.json()]
        else:
            list_of_users = [user.json() for user in users_list]

        return list_of_users, 200

    @staticmethod
    def update_user_profile(user_id, data):
        """Updates a user's profile.

        Updates the information pertaining to a given user and saves it to the database.

        Args:
            user_id : user_id of the user whose details are to be updated.
            data: List containing the fields to be updated and their corresponding values.

        Returns:
            message: A message corresponding to the performed action.
        """

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User does not exist"}, 404

        username = data.get('username', None)
        if username:
            user_with_same_username = UserModel.find_by_username(username)

            # username should be unique
            if user_with_same_username:
                return {"message": "That username is already taken by another user."}, 400

            user.username = username

        if 'name' in data and data['name']:
            user.name = data['name']

        if 'bio' in data and data['bio']:
            user.bio = data['bio']

        if 'location' in data and data['location']:
            user.location = data['location']

        if 'occupation' in data and data['occupation']:
            user.occupation = data['occupation']

        if 'organization' in data and data['organization']:
            user.organization = data['organization']

        if 'slack_username' in data and data['slack_username']:
            user.slack_username = data['slack_username']

        if 'social_media_links' in data and data['social_media_links']:
            user.social_media_links = data['social_media_links']

        if 'skills' in data and data['skills']:
            user.skills = data['skills']

        if 'interests' in data and data['interests']:
            user.interests = data['interests']

        if 'resume_url' in data and data['resume_url']:
            user.resume_url = data['resume_url']

        if 'photo_url' in data and data['photo_url']:
            user.photo_url = data['photo_url']

        if 'need_mentoring' in data:
            user.need_mentoring = data['need_mentoring']

        if 'available_to_mentor' in data:
            user.available_to_mentor = data['available_to_mentor']

        user.save_to_db()

        return {"message": "User was updated successfully"}, 200

    @staticmethod
    def change_password(user_id, data):
        """Change the password of a user.

        Changes the password of a given user and saves it to the database.

        Args:
            user_id : user_id of the user whose details are to be updated.
            data: List containing the current and new password and their corresponding values.

        Returns:
            message: A message corresponding to the performed action.
        """

        current_password = data['current_password']
        new_password = data['new_password']

        user = UserModel.find_by_id(user_id)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save_to_db()
            return {"message": "Password was updated successfully."}, 201

        return {"message": "Current password is incorrect."}, 400

    @staticmethod
    def confirm_registration(token):
        """Confirms a newly registered user.

        Sets the is_email_verified of a user to True if it is not already the case and saves to the database.

        Args:
            token : Token which has been emailed.

        Returns:
            message: A message corresponding to the performed action.
        """

        email_from_token = confirm_token(token)

        if email_from_token is False or email_from_token is None:
            return {'message': 'The confirmation link is invalid or the token has expired.'}, 400

        user = UserModel.find_by_email(email_from_token)
        if user.is_email_verified:
            return {'message': 'Account already confirmed.'}, 200
        else:
            user.is_email_verified = True
            user.email_verification_date = datetime.now()
            user.save_to_db()
            return {'message': 'You have confirmed your account. Thanks!'}, 200

    @staticmethod
    def authenticate(username_or_email, password):
        """Authenticates a user.

        Authenticates a user given the latter has a valid email and provides the appropriate password.
        The user can login with two options:
            -> username + password
            -> email + password

        Args:
            username_or_email : username or email of the user being authenticated.
            password: List containing the current and new password and their corresponding values.
        """

        if is_email_valid(username_or_email):
            user = UserModel.find_by_email(username_or_email)
        else:
            user = UserModel.find_by_username(username_or_email)

        if user and user.check_password(password):
            return user

        return None
