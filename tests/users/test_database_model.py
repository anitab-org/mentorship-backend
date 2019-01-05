import unittest
from werkzeug.security import check_password_hash

from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from tests.base_test_case import BaseTestCase
from tests.test_data import TEST_ADMIN_USER


# Testing User database model
#
# TODO tests:
#     - User insertion/deletion/update/read
#     - Check if first user is an admin


class TestAdminUserModel(BaseTestCase):
    def test_is_first_user_admin(self):

        user = UserModel.query.filter_by(
            email=TEST_ADMIN_USER["email"]
        ).first()
        self.assertTrue(user is not None)
        self.assertTrue(user.id is not None)
        self.assertTrue(user.name == TEST_ADMIN_USER["name"])
        self.assertTrue(user.username == TEST_ADMIN_USER["username"])
        self.assertTrue(user.email == TEST_ADMIN_USER["email"])
        self.assertFalse(user.password_hash == TEST_ADMIN_USER["password"])
        self.assertTrue(user.is_admin)
        self.assertTrue(
            user.terms_and_conditions_checked
            == TEST_ADMIN_USER["terms_and_conditions_checked"]
        )

    def test_second_user_cannot_be_admin(self):

        user = UserModel(
            name="User1",
            email="user1@email.com",
            username="user_not_admin",
            password="user1_password",
            terms_and_conditions_checked=True,
        )
        DB.session.add(user)
        DB.session.commit()

        user = UserModel.query.filter_by(email="user1@email.com").first()
        self.assertTrue(user is not None)
        self.assertTrue(user.id is not None)
        self.assertTrue(user.name == "User1")
        self.assertTrue(user.username == "user_not_admin")
        self.assertTrue(user.email == "user1@email.com")
        self.assertFalse(user.password_hash == "user1_password")
        self.assertTrue(
            check_password_hash(user.password_hash, "user1_password")
        )
        self.assertFalse(user.is_admin)
        self.assertTrue(user.terms_and_conditions_checked)
        self.assertIsInstance(user.registration_date, float)
        self.assertFalse(user.is_email_verified)


if __name__ == "__main__":
    unittest.main()
