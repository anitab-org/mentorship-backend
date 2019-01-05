import unittest

from tests.base_test_case import BaseTestCase
from tests.test_data import USER1
from app.database.models.user import UserModel
from app.api.dao.admin import AdminDAO
from app.database.sqlalchemy_extension import DB


class TestAdminDao(BaseTestCase):
    def test_dao_assign_new_admin_valid_user(self):
        dao = AdminDAO()

        user = UserModel(
            name="Joan",
            username="joan2",
            email="joan@email.com",
            password="test_password",
            terms_and_conditions_checked=True,
        )
        DB.session.add(user)
        DB.session.commit()

        user = UserModel.query.filter_by(id=2).first()

        self.assertFalse(user.is_admin)

        data = dict(user_id=2)
        dao.assign_new_user(1, data)

        user = UserModel.query.filter_by(id=2).first()
        self.assertTrue(user.is_admin)

    def test_dao_assign_admin_role_to_myself(self):
        dao = AdminDAO()

        user = UserModel(
            name=USER1["name"],
            username=USER1["username"],
            email=USER1["email"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

        data = dict(user_id=2)

        dao_result = dao.assign_new_user(2, data)

        self.assertEqual(
            ({"message": "You cannot assign yourself as an Admin."}, 403),
            dao_result,
        )

    def test_dao_revoke_admin_role_to_valid_user(self):
        dao = AdminDAO()

        user = UserModel(
            name=USER1["name"],
            username=USER1["username"],
            email=USER1["email"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
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

    def test_dao_revoke_admin_role_to_non_existing_user(self):
        dao = AdminDAO()

        data = dict(user_id=123)

        dao_result = dao.revoke_admin_user(1, data)

        self.assertEqual(
            ({"message": "User does not exist."}, 404), dao_result
        )

    def test_dao_revoke_admin_role_to_non_admin_user(self):
        dao = AdminDAO()

        user = UserModel(
            name=USER1["name"],
            username=USER1["username"],
            email=USER1["email"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()
        self.assertFalse(user.is_admin)

        data = dict(user_id=2)

        dao_result = dao.revoke_admin_user(1, data)

        self.assertEqual(
            ({"message": "User is not an Admin."}, 400), dao_result
        )

    def test_dao_revoke_admin_role_to_myself(self):
        dao = AdminDAO()

        data = dict(user_id=1)

        dao_result = dao.revoke_admin_user(1, data)

        self.assertEqual(
            ({"message": "You cannot revoke your admin status."}, 403),
            dao_result,
        )


if __name__ == "__main__":
    unittest.main()
