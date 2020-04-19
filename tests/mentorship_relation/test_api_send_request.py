import json
import unittest
from datetime import datetime, timedelta

from app import messages
from app.api.mail_extension import mail
from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestSendRequestApi(MentorshipRelationBaseTestCase):
    def setUp(self):
        super(TestSendRequestApi, self).setUp()
	self.notes_example = 'description of a good mentorship relation'
        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        mail.init_app(self.app)



    def test_fail_send_request_bad_mentee_id(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MENTEE_DOES_NOT_EXIST
        test_payload={
            "mentor_id": self.first_user.id,
            "mentee_id": 1234,
            "end_date": int((datetime.now()+timedelta(days=40)).timestamp()),
            "notes": "some notes"
        }
        actual_response = self.client.post('/mentorship_relation/send_request',
                                           headers=auth_header, content_type='application/json',
                                           data=json.dumps(test_payload))
        self.assertEqual(404, actual_response.status_code)
        self.assertEqual(1, len(outbox))
        self.assertEqual([self.second_user.email], outbox[0].recipients)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_fail_send_request_bad_mentor_id(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MENTOR_DOES_NOT_EXIST
        test_payload={
            "mentor_id": 1234,
            "mentee_id": self.first_user.id,
            "end_date": int((datetime.now()+timedelta(days=40)).timestamp()),
            "notes": "some notes"
        }
        actual_response = self.client.post('/mentorship_relation/send_request',
                                           headers=auth_header, content_type='application/json',
                                           data=json.dumps(test_payload))
        self.assertEqual(404, actual_response.status_code)
        self.assertEqual(1, len(outbox))
        self.assertEqual([self.second_user.email], outbox[0].recipients)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))


    # In case if a user tries to send request on behalf of some other user
    def test_fail_send_request_bad_user_id(self):
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.MATCH_EITHER_MENTOR_OR_MENTEE
        test_payload={
            "mentor_id": self.second_user.id,
            "mentee_id": 4321,
            "end_date": int((datetime.now()+timedelta(days=40)).timestamp()),
            "notes": "some notes"
        }
        actual_response = self.client.post('/mentorship_relation/send_request',
                                           headers=auth_header, content_type='application/json',
                                           data=json.dumps(test_payload))
        self.assertEqual(400, actual_response.status_code)
        self.assertEqual(1, len(outbox))
        self.assertEqual([self.second_user.email], outbox[0].recipients)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))


    def test_create_mentorship_request(self):
        with mail.record_messages() as outbox:
            with self.client:
                response = self.client.post('/mentorship_relation/send_request',
                                            headers=get_test_request_header(self.first_user.id),
                                            json={
                                                "mentor_id": self.first_user.id,
                                                "mentee_id": self.second_user.id,
                                                "end_date": self.end_date_example.timestamp(),
                                                "notes": self.notes_example
                                            })

                self.assertEqual(200, response.status_code)
                self.assertEqual(1, len(outbox))
                self.assertEqual([self.second_user.email], outbox[0].recipients)


    def test_create_invalid_mentorship_request(self):
        with mail.record_messages() as outbox:
            with self.client:
                # receiver's id and action user's id are equal
                response = self.client.post('/mentorship_relation/send_request',
                                            headers=get_test_request_header(self.first_user.id),
                                            json={
                                                "mentor_id": self.first_user.id,
                                                "mentee_id": self.first_user.id,
                                                "end_date": self.end_date_example.timestamp(),
                                                "notes": self.notes_example
                                            })
                self.assertNotEqual(200, response.status_code)
                self.assertEqual(0, len(outbox))




if __name__ == "__main__":
    unittest.main()
