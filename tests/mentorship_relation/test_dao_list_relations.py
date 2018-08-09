import unittest
from datetime import datetime, timedelta

from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2


class TestListMentorshipRelationsDAO(BaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super(TestListMentorshipRelationsDAO, self).setUp()

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
        self.past_end_date_example = self.now_datetime - timedelta(weeks=5)
        self.future_end_date_example = self.now_datetime + timedelta(weeks=5)

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

        # create new mentorship relation

        self.past_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.past_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example
        )

        self.future_pending_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example
        )

        self.future_accepted_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example
        )

        db.session.add(self.past_mentorship_relation)
        db.session.add(self.future_pending_mentorship_relation)
        db.session.add(self.future_accepted_mentorship_relation)
        db.session.commit()

    def test_dao_list_past_mentorship_relations(self):

        result = MentorshipRelationDAO.list_past_mentorship_relations(user_id=self.first_user.id)

        expected_response = [self.past_mentorship_relation]

        self.assertIsNotNone(result[0])
        self.assertEqual(expected_response, result[0])

    def test_dao_list_current_mentorship_relation(self):

        result = MentorshipRelationDAO.list_current_mentorship_relation(user_id=self.first_user.id)
        expected_response = self.future_accepted_mentorship_relation

        self.assertEqual(expected_response, result)

    def test_dao_list_non_existing_current_mentorship_relation(self):
        result = MentorshipRelationDAO.list_current_mentorship_relation(user_id=self.admin_user.id)
        expected_response = ({'message': 'You are not in a current mentorship relation.'}, 200)

        self.assertEqual(expected_response, result)

    def test_dao_list_pending_mentorship_relation(self):

        result = MentorshipRelationDAO.list_pending_mentorship_relations(user_id=self.first_user.id)
        expected_response = [self.future_pending_mentorship_relation]

        self.assertEqual(expected_response, result[0])
        self.assertEqual(200, result[1])


if __name__ == '__main__':
    unittest.main()
