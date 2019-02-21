from datetime import datetime
from operator import itemgetter

from app.utils.decorator_utils import email_verification_required
from app.api.email_utils import confirm_token
from app.database.models.user import UserModel
from app.utils.enum_utils import MentorshipRelationState
from app.utils.validation_utils import is_email_valid


class UserDAO:
    FAIL_USER_ALREADY_EXISTS = "FAIL_USER_ALREADY_EXISTS"
    SUCCESS_USER_CREATED = "SUCCESS_USER_CREATED"
    MIN_NUMBER_OF_ADMINS = 1

    @staticmethod
    def create_user(data):
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
        return UserModel.find_by_id(user_id)

    @staticmethod
    def get_user_by_email(email):
        return UserModel.find_by_email(email)

    @staticmethod
    def get_user_by_username(username):
        return UserModel.find_by_username(username)

    @staticmethod
    def list_users(user_id, is_verified=None):
        users_list = UserModel.query.filter(UserModel.id != user_id).all()
        list_of_users = []
        if is_verified:
            for user in users_list:
                if user.is_email_verified:
                    list_of_users += [user.json()]
        else:
            list_of_users = [user.json() for user in users_list]

        return list_of_users, 200

    @staticmethod
    @email_verification_required
    def update_user_profile(user_id, data):

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
        """
        The user can login with two options:
        -> username + password
        -> email + password
        """

        if is_email_valid(username_or_email):
            user = UserModel.find_by_email(username_or_email)
        else:
            user = UserModel.find_by_username(username_or_email)

        if user and user.check_password(password):
            return user

        return None

    @staticmethod
    def get_achievements(user_id):
        """Shows a subset of the user's achievements

        Gets all the completed tasks of the user and
        return them in a list. Achievements are completed tasks

        Args:
            user_id: The ID of the user for whom tasks are
                requested.

        Returns:
            achievements: A list containing the user's achievements
        """
        user = UserModel.find_by_id(user_id)
        all_relations = user.mentor_relations + user.mentee_relations
        tasks = []
        for relation in all_relations:
            tasks += relation.tasks_list.tasks
        achievements = [task for task in tasks if task.get("is_done")]
        return achievements

    @staticmethod
    def get_user_statistics(user_id):
        """Shows some basic user statistics

        Gets the following statistics of the user:
        -> Pending Requests
        -> Accepted Requests
        -> Rejected Requests
        -> Completed Relations
        -> Cancelled Relations
        -> Up to 3 recent achievements

        Args:
            user_id: The id of the user for whom stats are requested

        Returns:
            A dict containing the stats (if the user ID is valid)
            If user ID is invalid, returns None
        """
        user = UserModel.find_by_id(user_id)

        if not user:
            return None

        all_relations = user.mentor_relations + user.mentee_relations
        (pending_requests, accepted_requests, rejected_requests, completed_relations, cancelled_relations) = (
            0, 0, 0, 0, 0)
        for relation in all_relations:
            if relation.state == MentorshipRelationState.PENDING:
                pending_requests += 1
            elif relation.state == MentorshipRelationState.ACCEPTED:
                accepted_requests += 1
            elif relation.state == MentorshipRelationState.REJECTED:
                rejected_requests += 1
            elif relation.state == MentorshipRelationState.COMPLETED:
                completed_relations += 1
            elif relation.state == MentorshipRelationState.CANCELLED:
                cancelled_relations += 1

        achievements = UserDAO.get_achievements(user_id)
        if achievements:
            # We only need the first three of these achievements
            achievements = achievements[0:3]
            sorted(achievements, key=itemgetter("created_at"))

        response = {
            'name': user.name,
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests,
            'rejected_requests': rejected_requests,
            'completed_relations': completed_relations,
            'cancelled_relations': cancelled_relations,
            'achievements': achievements
        }
        return response
