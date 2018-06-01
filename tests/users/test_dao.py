import unittest
import datetime
from werkzeug.security import check_password_hash

from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.api.dao.user import UserDAO


class TestUserDao(BaseTestCase):

    def test_dao_create_user(self):
        dao = UserDAO()
        data = dict(
            name='User2',
            username='user2',
            email='user2@email.com',
            password='test_password',
            terms_and_conditions_checked=True
        )
        dao.create_user(data)

        # Verify that user was inserted in database through DAO
        user = UserModel.query.filter_by(email='user2@email.com').first()
        self.assertTrue(user is not None)
        self.assertTrue(user.id is not None)
        self.assertTrue(user.name == 'User2')
        self.assertTrue(user.username == 'user2')
        self.assertTrue(user.email == 'user2@email.com')
        self.assertFalse(user.is_admin)
        self.assertFalse(user.password_hash == 'test_password')
        self.assertTrue(check_password_hash(user.password_hash, 'test_password'))
        self.assertTrue(user.terms_and_conditions_checked)
        self.assertIsInstance(user.registration_date, datetime.datetime)
        self.assertFalse(user.is_email_verified)


if __name__ == '__main__':
    unittest.main()
