from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1, USER2


class MentorshipRelationBaseTestCase(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(MentorshipRelationBaseTestCase, self).setUp()

        self.first_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        self.second_user = UserModel(
            name=USER2["name"],
            email=USER2["email"],
            username=USER2["username"],
            password=USER2["password"],
            terms_and_conditions_checked=USER2["terms_and_conditions_checked"],
        )

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True

        DB.session.add(self.first_user)
        DB.session.add(self.second_user)
        DB.session.commit()
