import unittest

from app import messages
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from app.database.sqlalchemy_extension import db


# TODO test combination of parameters while listing relations

class TestMentorshipRelationListingDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super(TestMentorshipRelationListingDAO, self).setUp()

    def test_dao_list_mentorship_relation_accepted(self):
        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.list_mentorship_relations(user_id=self.first_user.id,
                                                    accepted=True)

        self.assertEqual((messages.NOT_IMPLEMENTED, 200), result)

    def test_dao_list_mentorship_relation_cancelled(self):
        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.list_mentorship_relations(user_id=self.first_user.id,
                                                    cancelled=True)

        self.assertEqual((messages.NOT_IMPLEMENTED, 200), result)

    def test_dao_list_mentorship_relation_rejected(self):
        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.list_mentorship_relations(user_id=self.first_user.id,
                                                    rejected=True)

        self.assertEqual((messages.NOT_IMPLEMENTED, 200), result)

    def test_dao_list_mentorship_relation_completed(self):
        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.list_mentorship_relations(user_id=self.first_user.id,
                                                    completed=True)

        self.assertEqual((messages.NOT_IMPLEMENTED, 200), result)

    def test_dao_list_mentorship_relation_pending(self):
        self.mentorship_relation.state = MentorshipRelationState.PENDING
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.list_mentorship_relations(user_id=self.first_user.id,
                                                    pending=True)

        self.assertEqual((messages.NOT_IMPLEMENTED, 200), result)

    def test_dao_list_mentorship_relation_all(self):
        self.mentorship_relation.state = MentorshipRelationState.PENDING
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.list_mentorship_relations(user_id=self.first_user.id)
        expected_response = [self.mentorship_relation], 200

        self.assertIsNotNone(result)
        self.assertEqual(expected_response, result)


if __name__ == '__main__':
    unittest.main()
