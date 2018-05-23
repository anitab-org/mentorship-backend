from app.database.models.user import UserModel
from app.database import db


class UserDAO:

    FAIL_USER_ALREADY_EXISTS = "FAIL_USER_ALREADY_EXISTS"
    SUCCESS_USER_CREATED = "SUCCESS_USER_CREATED"

    def create_user(self, data):
        name = data['name']
        username = data['username']
        password = data['password']
        email = data['email']
        security_question = data['security_question']
        security_answer = data['security_answer']
        terms_and_conditions_checked = data['terms_and_conditions_checked']

        existing_user = UserModel.find_by_username(data['username'])
        if existing_user:
            return existing_user
        else:
            existing_user = UserModel.find_by_email(data['email'])
            if existing_user:
                return existing_user

        user = UserModel(name, username, password, email,
                         security_question, security_answer,
                         terms_and_conditions_checked)

        user.save_to_db()

        return None

    def delete_user(self, user_id):
        user = UserModel.find_by_id(user_id).one()
        if user:
            user.delete_from_db()
            return {"message": "User was deleted successfully"}, 201

        return {"message": "User does not exist"}, 201

    def get_user(self, user_id):
        return UserModel.find_by_id(user_id), 201

    def list_users(self, is_verified = None):
        users_list = UserModel.query.all()
        list_of_users = []
        if is_verified:
            for user in users_list:
                if not user.is_email_verified:
                    list_of_users += [user.json()]
        else:
            list_of_users = [user.json() for user in users_list]

        return list_of_users, 201

    def update_user(self, user_id, data):
        user = UserModel.find_by_id(user_id)
        if 'name' in data:
            user.name = data['name']

        user.save_to_db()

        return {"message": "User was updated successfully"}, 201

    def change_password(self, user_id, data):
        current_password = data['current_password']
        new_password = data['new_password']

        user = UserModel.find_by_id(user_id)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save_to_db()
            return {"message": "Password was updated successfully."}, 201

        return {"message": "Current password is incorrect."}, 201

    def confirm_registration(self, user_id, data):

        # Not implemented yet
        # set confirmation date
        # set confirmation value

        return {"message": "User was updated successfully"}, 201