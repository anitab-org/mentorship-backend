from datetime import datetime, timedelta

from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.tasks_list import TasksListModel
from app.utils.enum_utils import MentorshipRelationState
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1, USER2


class TestMentorshipRelationDeleteDAO(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestMentorshipRelationDeleteDAO, self).setUp()

        self.first_user = UserModel(
            name=USER1["name"],
            email=USER1["email"],
            username=USER1["username"],
            password=USER1["password"],
            terms_and_conditions_checked=USER1["terms_and_conditions_checked"],
        )
        self.second_user = UserModel(
            name=USER2["name"],
            email=USER2["email"],
            username=USER2["username"],
            password=USER2["password"],
            terms_and_conditions_checked=USER2["terms_and_conditions_checked"],
        )

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True

        self.notes_example = "description of a good mentorship relation"

        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        DB.session.add(self.first_user)
        DB.session.add(self.second_user)
        DB.session.commit()

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

    def test_dao_delete_non_existing_mentorship_request(self):

        result = MentorshipRelationDAO.delete_request(self.first_user.id, 123)

        self.assertEqual(
            (
                {
                    "message": "This mentorship relation "
                               "request does not exist."
                },
                404,
            ),
            result,
        )
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(
                id=self.mentorship_relation.id
            ).first()
        )

    def test_dao_sender_does_not_exist(self):

        result = MentorshipRelationDAO.delete_request(
            123, self.mentorship_relation.id
        )

        self.assertEqual(({"message": "User does not exist."}, 404), result)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(
                id=self.mentorship_relation.id
            ).first()
        )

    def test_dao_receiver_tries_to_delete_mentorship_request(self):

        result = MentorshipRelationDAO.delete_request(
            self.second_user.id, self.mentorship_relation.id
        )

        self.assertEqual(
            (
                {
                    "message": "You cannot delete a mentorship request "
                               "that you did not create."
                },
                400,
            ),
            result,
        )
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(
                id=self.mentorship_relation.id
            ).first()
        )

    def test_dao_sender_delete_mentorship_request(self):
        relation_id = self.mentorship_relation.id

        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first()
        )

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id, relation_id
        )
        self.assertEqual(
            (
                {"message": "Mentorship relation was deleted successfully."},
                200,
            ),
            result,
        )

        self.assertIsNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first()
        )

    def test_dao_user_not_involved_tries_to_delete_mentorship_request(self):

        result = MentorshipRelationDAO.delete_request(
            self.admin_user.id, self.mentorship_relation.id
        )

        self.assertEqual(
            (
                {
                    "message": "You cannot delete a mentorship request "
                               "that you did not create."
                },
                400,
            ),
            result,
        )
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(
                id=self.mentorship_relation.id
            ).first()
        )

    def test_dao_mentorship_delete_request_not_in_pending_state(self):
        relation_id = self.mentorship_relation.id

        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id, self.mentorship_relation.id
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
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first()
        )

        self.mentorship_relation.state = MentorshipRelationState.COMPLETED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id, self.mentorship_relation.id
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
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first()
        )

        self.mentorship_relation.state = MentorshipRelationState.CANCELLED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id, self.mentorship_relation.id
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
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first()
        )

        self.mentorship_relation.state = MentorshipRelationState.REJECTED
        DB.session.add(self.mentorship_relation)
        DB.session.commit()

        result = MentorshipRelationDAO.delete_request(
            self.first_user.id, self.mentorship_relation.id
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
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=relation_id).first()
        )
