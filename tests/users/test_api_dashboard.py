from datetime import datetime, timedelta

from flask import json

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.database.models.tasks_list import TasksListModel
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.enum_utils import MentorshipRelationState
from tests.base_test_case import BaseTestCase
from tests.test_data import user1, user2
from tests.test_utils import get_test_request_header


class TestDashboardApi(BaseTestCase):

    def setUp(self):
        super(TestDashboardApi, self).setUp()

        self.creation_date = (datetime.now()).timestamp()
        self.end_date = (datetime.now() + timedelta(weeks=4)).timestamp()

        self.user1 = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.user2 = UserModel(
            name=user2['name'],
            email=user2['email'],
            username=user2['username'],
            password=user2['password'],
            terms_and_conditions_checked=user2['terms_and_conditions_checked']
        )
        self.user1.is_email_verified = True
        self.user1.available_to_mentor = True
        self.user1.is_email_verified = True

        self.user2.is_email_verified = True
        self.user2.need_mentoring = True
        self.user2.is_email_verified = True

        self.empty_response = {
            # relations received as mentee, by state
            "pending_relations_received_as_mentee": [],
            "accepted_relations_received_as_mentee": [],
            "rejected_relations_received_as_mentee": [],
            "cancelled_relations_received_as_mentee": [],
            "completed_relations_received_as_mentee": [],

            # relations sent as mentee, by state
            "pending_relations_sent_as_mentee": [],
            "accepted_relations_sent_as_mentee": [],
            "rejected_relations_sent_as_mentee": [],
            "cancelled_relations_sent_as_mentee": [],
            "completed_relations_sent_as_mentee": [],

            # relations received as mentor, by state
            "pending_relations_received_as_mentor": [],
            "accepted_relations_received_as_mentor": [],
            "rejected_relations_received_as_mentor": [],
            "cancelled_relations_received_as_mentor": [],
            "completed_relations_received_as_mentor": [],

            # relations sent as mentor, by state
            "pending_relations_sent_as_mentor": [],
            "accepted_relations_sent_as_mentor": [],
            "rejected_relations_sent_as_mentor": [],
            "cancelled_relations_sent_as_mentor": [],
            "completed_relations_sent_as_mentor": [],
            "tasks_undone": [],
            "tasks_done": []
        }

        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def test_dashboard_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_relations_invalid_id(self):
        auth_header = get_test_request_header(None)  # Supply invalid user ID for the test
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)
        self.assertEqual(404, actual_response.status_code)
        self.assertEqual(messages.USER_NOT_FOUND, json.loads(actual_response.data))

    def test_pending_relations_received_as_mentee(self):
        pending_relation_received_as_mentee = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=self.creation_date,
            end_date=self.end_date,
            state=MentorshipRelationState.PENDING,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(pending_relation_received_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["pending_relations_received_as_mentee"] = [pending_relation_received_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_accepted_relations_received_as_mentee(self):
        accepted_relation_received_as_mentee = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(accepted_relation_received_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["accepted_relations_received_as_mentee"] = [accepted_relation_received_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_rejected_relations_received_as_mentee(self):
        rejected_relation_received_as_mentee = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(rejected_relation_received_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["rejected_relations_received_as_mentee"] = [rejected_relation_received_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_cancelled_relations_received_as_mentee(self):
        cancelled_relation_received_as_mentee = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.CANCELLED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(cancelled_relation_received_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["cancelled_relations_received_as_mentee"] = [cancelled_relation_received_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_completed_relations_received_as_mentee(self):
        completed_relation_received_as_mentee = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(completed_relation_received_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["completed_relations_received_as_mentee"] = [completed_relation_received_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_pending_relations_sent_as_mentee(self):
        pending_relation_sent_as_mentee = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.PENDING,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(pending_relation_sent_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["pending_relations_sent_as_mentee"] = [pending_relation_sent_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_accepted_relations_sent_as_mentee(self):
        pending_accepted_sent_as_mentee = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(pending_accepted_sent_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["accepted_relations_sent_as_mentee"] = [pending_accepted_sent_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_rejected_relations_sent_as_mentee(self):
        rejected_relation_sent_as_mentee = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(rejected_relation_sent_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["rejected_relations_sent_as_mentee"] = [rejected_relation_sent_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_cancelled_relations_sent_as_mentee(self):
        cancelled_relation_sent_as_mentee = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.CANCELLED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(cancelled_relation_sent_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["cancelled_relations_sent_as_mentee"] = [cancelled_relation_sent_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_completed_relations_sent_as_mentee(self):
        completed_relation_sent_as_mentee = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user2,
            mentee_user=self.user1,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(completed_relation_sent_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["completed_relations_sent_as_mentee"] = [completed_relation_sent_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_pending_relations_received_as_mentor(self):
        pending_relation_received_as_mentee = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.PENDING,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(pending_relation_received_as_mentee)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["pending_relations_received_as_mentor"] = [pending_relation_received_as_mentee.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_accepted_relations_received_as_mentor(self):
        accepted_relation_received_as_mentor = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(accepted_relation_received_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["accepted_relations_received_as_mentor"] = [accepted_relation_received_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_rejected_relations_received_as_mentor(self):
        rejected_relation_received_as_mentor = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(rejected_relation_received_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["rejected_relations_received_as_mentor"] = [rejected_relation_received_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_cancelled_relations_received_as_mentor(self):
        cancelled_relation_received_as_mentor = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.CANCELLED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(cancelled_relation_received_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["cancelled_relations_received_as_mentor"] = [cancelled_relation_received_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_completed_relations_received_as_mentor(self):
        completed_relation_received_as_mentor = MentorshipRelationModel(
            action_user_id=self.user2.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(completed_relation_received_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["completed_relations_received_as_mentor"] = [completed_relation_received_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_pending_relations_sent_as_mentor(self):
        pending_relation_sent_as_mentor = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.PENDING,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(pending_relation_sent_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["pending_relations_sent_as_mentor"] = [pending_relation_sent_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_accepted_relations_sent_as_mentor(self):
        accepted_relation_sent_as_mentor = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.ACCEPTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(accepted_relation_sent_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["accepted_relations_sent_as_mentor"] = [accepted_relation_sent_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_pending_relations_sent_as_mentor(self):
        rejected_relation_sent_as_mentor = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.REJECTED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(rejected_relation_sent_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["rejected_relations_sent_as_mentor"] = [rejected_relation_sent_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_cancelled_relations_sent_as_mentor(self):
        cancelled_relation_sent_as_mentor = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.CANCELLED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(cancelled_relation_sent_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["cancelled_relations_sent_as_mentor"] = [cancelled_relation_sent_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

    def test_completed_relations_sent_as_mentor(self):
        completed_relation_sent_as_mentor = MentorshipRelationModel(
            action_user_id=self.user1.id,
            mentor_user=self.user1,
            mentee_user=self.user2,
            creation_date=(datetime.now()).timestamp(),
            end_date=(datetime.now() + timedelta(weeks=4)).timestamp(),
            state=MentorshipRelationState.COMPLETED,
            notes="",
            tasks_list=TasksListModel()
        )
        db.session.add(completed_relation_sent_as_mentor)
        db.session.commit()

        expected_response = self.empty_response
        expected_response["completed_relations_sent_as_mentor"] = [completed_relation_sent_as_mentor.json()]

        auth_header = get_test_request_header(self.user1.id)
        actual_response = self.client.get('/dashboard', follow_redirects=True, headers=auth_header)

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))
