from app import messages
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.utils.enum_utils import MentorshipRelationState
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.sqlalchemy_extension import db
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase


class TestMentorshipRelationDeleteDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestMentorshipRelationDeleteDAO, self).setUp()

    def test_dao_delete_non_existing_mentorship_request(self):
        result = MentorshipRelationDAO.delete_request(self.first_user.id, 123)

        self.assertEqual(
            (messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, 404), result)
        self.assertIsNotNone(MentorshipRelationModel.query.filter_by(
            id=self.mentorship_relation.id).first())

    def test_dao_sender_does_not_exist(self):
        result = MentorshipRelationDAO.delete_request(
            123, self.mentorship_relation.id)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, 404), result)
        self.assertIsNotNone(MentorshipRelationModel.query.filter_by(
            id=self.mentorship_relation.id).first())

    def test_dao_receiver_tries_to_delete_mentorship_request(self):
        result = MentorshipRelationDAO.delete_request(
            self.second_user.id,
            self.mentorship_relation.id)

        self.assertEqual((messages.CANT_DELETE_UNINVOLVED_REQUEST, 400), result)
        self.assertIsNotNone(MentorshipRelationModel.query.filter_by(
            id=self.mentorship_relation.id).first())

    def test_dao_sender_delete_mentorship_request(self):
        relation_id = self.mentorship_relation.id

        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first())

        result = MentorshipRelationDAO.delete_request(self.first_user.id,
                                                      relation_id)
        self.assertEqual(
            (messages.MENTORSHIP_RELATION_WAS_DELETED_SUCCESSFULLY, 200),
            result)

        self.assertIsNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first())

    def test_dao_user_not_involved_tries_to_delete_mentorship_request(self):
        result = MentorshipRelationDAO.delete_request(
            self.admin_user.id,
            self.mentorship_relation.id)

        self.assertEqual((messages.CANT_DELETE_UNINVOLVED_REQUEST, 400), result)
        self.assertIsNotNone(MentorshipRelationModel.query.filter_by(
            id=self.mentorship_relation.id).first())

    def test_dao_mentorship_delete_request_not_in_pending_state(self):
        relation_id = self.mentorship_relation.id

        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id,
            self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first())

        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id,
            self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first())

        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id,
            self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first())

        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id,
            self.mentorship_relation.id)
        self.assertEqual((messages.NOT_PENDING_STATE_RELATION, 400), result)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first())
