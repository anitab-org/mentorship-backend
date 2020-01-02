import unittest

from app.api.dao.task_comment import TaskCommentDAO
from app.database.models.task_comment import TaskCommentModel
from tests.tasks.tasks_base_setup import TasksBaseTestCase
from app.database.models.task_comment import TaskCommentsFields
from datetime import timedelta, datetime
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.test_data import user1, user2


class TestTaskCommentDao(TasksBaseTestCase):

    def setUp(self):
        super(TasksBaseTestCase, self).setUp()

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

        self.notes_example = 'description of a good mentorship relation'

        self.now_datetime = datetime.now()
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

        self.mentorship_relation_w_second_user = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_1
        )

        self.mentorship_relation_w_admin_user = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.admin_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_2
        )

        self.mentorship_relation_without_first_user = MentorshipRelationModel(
            action_user_id=self.second_user.id,
            mentor_user=self.second_user,
            mentee_user=self.admin_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes=self.notes_example,
            tasks_list=self.tasks_list_3
        )

        db.session.add(self.mentorship_relation_w_second_user)
        db.session.add(self.mentorship_relation_w_admin_user)
        db.session.add(self.mentorship_relation_without_first_user)
        db.session.commit()

        self.description_example = 'This is an example of a description'

        self.tasks_list_1.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp()
        )
        self.tasks_list_1.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp(),
            is_done=True,
            completed_at=self.end_date_example.timestamp()
        )
        self.tasks_list_2.add_task(
            description=self.description_example,
            created_at=self.now_datetime.timestamp()
        )

        db.session.add(self.tasks_list_1)
        db.session.add(self.tasks_list_2)
        db.session.commit()

        self.test_description = 'testing this description'
        self.test_is_done = False

    def test_dao_create_task_comment(self):
        dao = TaskCommentDAO()
        data = dict(
            user_id=1,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(relation_id=1, user_id=1, task_id=1, data=data)

        # Verify that task comment was inserted in database through DAO
        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=1, task_id=1)
        task_comment = task_comments_list.find_task_comment_by_id(task_comment_id=1)
        self.assertTrue(task_comment is not None)
        self.assertTrue(task_comment[TaskCommentsFields.ID.value] is not None)
        self.assertTrue(task_comment[TaskCommentsFields.ID.value] == 1)
        self.assertIsNotNone(task_comment[TaskCommentsFields.CREATION_DATE.value])
        self.assertEqual(task_comment[TaskCommentsFields.COMMENT.value], 'comment')

    def test_dao_find_by_task_id(self):

        dao = TaskCommentDAO()
        data1 = dict(
            user_id=self.first_user.id,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(relation_id=self.mentorship_relation_w_second_user.id, user_id=self.first_user.id, task_id=1, data=data1)
        data2 = dict(
            user_id=self.first_user.id,
            task_id=1,
            comment='hello'
        )
        dao.create_task_comment(relation_id=self.mentorship_relation_w_second_user.id, user_id=self.first_user.id, task_id=1, data=data2)

        # Verify that find_by_task_id() function is working properly
        task_comments_list = dao.get_task_comments_by_task_id(user_id=self.first_user.id, task_id=1, relation_id=self.mentorship_relation_w_second_user.id)
        for task_comment in task_comments_list:
            self.assertTrue(task_comment is not None)
            self.assertTrue(task_comment[TaskCommentsFields.TASK_ID.value] == 1)
            self.assertIsNotNone(task_comment[TaskCommentsFields.CREATION_DATE.value])
            self.assertTrue(task_comment[TaskCommentsFields.COMMENT.value] == 'comment' or task_comment[TaskCommentsFields.COMMENT.value] == 'hello')

    def test_dao_modify_comment(self):

        dao = TaskCommentDAO()
        data1 = dict(
            user_id=self.first_user.id,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(relation_id=self.mentorship_relation_w_second_user.id, user_id=self.first_user.id, task_id=1,
                                data=data1)

        dao.modify_comment(user_id=self.first_user.id, _id=1, comment='modified comment', relation_id=self.mentorship_relation_w_second_user.id, task_id=1)

        # Verify that task comment was modified
        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=self.mentorship_relation_w_second_user.id, task_id=1)
        task_comment = task_comments_list.find_task_comment_by_id(task_comment_id=1)
        self.assertTrue(task_comment is not None)
        self.assertTrue(task_comment[TaskCommentsFields.ID.value] == 1)
        self.assertIsNotNone(task_comment[TaskCommentsFields.CREATION_DATE.value])
        self.assertEqual(task_comment[TaskCommentsFields.COMMENT.value], 'modified comment')

    def test_dao_delete_comment(self):

        dao = TaskCommentDAO()
        data1 = dict(
            user_id=self.first_user.id,
            task_id=1,
            comment='comment'
        )
        dao.create_task_comment(relation_id=self.mentorship_relation_w_second_user.id, user_id=self.first_user.id, task_id=1,
                                data=data1)

        dao.delete_comment(user_id=self.first_user.id, task_id=1, relation_id=self.mentorship_relation_w_second_user.id, _id=1)

        # Verify that task comment was deleted
        task_comments_list = TaskCommentModel.find_task_comments_list_by_task_id(relation_id=self.mentorship_relation_w_second_user.id, task_id=1)
        task_comment = task_comments_list.find_task_comment_by_id(task_comment_id=1)
        self.assertIsNone(task_comment)


if __name__ == '__main__':
    unittest.main()
