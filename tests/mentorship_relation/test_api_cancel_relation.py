import json
import unittest
from datetime import datetime, timedelta

from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2
from tests.test_utils import get_test_request_header


class TestCancelMentorshipRelationApi(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestCancelMentorshipRelationApi, self).setUp()

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.second_user = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True

        self.notes_example = 'description of a good mentorship relation'

        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

        # create new mentorship relation

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test__mentor_cancel_mentorship_relation(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.first_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.CANCELLED, self.mentorship_relation.state)
            self.assertEqual({'message': 'Mentorship relation was cancelled successfully.'},
                             json.loads(response.data))

    def test__mentee_cancel_mentorship_relation(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.CANCELLED, self.mentorship_relation.state)
            self.assertEqual({'message': 'Mentorship relation was cancelled successfully.'},
                             json.loads(response.data))


if __name__ == "__main__":
    unittest.main()