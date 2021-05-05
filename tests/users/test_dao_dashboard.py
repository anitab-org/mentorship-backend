import unittest
from flask_restx import marshal
from app.api.models.mentorship_relation import list_tasks_response_body
from app.api.email_utils import generate_confirmation_token
from app.api.dao.user import UserDAO, DashboardRelationResponseModel
from datetime import timedelta, datetime
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2


class TestUserDao(BaseTestCase):
    def setUp(self):
        super().setUp()

        self.first_user = UserModel(
            name=user1["name"],
            email=user1["email"],
            username=user1["username"],
            password=user1["password"],
            terms_and_conditions_checked=user1["terms_and_conditions_checked"],
        )
        self.second_user = UserModel(
            name=user2["name"],
            email=user2["email"],
            username=user2["username"],
            password=user2["password"],
            terms_and_conditions_checked=user2["terms_and_conditions_checked"],
        )

        # making sure both are available to be mentor or mentee
        self.first_user.need_mentoring = True
        self.first_user.available_to_mentor = True
        self.first_user.is_email_verified = True
        self.second_user.need_mentoring = True
        self.second_user.available_to_mentor = True
        self.second_user.is_email_verified = True

        self.notes_example = "description of a good mentorship relation"

        self.now_datetime = datetime.utcnow()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        self.tasks_list_1 = TasksListModel()
        self.tasks_list_2 = TasksListModel()
        self.tasks_list_3 = TasksListModel()

        db.session.add(self.tasks_list_1)
        db.session.add(self.tasks_list_2)
        db.session.add(self.tasks_list_3)
        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.commit()

        # create new mentorship relation
        self.mentorship_relation1 = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_1,
        )

        self.mentorship_relation2 = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=self.tasks_list_2,
        )

        self.mentorship_relation3 = MentorshipRelationModel(
            action_user_id=self.second_user.id,
            mentor_user=self.second_user,
            mentee_user=self.first_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.CANCELLED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_3,
        )

        db.session.add(self.mentorship_relation1)
        db.session.add(self.mentorship_relation3)
        db.session.add(self.mentorship_relation2)
        db.session.commit()

        self.description_example = "This is an example of a description"

        self.tasks_list_1.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
        )
        self.tasks_list_1.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
            is_done=True,
            completed_at=self.end_date_example.timestamp(),
        )
        self.tasks_list_2.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
        )

        db.session.add(self.tasks_list_1)
        db.session.add(self.tasks_list_2)
        db.session.commit()

        self.test_description = "testing this description"
        self.test_is_done = False

    def test_dao_get_user_dashboard(self):
        expected_response = {
            "as_mentor": {
                "sent": {
                    "accepted": [
                        DashboardRelationResponseModel(
                            self.mentorship_relation1
                        ).response
                    ],
                    "rejected": [],
                    "completed": [],
                    "cancelled": [],
                    "pending": [
                        DashboardRelationResponseModel(
                            self.mentorship_relation2
                        ).response
                    ],
                },
                "received": {
                    "accepted": [],
                    "rejected": [],
                    "completed": [],
                    "cancelled": [],
                    "pending": [],
                },
            },
            "as_mentee": {
                "sent": {
                    "accepted": [],
                    "rejected": [],
                    "completed": [],
                    "cancelled": [],
                    "pending": [],
                },
                "received": {
                    "accepted": [],
                    "rejected": [],
                    "completed": [],
                    "cancelled": [
                        DashboardRelationResponseModel(
                            self.mentorship_relation3
                        ).response
                    ],
                    "pending": [],
                },
            },
            "tasks_todo": [
                marshal(self.tasks_list_1.find_task_by_id(1), list_tasks_response_body)
            ],
            "tasks_done": [
                marshal(self.tasks_list_1.find_task_by_id(2), list_tasks_response_body)
            ],
        }
        actual_response = UserDAO.get_user_dashboard(self.first_user.id)
        self.assertEqual(actual_response, expected_response)


if __name__ == "__main__":
    unittest.main()
