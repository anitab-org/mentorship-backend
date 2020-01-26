import unittest

from app import messages
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase


class TestListMentorshipRelationsDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super(TestListMentorshipRelationsDAO, self).setUp()
        super(TestListMentorshipRelationsDAO,
              self).create_mentorship_relations()

    def test_dao_list_past_mentorship_relations(self):
        result = MentorshipRelationDAO.list_past_mentorship_relations(
            user_id=self.first_user.id)

        expected_response = [self.past_mentorship_relation]

        self.assertIsNotNone(result[0])
        self.assertEqual(expected_response, result[0])

    def test_dao_list_current_mentorship_relation(self):
        result = MentorshipRelationDAO.list_current_mentorship_relation(
            user_id=self.first_user.id)
        expected_response = self.future_accepted_mentorship_relation

        self.assertEqual(expected_response, result)

    def test_dao_list_non_existing_current_mentorship_relation(self):
        result = MentorshipRelationDAO.list_current_mentorship_relation(
            user_id=self.admin_user.id)
        expected_response = (messages.NOT_IN_MENTORED_RELATION_CURRENTLY, 200)

        self.assertEqual(expected_response, result)

    def test_dao_list_pending_mentorship_relation(self):
        result = MentorshipRelationDAO.list_pending_mentorship_relations(
            user_id=self.first_user.id)
        expected_response = self.future_pending_mentorship_relation

        self.assertEqual(expected_response, result[0][1])
        self.assertEqual(200, result[1])


if __name__ == '__main__':
    unittest.main()
