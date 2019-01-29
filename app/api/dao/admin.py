from app.database.models.user import UserModel
from app import constants

class AdminDAO:

    @staticmethod
    def assign_new_user(assigner_user_id, data):

        new_admin_user_id = data['user_id']

        if assigner_user_id is new_admin_user_id:
            return {"message": USER_CANNOT_ASSIGN_HIMSELF_AS_ADMIN }, 403

        new_admin_user = UserModel.find_by_id(new_admin_user_id)

        if new_admin_user:

            if new_admin_user.is_admin:
                return {"message": USER_IS_ALREADY_AN_ADMIN }, 400

            new_admin_user.is_admin = True
            new_admin_user.save_to_db()

            return {"message": USER_IS_ALREADY_AN_ADMIN }, 200

        return {"message": USER_DOES_NOT_EXIST }, 404

    @staticmethod
    def revoke_admin_user(revoker_user_id, data):

        admin_user_id = data['user_id']

        if revoker_user_id is admin_user_id:
            return {"message": USER_CANNOT_REVOKE_ADMIN_STATUS }, 403

        new_admin_user = UserModel.find_by_id(admin_user_id)

        if new_admin_user:

            if not new_admin_user.is_admin:
                return {"message": USER_IS_NOT_AN_ADMIN }, 400

            new_admin_user.is_admin = False
            new_admin_user.save_to_db()

            return {"message": USER_ADMIN_STATUS_WAS_REVOKED }, 200

        return {"message": USER_DOES_NOT_EXIST }, 404
