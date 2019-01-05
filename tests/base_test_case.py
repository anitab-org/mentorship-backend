from flask_testing import TestCase

from run import application

from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from tests.test_data import TEST_ADMIN_USER


class BaseTestCase(TestCase):
    @classmethod
    def create_app(cls):
        application.config.from_object("config.TestingConfig")

        # Setting up test environment variables
        application.config["SECRET_KEY"] = "TEST_SECRET_KEY"
        application.config["SECURITY_PASSWORD_SALT"] = "TEST_SECURITY_PWD_SALT"
        return application

    def setUp(self):
        DB.create_all()

        self.admin_user = UserModel(
            name=TEST_ADMIN_USER["name"],
            email=TEST_ADMIN_USER["email"],
            username=TEST_ADMIN_USER["username"],
            password=TEST_ADMIN_USER["password"],
            terms_and_conditions_checked=TEST_ADMIN_USER[
                "terms_and_conditions_checked"
            ],
        )
        DB.session.add(self.admin_user)
        DB.session.commit()
        self.admin_user.is_email_verified = True

    @classmethod
    def tearDown(cls):
        DB.session.remove()
        DB.drop_all()
