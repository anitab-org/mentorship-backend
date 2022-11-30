import unittest
from datetime import datetime, timedelta
from http import HTTPStatus

from app import messages
from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase


class TestListMentorshipRelationsDAO(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    def setUp(self):
        super().setUp()

        self.notes_example = "description of a good mentorship relation"
        self.now_datetime = datetime.utcnow()
        self.past_end_date_example = self.now_datetime - timedelta(weeks=5)
        self.future_end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.past_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.past_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        self.future_pending_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        self.future_accepted_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel(),
        )

        db.session.add(self.past_mentorship_relation)
        db.session.add(self.future_pending_mentorship_relation)
        db.session.add(self.future_accepted_mentorship_relation)
        db.session.commit()

    def test_dao_list_past_mentorship_relations(self):

        result = MentorshipRelationDAO.list_past_mentorship_relations(
            user_id=self.first_user.id
        )

        expected_response = [self.past_mentorship_relation]

        self.assertIsNotNone(result[0])
        self.assertEqual(expected_response, result[0])

    def test_dao_list_current_mentorship_relation(self):

        result = MentorshipRelationDAO.list_current_mentorship_relation(
            user_id=self.first_user.id
        )
        expected_response = self.future_accepted_mentorship_relation

        self.assertEqual(expected_response, result)

    def test_dao_list_non_existing_current_mentorship_relation(self):
        result = MentorshipRelationDAO.list_current_mentorship_relation(
            user_id=self.admin_user.id
        )
        expected_response = (messages.NOT_IN_MENTORED_RELATION_CURRENTLY, HTTPStatus.OK)

        self.assertEqual(expected_response, result)

    def test_dao_list_pending_mentorship_relation(self):

        result = MentorshipRelationDAO.list_pending_mentorship_relations(
            user_id=self.first_user.id
        )
        expected_response = [self.future_pending_mentorship_relation]

        self.assertEqual(expected_response, result[0])
        self.assertEqual(HTTPStatus.OK, result[1])


if __name__ == "__main__":
    unittest.main()
