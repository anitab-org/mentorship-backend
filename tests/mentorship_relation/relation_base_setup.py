from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from tests.base_test_case import BaseTestCase
from tests.test_data import *


class MentorshipRelationBaseTestCase(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(MentorshipRelationBaseTestCase, self).setUp()

        self.first_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        self.second_user = UserModel(
            name=user2["name"],
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )
        self.third_user = UserModel(
            name=user3["name"],
            email=user3["email"],
            username=user3["username"],
            password=user3["password"],
            terms_and_conditions_checked=user3["terms_and_conditions_checked"],
        )

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.first_user.is_email_verified = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True
        self.second_user.is_email_verified = True
        self.third_user.need_mentoring = True
        self.third_user.available_to_mentor = True
        self.third_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.add(self.third_user)
        db.session.commit()
