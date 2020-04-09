import unittest
from datetime import datetime, timedelta
from app.api.mail_extension import mail
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header

class TestCreateMentorshipRequestApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestCreateMentorshipRequestApi, self).setUp()

        self.notes_example = 'description of a good mentorship relation'
        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        mail.init_app(self.app)

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
