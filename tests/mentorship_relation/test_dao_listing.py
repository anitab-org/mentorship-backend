import unittest
from datetime import datetime, timedelta

from app import messages
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from app.database.sqlalchemy_extension import db


# TODO test combination of parameters while listing relations

class TestMentorshipRelationListingDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super(TestMentorshipRelationListingDAO, self).setUp()

        self.notes_example = 'description of a good mentorship relation'
        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.mentorship_relation_pending = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )
        self.mentorship_relation_accepted = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )
        self.mentorship_relation_cancelled = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.CANCELLED,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )
        self.mentorship_relation_rejected = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )
        self.mentorship_relation_completed = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

        db.session.add(self.mentorship_relation_pending)
        db.session.add(self.mentorship_relation_accepted)
        db.session.add(self.mentorship_relation_cancelled)
        db.session.add(self.mentorship_relation_rejected)
        db.session.add(self.mentorship_relation_completed)
        db.session.commit()

    def test_dao_list_mentorship_relation_accepted(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_accepted)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, stateList=['ACCEPTED'])

        self.assertEqual(([self.mentorship_relation_accepted], 200), result)

    def test_dao_list_mentorship_relation_cancelled(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_cancelled)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, stateList=['CANCELLED'])

        self.assertEqual(([self.mentorship_relation_cancelled], 200), result)

    def test_dao_list_mentorship_relation_rejected(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_rejected)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, stateList=['REJECTED'])

        self.assertEqual(([self.mentorship_relation_rejected], 200), result)

    def test_dao_list_mentorship_relation_completed(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_completed)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, stateList=['COMPLETED'])

        self.assertEqual(([self.mentorship_relation_completed], 200), result)

    def test_dao_list_mentorship_relation_pending(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_pending)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, stateList=['PENDING'])

        self.assertEqual(([self.mentorship_relation_pending], 200), result)

    def test_dao_list_mentorship_relation_all(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_pending)
        db.session.add(self.mentorship_relation_accepted)
        db.session.add(self.mentorship_relation_cancelled)
        db.session.add(self.mentorship_relation_rejected)
        db.session.add(self.mentorship_relation_completed)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id)
        expected_response = [self.mentorship_relation_pending, self.mentorship_relation_accepted,
                             self.mentorship_relation_cancelled, self.mentorship_relation_rejected, self.mentorship_relation_completed], 200

        self.assertIsNotNone(result)
        self.assertEqual(expected_response, result)

    def test_dao_list_mentorship_relation_pending_and_accepted(self):
        DAO = MentorshipRelationDAO()

        db.session.add(self.mentorship_relation_pending)
        db.session.add(self.mentorship_relation_accepted)
        db.session.commit()

        result = DAO.list_mentorship_relations(user_id=self.first_user.id, stateList=['PENDING', 'ACCEPTED'])
        expected_response = [self.mentorship_relation_pending, self.mentorship_relation_accepted], 200

        self.assertIsNotNone(result)
        self.assertEqual(expected_response, result)

if __name__ == '__main__':
    unittest.main()
