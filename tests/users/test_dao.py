import unittest
import datetime
from werkzeug.security import check_password_hash

from app.api.email_utils import generate_confirmation_token
from app.api.dao.user import UserDAO
from app.database.sqlalchemy_extension import db
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import user2


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

    def test_dao_confirm_registration_good_token(self):
        dao = UserDAO()

        user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )
        db.session.add(user)
        db.session.commit()

        # Verify that user was inserted in database through DAO
        user = UserModel.query.filter_by(email=user2['email']).first()
        self.assertIsNotNone(user)

        good_token = generate_confirmation_token(user2['email'])

        self.assertFalse(user.is_email_verified)

        actual_result = dao.confirm_registration(good_token)

        self.assertTrue(user.is_email_verified)
        self.assertIsNotNone(user.email_verification_date)
        self.assertEqual(({'message': 'You have confirmed your account. Thanks!'}, 200),
                         actual_result)

    def test_dao_confirm_registration_bad_token(self):
        dao = UserDAO()

        user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )
        db.session.add(user)
        db.session.commit()

        # Verify that user was inserted in database through DAO
        user = UserModel.query.filter_by(email=user2['email']).first()
        self.assertIsNotNone(user)

        # bad token because it is incomplete
        bad_token = generate_confirmation_token(user2['email'])[:4]

        self.assertFalse(user.is_email_verified)

        actual_result = dao.confirm_registration(bad_token)

        self.assertFalse(user.is_email_verified)
        self.assertIsNone(user.email_verification_date)
        self.assertEqual(({'message': 'The confirmation link is invalid or the token has expired.'}, 400),
                         actual_result)

    def test_dao_confirm_registration_of_already_verified_user(self):
        dao = UserDAO()

        user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )
        db.session.add(user)
        db.session.commit()

        # Verify that user was inserted in database through DAO
        user = UserModel.query.filter_by(email=user2['email']).first()
        self.assertIsNotNone(user)
        user.is_email_verified = True
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.is_email_verified)
        good_token = generate_confirmation_token(user2['email'])
        actual_result = dao.confirm_registration(good_token)

        self.assertTrue(user.is_email_verified)
        self.assertEqual(({'message': 'Account already confirmed.'}, 200),
                         actual_result)

    def test_dao_delete_only_user_admin(self):
        dao = UserDAO()

        before_delete_user = UserModel.query.filter_by(id=1).first()
        self.assertIsNotNone(before_delete_user)
        self.assertTrue(before_delete_user.is_admin)

        dao_result = dao.delete_user(1)

        # Verify that user was inserted in database through DAO
        after_delete_user = UserModel.query.filter_by(id=1).first()
        self.assertTrue(after_delete_user.is_admin)
        self.assertIsNotNone(after_delete_user)
        self.assertEqual(1, after_delete_user.id)
        self.assertEqual(({"message": "You cannot delete your account, since you are the only Admin left."}, 400),
                         dao_result)


if __name__ == '__main__':
    unittest.main()
