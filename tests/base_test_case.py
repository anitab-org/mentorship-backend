from flask_testing import TestCase

from app.database.models.user import UserModel
from run import application, db

from tests.utils import test_admin_user


class BaseTestCase(TestCase):

    @classmethod
    def create_app(cls):
        application.config.from_object('config.TestingConfig')
        return application

    @classmethod
    def setUp(cls):
        db.create_all()

        user = UserModel(
            name=test_admin_user['name'],
            email=test_admin_user['email'],
            username=test_admin_user['username'],
            password=test_admin_user['password'],
            terms_and_conditions_checked=test_admin_user['terms_and_conditions_checked']
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
