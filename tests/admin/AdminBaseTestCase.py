from app.api.dao.admin import AdminDAO
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import user1


class AdminBaseTestCase(BaseTestCase):

    def setUp(self):
        super(AdminBaseTestCase, self).setUp()
        self.dao = AdminDAO()

        self.user = UserModel(
            name=user1['name'],
            username=user1['username'],
            email=user1['email'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.user.is_email_verified = True
        self.user.save_to_db()

        user = UserModel.query.filter_by(id=2).first()

        self.assertFalse(user.is_admin)
