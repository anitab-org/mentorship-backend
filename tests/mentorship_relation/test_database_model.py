import unittest
from datetime import datetime

from tests.base_test_case import BaseTestCase
from app.database.models.user import UserModel
from app.database.models.mentorship_relation import MentorshipRelationModel
from run import db

from tests.utils import user1, user2


# Testing Mentorship Relation database model
#
# Tests:
#     - Mentorship Relation creation
#     - Mentorship Relation setup in mentors and mentee
#     - Mentorship Relation json format
#     - Mentorship Relation update


class TestMentorshipRelationModel(BaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        db.create_all()

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

        self.notes_example = 'description of a good mentorship relation'

        now_datetime = datetime.now()
        self.init_date_example = datetime(year=now_datetime.year + 1, month=3, day=1)
        self.end_date_example = datetime(year=now_datetime.year + 1, month=5, day=1)

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

        self.mentorship_relation = MentorshipRelationModel(
            sender_id=self.first_user.id,
            receiver_id=self.second_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            init_date=self.init_date_example,
            end_date=self.end_date_example,
            notes=self.notes_example
        )
        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test_mentorship_relation_creation(self):
        query_mentorship_relation = MentorshipRelationModel.query.first()

        self.assertTrue(query_mentorship_relation is not None)

        self.assertEqual(query_mentorship_relation.id, 1)

        # asserting relation extra fields
        self.assertEqual(self.first_user.id, query_mentorship_relation.sender_id)
        self.assertEqual(self.second_user.id, query_mentorship_relation.receiver_id)
        self.assertEqual(self.init_date_example, query_mentorship_relation.init_date)
        self.assertEqual(self.end_date_example, query_mentorship_relation.end_date)
        self.assertEqual(self.notes_example, query_mentorship_relation.notes)

        # asserting mentor and mentees setup
        self.assertEqual(self.first_user.id, query_mentorship_relation.mentor_id)
        self.assertEqual(self.second_user.id, query_mentorship_relation.mentee_id)

        # assert mentors' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.first_user.mentor_relations))
        self.assertEqual(query_mentorship_relation, self.first_user.mentor_relations[0])
        self.assertEqual([], self.first_user.mentee_relations)

        # assert mentees' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.second_user.mentee_relations))
        self.assertEqual(query_mentorship_relation, self.second_user.mentee_relations[0])
        self.assertEqual([], self.second_user.mentor_relations)

    def test_mentorship_relation_json_representation(self):
        expected_json = {
            'sender_id': self.first_user.id,
            'receiver_id': self.second_user.id,
            'mentor_id': self.first_user.id,
            'mentee_id': self.second_user.id,
            'init_date': str(self.init_date_example),
            'end_date': str(self.end_date_example),
            'notes': self.notes_example
        }
        print(expected_json)
        self.assertEqual(expected_json, self.mentorship_relation.json())

    def test_mentorship_relation_update(self):
        new_notes = "This contract notes are different..."
        self.mentorship_relation.notes = new_notes

        db.session.add(self.mentorship_relation)
        db.session.commit()

        self.assertEqual(self.mentorship_relation.notes, new_notes)

        # assert mentors' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.first_user.mentor_relations))
        self.assertEqual(new_notes, self.first_user.mentor_relations[0].notes)
        self.assertEqual([], self.first_user.mentee_relations)

        # assert mentees' mentor_relations and mentee_relations
        self.assertEqual(1, len(self.second_user.mentee_relations))
        self.assertEqual(new_notes, self.second_user.mentee_relations[0].notes)
        self.assertEqual([], self.second_user.mentor_relations)

    def test_find_mentorship_relation_by_id(self):
        query_mentorship_relation = MentorshipRelationModel.query.first()
        find_by_id_result = MentorshipRelationModel.find_by_id(query_mentorship_relation.id)
        self.assertEqual(query_mentorship_relation, find_by_id_result)

    def test_empty_table(self):
        self.assertFalse(MentorshipRelationModel.is_empty())
        db.session.delete(self.mentorship_relation)
        db.session.commit()
        self.assertTrue(MentorshipRelationModel.is_empty())




if __name__ == '__main__':
    unittest.main()
