from app.database.models.user import UserModel


class AdminDAO:
    """Data Access Object for Admin functionalities."""

    @staticmethod
    def assign_new_user(assigner_user_id, data):
        """Creates a new admin.

        Creates a new admin if the assigned user exists and is assigned
        by another user. Otherwise returns a message.

        Args:
            assigner_user_id: The user id of the assigner.
            data: A list containing the details of the assigned user.

        Returns:
            message: A message corresponding to the completed action.
        """

        new_admin_user_id = data["user_id"]

        if assigner_user_id is new_admin_user_id:
            return {"message": "You cannot assign yourself as an Admin."}, 403

        new_admin_user = UserModel.find_by_id(new_admin_user_id)

        if new_admin_user:

            if new_admin_user.is_admin:
                return {"message": "User is already an Admin."}, 400

            new_admin_user.is_admin = True
            new_admin_user.save_to_db()

            return {"message": "User is now an Admin."}, 200

        return {"message": "User does not exist."}, 404

    @staticmethod
    def revoke_admin_user(revoker_user_id, data):
        """Revokes the admin status of an user.

        Revokes the admin status of an user if the user exists, is an
        admin and another user requests for this action. Otherwise,
        returns a message.

        Args:
            revoker_user_id: The user id of the revoker.
            data: A list containing the details of the user whose admin
                 status is to be revoked.

        Returns:
            message: A message corresponding to the completed action.
        """
        admin_user_id = data["user_id"]

        if revoker_user_id is admin_user_id:
            return {"message": "You cannot revoke your admin status."}, 403

        new_admin_user = UserModel.find_by_id(admin_user_id)

        if new_admin_user:

            if not new_admin_user.is_admin:
                return {"message": "User is not an Admin."}, 400

            new_admin_user.is_admin = False
            new_admin_user.save_to_db()

            return {"message": "User admin status was revoked."}, 200

        return {"message": "User does not exist."}, 404
