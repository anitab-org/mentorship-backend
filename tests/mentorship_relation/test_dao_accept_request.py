from app import messages
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from app.database.sqlalchemy_extension import db


# TODO test when a user is in a current relation and tries to accept another relation
# TODO test when a user tries to accept a relation where this user is not involved

class TestMentorshipRelationAcceptRequestselfDAO(
    MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestMentorshipRelationAcceptRequestselfDAO, self).setUp()

    def test_dao_accept_non_existing_mentorship_request(self):
        result = self.dao.accept_request(self.first_user.id, 123)

        self.assertEqual(
            (messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404), result)
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)

    def test_dao_requester_tries_to_accept_mentorship_request(self):
        result = self.dao.accept_request(self.first_user.id,
                                         self.mentorship_relation.id)

        self.assertEqual((messages.CANT_ACCEPT_MENTOR_REQ_SENT_BY_USER, 400),
                         result)
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)

    def test_dao_receiver_accepts_mentorship_request(self):
        result = self.dao.accept_request(self.second_user.id,
                                         self.mentorship_relation.id)

        self.assertEqual(
            (messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY, 200),
            result)
        self.assertEqual(MentorshipRelationState.ACCEPTED,
                         self.mentorship_relation.state)

    def test_dao_sender_does_not_exist_mentorship_request(self):
        result = self.dao.accept_request(123, self.mentorship_relation.id)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, 404), result)
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)

    def test_dao_mentorship_request_is_not_in_pending_state(self):
        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.accept_request(self.second_user.id,
                                         self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)

        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.accept_request(self.second_user.id,
                                         self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)

        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.accept_request(self.second_user.id,
                                         self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)

        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = self.dao.accept_request(self.second_user.id,
                                         self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)
