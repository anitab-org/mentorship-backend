from datetime import timedelta, datetime

from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import DB
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import USER1, USER2


class TasksBaseTestCase(BaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    # pylint: disable=too-many-instance-attributes
    def setUp(self):
        super(TasksBaseTestCase, self).setUp()

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

        self.tasks_list_1 = TasksListModel()
        self.tasks_list_2 = TasksListModel()
        self.tasks_list_3 = TasksListModel()

        DB.session.add(self.tasks_list_1)
        DB.session.add(self.tasks_list_2)
        DB.session.add(self.tasks_list_3)
        DB.session.add(self.first_user)
        DB.session.add(self.second_user)
        DB.session.commit()

        # create new mentorship relation

        self.mentorship_relation_w_second_user = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_1,
        )

        self.mentorship_relation_w_admin_user = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.admin_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_2,
        )

        self.mentorship_relation_without_first_user = MentorshipRelationModel(
            action_user_id=self.second_user.id,
            mentor_user=self.second_user,
            mentee_user=self.admin_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_3,
        )

        DB.session.add(self.mentorship_relation_w_second_user)
        DB.session.add(self.mentorship_relation_w_admin_user)
        DB.session.add(self.mentorship_relation_without_first_user)
        DB.session.commit()

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

        DB.session.add(self.tasks_list_1)
        DB.session.add(self.tasks_list_2)
        DB.session.commit()

        self.test_description = "testing this description"
        self.test_is_done = False
