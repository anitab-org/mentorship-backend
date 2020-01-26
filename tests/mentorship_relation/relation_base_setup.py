from datetime import datetime, timedelta

from app.api.dao.mentorship_relation import MentorshipRelationDAO
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import *


class MentorshipRelationBaseTestCase(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(MentorshipRelationBaseTestCase, self).setUp()

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

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.first_user.is_email_verified = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True
        self.second_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

        self.notes_example = 'description of a good mentorship relation'

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
            tasks_list=TasksListModel()
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

        self.dao = MentorshipRelationDAO()

    # creates past, future_pending and future_accepted mentorship relations
    def create_mentorship_relations(self):
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
            tasks_list=TasksListModel()
        )

        self.future_pending_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

        self.future_accepted_mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.future_end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

        db.session.add(self.past_mentorship_relation)
        db.session.add(self.future_pending_mentorship_relation)
        db.session.add(self.future_accepted_mentorship_relation)
        db.session.commit()
