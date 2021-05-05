from datetime import datetime, timedelta
from http import HTTPStatus

from app import messages
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from app.database.sqlalchemy_extension import db


# TODO test when a user tries to reject a relation where this user is not involved


class TestMentorshipRelationListingDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super().setUp()

        self.notes_example = "description of a good mentorship relation"
        self.now_datetime = datetime.utcnow()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test_dao_reject_non_existing_mentorship_request(self):
        DAO = MentorshipRelationDAO()

        result = DAO.reject_request(self.first_user.id, 123)

        self.assertEqual(
            (messages.MENTORSHIP_RELATION_REQUEST_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND),
            result,
        )
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )

    def test_dao_sender_does_not_exist_mentorship_request(self):
        DAO = MentorshipRelationDAO()

        result = DAO.reject_request(123, self.mentorship_relation.id)

        self.assertEqual((messages.USER_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND), result)
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )

    def test_dao_requester_tries_to_reject_mentorship_request(self):
        DAO = MentorshipRelationDAO()

        result = DAO.reject_request(self.first_user.id, self.mentorship_relation.id)

        self.assertEqual(
            (messages.USER_CANT_REJECT_REQUEST_SENT_BY_USER, HTTPStatus.FORBIDDEN),
            result,
        )
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )

    def test_dao_receiver_rejects_mentorship_request(self):
        DAO = MentorshipRelationDAO()

        result = DAO.reject_request(self.second_user.id, self.mentorship_relation.id)

        self.assertEqual(
            (messages.MENTORSHIP_RELATION_WAS_REJECTED_SUCCESSFULLY, HTTPStatus.OK),
            result,
        )
        self.assertEqual(
            MentorshipRelationState.REJECTED, self.mentorship_relation.state
        )

    def test_dao_mentorship_request_is_not_in_pending_state(self):
        DAO = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.reject_request(self.second_user.id, self.mentorship_relation.id)
        self.assertEqual(
            (messages.NOT_PENDING_STATE_RELATION, HTTPStatus.FORBIDDEN), result
        )

        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.reject_request(self.second_user.id, self.mentorship_relation.id)
        self.assertEqual(
            (messages.NOT_PENDING_STATE_RELATION, HTTPStatus.FORBIDDEN), result
        )

        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.reject_request(self.second_user.id, self.mentorship_relation.id)
        self.assertEqual(
            (messages.NOT_PENDING_STATE_RELATION, HTTPStatus.FORBIDDEN), result
        )

        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        db.session.add(self.mentorship_relation)
        db.session.commit()

        result = DAO.reject_request(self.second_user.id, self.mentorship_relation.id)
        self.assertEqual(
            (messages.NOT_PENDING_STATE_RELATION, HTTPStatus.FORBIDDEN), result
        )
