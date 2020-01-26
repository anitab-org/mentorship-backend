import unittest

from app import messages
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.admin.AdminBaseTestCase import AdminBaseTestCase


class TestAdminDao(AdminBaseTestCase):

    def set_up(self):
        super(TestAdminDao, self).setUp()

    """
    Checks whether a new admin can be assigned by existing admin.
    """

    def test_dao_assign_new_admin_valid_user(self):
        user = UserModel(
            name='Joan',
            username='joan2',
            email='joan@email.com',
            password='test_password',
            terms_and_conditions_checked=True
        )
        db.session.add(user)
        db.session.commit()

        user = UserModel.query.filter_by(id=2).first()

        self.assertFalse(user.is_admin)

        data = dict(user_id=2)
        self.dao.assign_new_user(1, data)

        user = UserModel.query.filter_by(id=2).first()
        self.assertTrue(user.is_admin)

    """
    Checks whether a new admin can be assigned by normal user.
    """

    def test_dao_assign_new_admin_by_normal_user(self):
        data = dict(user_id=1)
        dao_result = self.dao.assign_new_user(2, data)

        self.assertEqual((messages.USER_ASSIGN_NOT_ADMIN, 403), dao_result)

    """
    Checks whether a user tries to assign admin rights to a non existing user.
    """

    def test_dao_assign_admin_role_to_non_existing_user(self):
        data = dict(user_id=123)

        dao_result = self.dao.assign_new_user(1, data)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, 404), dao_result)

    """
    Checks whether a user tries to assign admin rights to existing admin user.
    """

    def test_dao_assign_admin_role_to_admin_user(self):
        self.user.is_admin = True
        self.user.save_to_db()
        self.assertTrue(self.user.is_admin)

        data = dict(user_id=2)

        dao_result = self.dao.assign_new_user(1, data)

        self.assertEqual((messages.USER_IS_ALREADY_AN_ADMIN, 400), dao_result)

    """
    Checks if a user tries to self-assign admin role.  
    """

    def test_dao_assign_admin_role_to_myself(self):
        data = dict(user_id=2)
        dao_result = self.dao.assign_new_user(2, data)

        self.assertEqual((messages.USER_CANNOT_BE_ASSIGNED_ADMIN_BY_USER, 403),
                         dao_result)

    """
    Checks whether a user is trying to revoke other user's admin privileges. 
    """

    def test_dao_revoke_admin_role_to_valid_user(self):
        self.user.is_admin = True
        self.user.save_to_db()
        self.assertTrue(self.user.is_admin)

        data = dict(user_id=2)
        self.dao.revoke_admin_user(1, data)

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

    """
    Checks whether a user is trying to revoke other user's admin privileges. 
    """

    def test_dao_revoke_admin_role_by_non_admin_user(self):
        data = dict(user_id=1)
        dao_result = self.dao.revoke_admin_user(2, data)

        self.assertEqual((messages.USER_REVOKE_NOT_ADMIN, 403), dao_result)

    """
    Checks whether a user tries to revoke admin rights from a non existing user.
    """

    def test_dao_revoke_admin_role_to_non_existing_user(self):
        data = dict(user_id=123)

        dao_result = self.dao.revoke_admin_user(1, data)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, 404), dao_result)

    """
    Checks whether a user tries to revoke admin rights of a non admin user.
    """

    def test_dao_revoke_admin_role_to_non_admin_user(self):
        data = dict(user_id=2)

        dao_result = self.dao.revoke_admin_user(1, data)

        self.assertEqual((messages.USER_IS_NOT_AN_ADMIN, 400), dao_result)

    """
    Checks whether a user tries to revoke their own admin status.
    """

    def test_dao_revoke_admin_role_to_myself(self):
        data = dict(user_id=1)

        dao_result = self.dao.revoke_admin_user(1, data)

        self.assertEqual((messages.USER_CANNOT_REVOKE_ADMIN_STATUS, 403),
                         dao_result)


if __name__ == '__main__':
    unittest.main()
