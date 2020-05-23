import unittest

from tests.base_test_case import BaseTestCase
from tests.test_data import user1

from app import messages
from app.database.models.user import UserModel
from app.api.dao.admin import AdminDAO
from app.database.sqlalchemy_extension import db


class TestAdminDao(BaseTestCase):

    """
    Checks whether a new admin can be assigned by existing admin.
    """

    def test_dao_assign_new_admin_valid_user(self):

        dao = AdminDAO()

        user = UserModel(
            name="Joan",
            username="joan2",
            email="joan@email.com",
            password="test_password",
            terms_and_conditions_checked=True,
        )
        db.session.add(user)
        db.session.commit()

        user = UserModel.query.filter_by(id=2).first()

        self.assertFalse(user.is_admin)

        data = dict(user_id=2)
        dao.assign_new_user(1, data)

        user = UserModel.query.filter_by(id=2).first()
        self.assertTrue(user.is_admin)

    """
    Checks whether a new admin can be assigned by normal user.
    """

    def test_dao_assign_new_admin_by_normal_user(self):

        dao = AdminDAO()

        user = UserModel(
            name=user1["name"],
            username=user1["username"],
            email=user1["email"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        user.is_email_verified = True
        user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()

        self.assertFalse(user.is_admin)

        data = dict(user_id=1)
        dao_result = dao.assign_new_user(2, data)

        self.assertEqual((messages.USER_ASSIGN_NOT_ADMIN, 403), dao_result)

    """
    Checks whether a user tries to assign admin rights to a non existing user.
    """

    def test_dao_assign_admin_role_to_non_existing_user(self):

        dao = AdminDAO()

        data = dict(user_id=123)

        dao_result = dao.assign_new_user(1, data)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, 404), dao_result)

    """
    Checks whether a user tries to assign admin rights to existing admin user.
    """

    def test_dao_assign_admin_role_to_admin_user(self):

        dao = AdminDAO()

        user = UserModel(
            name=user1["name"],
            username=user1["username"],
            email=user1["email"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )

        user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)
        user.is_admin = True
        user.save_to_db()
        self.assertTrue(user.is_admin)

        data = dict(user_id=2)

        dao_result = dao.assign_new_user(1, data)

        self.assertEqual((messages.USER_IS_ALREADY_AN_ADMIN, 400), dao_result)

    """
    Checks if a user tries to self-assign admin role.  
    """

    def test_dao_assign_admin_role_to_myself(self):

        dao = AdminDAO()

        user = UserModel(
            name=user1["name"],
            username=user1["username"],
            email=user1["email"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        user.is_email_verified = True
        user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

        data = dict(user_id=2)

        dao_result = dao.assign_new_user(2, data)

        self.assertEqual(
            (messages.USER_CANNOT_BE_ASSIGNED_ADMIN_BY_USER, 403), dao_result
        )

    """
    Checks whether a user is trying to revoke other user's admin priviledges. 
    """

    def test_dao_revoke_admin_role_to_valid_user(self):

        dao = AdminDAO()

        user = UserModel(
            name=user1["name"],
            username=user1["username"],
            email=user1["email"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)
        user.is_admin = True
        user.save_to_db()
        self.assertTrue(user.is_admin)

        data = dict(user_id=2)
        dao.revoke_admin_user(1, data)

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

    """
    Checks whether a user is trying to revoke other user's admin privileges. 
    """

    def test_dao_revoke_admin_role_by_non_admin_user(self):

        dao = AdminDAO()

        user = UserModel(
            name=user1["name"],
            username=user1["username"],
            email=user1["email"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        user.is_email_verified = True
        user.save_to_db()
        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

        data = dict(user_id=1)
        dao_result = dao.revoke_admin_user(2, data)

        self.assertEqual((messages.USER_REVOKE_NOT_ADMIN, 403), dao_result)

    """
    Checks whether a user tries to revoke admin rights from a non existing user.
    """

    def test_dao_revoke_admin_role_to_non_existing_user(self):

        dao = AdminDAO()

        data = dict(user_id=123)

        dao_result = dao.revoke_admin_user(1, data)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, 404), dao_result)

    """
    Checks whether a user tries to revoke admin rights of a non admin user.
    """

    def test_dao_revoke_admin_role_to_non_admin_user(self):

        dao = AdminDAO()

        user = UserModel(
            name=user1["name"],
            username=user1["username"],
            email=user1["email"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        user.save_to_db()
        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

        data = dict(user_id=2)

        dao_result = dao.revoke_admin_user(1, data)

        self.assertEqual((messages.USER_IS_NOT_AN_ADMIN, 400), dao_result)

    """
    Checks whether a user tries to revoke their own admin status.
    """

    def test_dao_revoke_admin_role_to_myself(self):
        dao = AdminDAO()

        data = dict(user_id=1)

        dao_result = dao.revoke_admin_user(1, data)

        self.assertEqual((messages.USER_CANNOT_REVOKE_ADMIN_STATUS, 403), dao_result)


if __name__ == "__main__":
    unittest.main()
