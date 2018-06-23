import unittest
from datetime import datetime, timedelta

from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from tests.test_data import user1, user2
from run import db

# TODO test combination of parameters while listing relations

class TestMentorshipRelationListingDAO(BaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super(TestMentorshipRelationListingDAO, self).setUp()

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
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test_dao_list_mentorship_relation_accepted(self):

        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, accepted=True)

        self.assertEqual(({'message': 'Not implemented.'}, 200), result)

    def test_dao_list_mentorship_relation_cancelled(self):

        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, cancelled=True)

        self.assertEqual(({'message': 'Not implemented.'}, 200), result)

    def test_dao_list_mentorship_relation_rejected(self):

        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, rejected=True)

        self.assertEqual(({'message': 'Not implemented.'}, 200), result)

    def test_dao_list_mentorship_relation_completed(self):

        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, completed=True)

        self.assertEqual(({'message': 'Not implemented.'}, 200), result)

    def test_dao_list_mentorship_relation_pending(self):

        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.PENDING
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, pending=True)

        self.assertEqual(({'message': 'Not implemented.'}, 200), result)

    def test_dao_list_mentorship_relation_all(self):

        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.PENDING
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id)
        expected_response = [self.mentorship_relation]

        self.assertIsNotNone(result)
        self.assertEqual(expected_response, result)


if __name__ == '__main__':
    unittest.main()