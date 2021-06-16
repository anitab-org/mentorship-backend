import unittest
from http import HTTPStatus

from app import messages
from app.api.dao.user import UserDAO
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase


class TestUpdateUserDao(BaseTestCase):
    def test_dao_update_user(self):

        self.assertIsNone(self.admin_user.occupation)
        self.assertIsNone(self.admin_user.organization)

        data = dict(occupation="good_developer", organization="good_org")
        UserDAO.update_user_profile(self.admin_user.id, data)

        self.assertEqual("good_developer", self.admin_user.occupation)
        self.assertEqual("good_org", self.admin_user.organization)

    def test_update_fields_with_empty_data(self):

        self.assertIsNone(self.admin_user.occupation)
        self.assertIsNone(self.admin_user.organization)

        data = dict(occupation="good_developer", organization="good_org")
        UserDAO.update_user_profile(self.admin_user.id, data)

        self.assertEqual("good_developer", self.admin_user.occupation)
        self.assertEqual("good_org", self.admin_user.organization)

        data = dict(occupation="", organization="")
        UserDAO.update_user_profile(self.admin_user.id, data)

        self.assertIsNone(self.admin_user.occupation)
        self.assertIsNone(self.admin_user.organization)

    def test_update_user_that_does_not_exist(self):

        user = UserModel.query.filter_by(id=2).first()
        self.assertIsNone(user)

        data = dict(occupation="good_developer", organization="good_org")
        dao_result = UserDAO.update_user_profile(user, data)

        self.assertEqual(
            (messages.USER_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND), dao_result
        )


if __name__ == "__main__":
    unittest.main()
