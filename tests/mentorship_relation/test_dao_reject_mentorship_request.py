from datetime import datetime, timedelta

from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import DB
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import (
    MentorshipRelationBaseTestCase,
)


# TODO test when a user tries to reject a relation
#      where this user is not involved


class TestMentorshipRelationListingDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestMentorshipRelationListingDAO, self).setUp()

        self.notes_example = "description of a good mentorship relation"
        self.now_datetime = datetime.now()
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

        DB.session.add(self.mentorship_relation)
        DB.session.commit()

    def test_dao_reject_non_existing_mentorship_request(self):
        dao = MentorshipRelationDAO()

        result = dao.reject_request(self.first_user.id, 123)

        self.assertEqual(
            (
                {
                    "message": "This mentorship relation request "
                               "does not exist."
                },
                404,
            ),
            result,
        )
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )

    def test_dao_sender_does_not_exist_mentorship_request(self):
        dao = MentorshipRelationDAO()

        result = dao.reject_request(123, self.mentorship_relation.id)

        self.assertEqual(({"message": "User does not exist."}, 404), result)
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )

    def test_dao_requester_tries_to_reject_mentorship_request(self):
        dao = MentorshipRelationDAO()

        result = dao.reject_request(
            self.first_user.id, self.mentorship_relation.id
        )

        self.assertEqual(
            (
                {
                    "message": "You cannot reject "
                               "a mentorship request sent by yourself."
                },
                400,
            ),
            result,
        )
        self.assertEqual(
            MentorshipRelationState.PENDING, self.mentorship_relation.state
        )

    def test_dao_receiver_rejects_mentorship_request(self):
        dao = MentorshipRelationDAO()

        result = dao.reject_request(
            self.second_user.id, self.mentorship_relation.id
        )

        self.assertEqual(
            (
                {"message": "Mentorship relation was rejected successfully."},
                200,
            ),
            result,
        )
        self.assertEqual(
            MentorshipRelationState.REJECTED, self.mentorship_relation.state
        )

    def test_dao_mentorship_request_is_not_in_pending_state(self):
        dao = MentorshipRelationDAO()

        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = dao.reject_request(
            self.second_user.id, self.mentorship_relation.id
        )
        self.assertEqual(
            (
                {
                    "message": "This mentorship relation "
                               "is not in the pending state."
                },
                400,
            ),
            result,
        )

        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = dao.reject_request(
            self.second_user.id, self.mentorship_relation.id
        )
        self.assertEqual(
            (
                {
                    "message": "This mentorship relation "
                               "is not in the pending state."
                },
                400,
            ),
            result,
        )

        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = dao.reject_request(
            self.second_user.id, self.mentorship_relation.id
        )
        self.assertEqual(
            (
                {
                    "message": "This mentorship relation is not "
                               "in the pending state."
                },
                400,
            ),
            result,
        )

        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = dao.reject_request(
            self.second_user.id, self.mentorship_relation.id
        )
        self.assertEqual(
            (
                {
                    "message": "This mentorship relation "
                               "is not in the pending state."
                },
                400,
            ),
            result,
        )
