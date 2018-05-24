from app.database.models.user import UserModel


class AdminDAO:

    def assign_new_user(self, new_admin_id):

        new_admin_user = UserModel.find_by_id(new_admin_id)

        if new_admin_user:

            if new_admin_user.is_admin:
                return {"message": "User is already an Admin"}, 201

            new_admin_user.is_admin = True
            new_admin_user.save_to_db()

            return {"message": "User is now an Admin"}, 201

        return {"message": "User does not exist"}, 401
