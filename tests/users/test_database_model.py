import unittest
from werkzeug.security import check_password_hash

from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db

from tests.test_data import test_admin_user

# Testing User database model
#
# TODO tests:
#     - User insertion/deletion/update/read
#     - Check if first user is an admin


class TestAdminUserModel(BaseTestCase):
    def test_is_first_user_admin(self):

        user = UserModel.query.filter_by(email=test_admin_user["email"]).first()
        self.assertTrue(user is not None)
        self.assertTrue(user.id is not None)
        self.assertTrue(user.name == test_admin_user["name"])
        self.assertTrue(user.username == test_admin_user["username"])
        self.assertTrue(user.email == test_admin_user["email"])
        self.assertFalse(user.password_hash == test_admin_user["password"])
        self.assertTrue(user.is_admin)
        self.assertTrue(
            user.terms_and_conditions_checked
            == test_admin_user["terms_and_conditions_checked"]
        )

    def test_second_user_cannot_be_admin(self):

        user = UserModel(
            name="User1",
            email="user1@email.com",
            username="user_not_admin",
            password="user1_password",
            terms_and_conditions_checked=True,
        )
        db.session.add(user)
        db.session.commit()

        user = UserModel.query.filter_by(email="user1@email.com").first()
        self.assertTrue(user is not None)
        self.assertTrue(user.id is not None)
        self.assertTrue(user.name == "User1")
        self.assertTrue(user.username == "user_not_admin")
        self.assertTrue(user.email == "user1@email.com")
        self.assertFalse(user.password_hash == "user1_password")
        self.assertTrue(check_password_hash(user.password_hash, "user1_password"))
        self.assertFalse(user.is_admin)
        self.assertTrue(user.terms_and_conditions_checked)
        self.assertIsInstance(user.registration_date, float)
        self.assertFalse(user.is_email_verified)


if __name__ == "__main__":
    unittest.main()
