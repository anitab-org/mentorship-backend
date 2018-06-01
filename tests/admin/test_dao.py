import unittest

from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.api.dao.admin import AdminDAO
from run import db


class TestAdminDao(BaseTestCase):

    def test_dao_assign_new_admin_valid_user(self):
        dao = AdminDAO()

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

        data = dict(
            user_id='2'
        )
        dao.assign_new_user(data)

        user = UserModel.query.filter_by(id=2).first()
        self.assertTrue(user.is_admin)


if __name__ == '__main__':
    unittest.main()
