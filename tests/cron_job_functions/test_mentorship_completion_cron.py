import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.schedulers.complete_mentorship_cron_job import \
    complete_overdue_mentorship_relations_job
from app.utils.enum_utils import MentorshipRelationState
from tests.tasks.tasks_base_setup import TasksBaseTestCase


class TestCompleteMentorshipRelationCronFunction(TasksBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestCompleteMentorshipRelationCronFunction, self).setUp()

        self.now_datetime = datetime.now()
        self.past_end_date_example = self.now_datetime - timedelta(weeks=5)
        self.future_end_date_example = self.now_datetime + timedelta(weeks=5)

        self.mentorship_relation_1 = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.past_end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_1
        )

        self.mentorship_relation_2 = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.past_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=self.tasks_list_2
        )

        self.mentorship_relation_3 = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_3
        )

        db.session.add(self.mentorship_relation_1)
        db.session.add(self.mentorship_relation_2)
        db.session.add(self.mentorship_relation_3)
        db.session.commit()

    def get_test_app(self):
        return self.app

    @patch('run.application', side_effect=get_test_app)
    def test_complete_mentorship_relations_accepted(self, get_test_app_fn):
        self.assertEqual(MentorshipRelationState.ACCEPTED,
                         self.mentorship_relation_1.state)
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation_2.state)
        self.assertEqual(MentorshipRelationState.ACCEPTED,
                         self.mentorship_relation_3.state)

        complete_overdue_mentorship_relations_job()

        self.assertEqual(MentorshipRelationState.COMPLETED,
                         self.mentorship_relation_1.state)
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation_2.state)
        self.assertEqual(MentorshipRelationState.ACCEPTED,
                         self.mentorship_relation_3.state)


if __name__ == "__main__":
    unittest.main()
