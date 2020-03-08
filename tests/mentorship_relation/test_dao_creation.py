import unittest
from datetime import datetime, timedelta

from app import messages
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from app.database.sqlalchemy_extension import db


class TestMentorshipRelationCreationDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super(TestMentorshipRelationCreationDAO, self).setUp()

        self.notes_example = "description of a good mentorship relation"

        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

    def test_dao_create_mentorship_relation_with_good_args_mentor_is_sender(self):
        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=self.first_user.id,
            mentee_id=self.second_user.id,
            end_date=self.end_date_example.timestamp(),
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(self.first_user.id, data)

        self.assertEqual(messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, result[0])

        query_mentorship_relation = MentorshipRelationModel.query.first()

        self.assertTrue(query_mentorship_relation is not None)

        self.assertEqual(1, query_mentorship_relation.id)

        # asserting relation extra fields
        self.assertEqual(self.first_user.id, query_mentorship_relation.action_user_id)
        self.assertEqual(self.notes_example, query_mentorship_relation.notes)

        # asserting dates
        self.assertIsNone(query_mentorship_relation.start_date)
        self.assertEqual(
            self.end_date_example.timestamp(), query_mentorship_relation.end_date
        )

        # asserting mentor and mentees setup
        self.assertEqual(self.first_user.id, query_mentorship_relation.mentor_id)
        self.assertEqual(self.second_user.id, query_mentorship_relation.mentee_id)

        # assert mentors' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.first_user.mentor_relations))
        self.assertEqual(query_mentorship_relation, self.first_user.mentor_relations[0])
        self.assertEqual([], self.first_user.mentee_relations)

        # assert mentees' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.second_user.mentee_relations))
        self.assertEqual(
            query_mentorship_relation, self.second_user.mentee_relations[0]
        )
        self.assertEqual([], self.second_user.mentor_relations)

    def test_dao_create_mentorship_relation_with_good_args_mentor_is_receiver(self):
        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=self.first_user.id,
            mentee_id=self.second_user.id,
            end_date=self.end_date_example.timestamp(),
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(self.second_user.id, data)

        self.assertEqual(messages.MENTORSHIP_RELATION_WAS_SENT_SUCCESSFULLY, result[0])

        query_mentorship_relation = MentorshipRelationModel.query.first()

        self.assertTrue(query_mentorship_relation is not None)

        self.assertEqual(1, query_mentorship_relation.id)

        # asserting relation extra fields
        self.assertEqual(self.second_user.id, query_mentorship_relation.action_user_id)
        self.assertEqual(self.notes_example, query_mentorship_relation.notes)

        # asserting dates
        # asserting dates
        self.assertIsNone(query_mentorship_relation.start_date)
        self.assertEqual(
            self.end_date_example.timestamp(), query_mentorship_relation.end_date
        )

        # asserting mentor and mentees setup
        self.assertEqual(self.first_user.id, query_mentorship_relation.mentor_id)
        self.assertEqual(self.second_user.id, query_mentorship_relation.mentee_id)

        # assert mentors' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.first_user.mentor_relations))
        self.assertEqual(query_mentorship_relation, self.first_user.mentor_relations[0])
        self.assertEqual([], self.first_user.mentee_relations)

        # assert mentees' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.second_user.mentee_relations))
        self.assertEqual(
            query_mentorship_relation, self.second_user.mentee_relations[0]
        )
        self.assertEqual([], self.second_user.mentor_relations)

    def test_dao_create_mentorship_relation_with_non_existent_mentor(self):
        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=1234,
            mentee_id=self.second_user.id,
            end_date=self.end_date_example.timestamp(),
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(1234, data)

        self.assertDictEqual(messages.MENTOR_DOES_NOT_EXIST, result[0])

        query_mentorship_relation = MentorshipRelationModel.query.first()

        self.assertIsNone(query_mentorship_relation)

    def test_dao_create_mentorship_relation_with_non_existent_mentee(self):
        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=self.first_user.id,
            mentee_id=1234,
            end_date=self.end_date_example.timestamp(),
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(self.first_user.id, data)

        self.assertDictEqual(messages.MENTEE_DOES_NOT_EXIST, result[0])

        query_mentorship_relation = MentorshipRelationModel.query.first()

        self.assertIsNone(query_mentorship_relation)

    def test_dao_create_mentorship_relation_with_mentee_already_in_relation(self):

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.admin_user.id,
            mentor_user=self.admin_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()
        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=self.first_user.id,
            mentee_id=self.second_user.id,
            end_date=self.end_date_example.timestamp(),
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(self.first_user.id, data)

        self.assertEqual((messages.MENTEE_ALREADY_IN_A_RELATION, 400), result)

        query_mentorship_relations = MentorshipRelationModel.query.all()

        self.assertTrue(1, len(query_mentorship_relations))

    def test_dao_create_mentorship_relation_with_mentor_already_in_relation(self):

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.admin_user.id,
            mentor_user=self.admin_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=self.second_user.id,
            mentee_id=self.first_user.id,
            end_date=self.end_date_example.timestamp(),
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(self.second_user.id, data)

        self.assertEqual((messages.MENTOR_ALREADY_IN_A_RELATION, 400), result)

        query_mentorship_relations = MentorshipRelationModel.query.all()

        self.assertTrue(1, len(query_mentorship_relations))

    def test_dao_create_mentorship_relation_with_good_args_but_invalid_timestamp(self):
        dao = MentorshipRelationDAO()
        data = dict(
            mentor_id=self.first_user.id,
            mentee_id=self.second_user.id,
            end_date=1580338800000000,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        # Use DAO to create a mentorship relation

        result = dao.create_mentorship_relation(self.first_user.id, data)

        self.assertEqual(messages.INVALID_END_DATE, result[0])
        self.assertEqual(400, result[1])


if __name__ == "__main__":
    unittest.main()
