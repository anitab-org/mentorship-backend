from typing import Dict
from http import HTTPStatus
from app import messages
from app.database.models.user import UserModel
from app.utils.decorator_utils import email_verification_required


class AdminDAO:
    """Data Access Object for Admin functionalities."""

    @staticmethod
    @email_verification_required
    def assign_new_user(user_id: int, data: Dict[str, str]):
        """Creates a new admin.

        Creates a new admin if the assigned user exists and is assigned by another user. Otherwise returns a message.

        Args:
            user_id: The user id of the assigner.
            data: A list containing the details of the assigned user.

        Returns:
            message: A message corresponding to the completed action.
        """
        new_admin_user_id = data["user_id"]

        if user_id == new_admin_user_id:
            return messages.USER_CANNOT_BE_ASSIGNED_ADMIN_BY_USER, HTTPStatus.FORBIDDEN

        admin_user = UserModel.find_by_id(user_id)

        if admin_user:
            if not admin_user.is_admin:
                return messages.USER_ASSIGN_NOT_ADMIN, HTTPStatus.FORBIDDEN
        else:
            return messages.USER_NOT_FOUND, HTTPStatus.NOT_FOUND

        new_admin_user = UserModel.find_by_id(new_admin_user_id)

        if new_admin_user:

            if new_admin_user.is_admin:
                return messages.USER_IS_ALREADY_AN_ADMIN, HTTPStatus.BAD_REQUEST

            new_admin_user.is_admin = True
            new_admin_user.save_to_db()

            return messages.USER_IS_NOW_AN_ADMIN, HTTPStatus.OK

        return messages.USER_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

    @staticmethod
    @email_verification_required
    def revoke_admin_user(user_id: int, data: Dict[str, str]):
        """Revokes the admin status of an user.

        Revokes the admin status of an user if the user exists, is an admin and another user requests for this action. Otherwise returns a message.

        Args:
            user_id: The user id of the revoker.
            data: A list containing the details of the user whose admin status is to be revoked.

        Returns:
            message: A message corresponding to the completed action.
        """
        admin_user_id = data["user_id"]

        admin_count = UserModel.query.filter(UserModel.is_admin == True).count()

        if user_id == admin_user_id and admin_count == 1:
            return messages.USER_CANNOT_REVOKE_ADMIN_STATUS, HTTPStatus.FORBIDDEN

        new_admin_user = UserModel.find_by_id(admin_user_id)

        admin_user = UserModel.find_by_id(user_id)

        if admin_user:
            if not admin_user.is_admin:
                return messages.USER_REVOKE_NOT_ADMIN, HTTPStatus.FORBIDDEN
        else:
            return messages.USER_NOT_FOUND, HTTPStatus.NOT_FOUND

        if new_admin_user:

            if not new_admin_user.is_admin:
                return messages.USER_IS_NOT_AN_ADMIN, HTTPStatus.BAD_REQUEST

            new_admin_user.is_admin = False
            new_admin_user.save_to_db()

            return messages.USER_ADMIN_STATUS_WAS_REVOKED, HTTPStatus.OK

        return messages.USER_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND

    @staticmethod
    def list_admins(user_id):
        """Retrieves a list of admin users for the user with specified ID.

        Arguments:
            user_id: The ID of the user querying the fellow admins.

        Returns:
            A list of admin users matching conditions and the HTTP response code.
        """

        users_list = UserModel.query.filter(UserModel.id != user_id).all()
        list_of_users = [user.json() for user in users_list if user.is_admin]

        return list_of_users
