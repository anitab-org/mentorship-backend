import json
import unittest

from app import messages
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestCancelMentorshipRelationApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestCancelMentorshipRelationApi, self).setUp()
        self.mentorship_relation.state = MentorshipRelationState.ACCEPTED
        self.mentorship_relation.save_to_db()

    def test__mentor_cancel_mentorship_relation(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED,
                         self.mentorship_relation.state)
        with self.client:
            response = self.client.put(
                '/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                headers=get_test_request_header(self.first_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.CANCELLED,
                             self.mentorship_relation.state)
            self.assertDictEqual(
                messages.MENTORSHIP_RELATION_WAS_CANCELLED_SUCCESSFULLY,
                json.loads(response.data))

    def test__mentee_cancel_mentorship_relation(self):
        self.assertEqual(MentorshipRelationState.ACCEPTED,
                         self.mentorship_relation.state)
        with self.client:
            response = self.client.put(
                '/mentorship_relation/%s/cancel' % self.mentorship_relation.id,
                headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.CANCELLED,
                             self.mentorship_relation.state)
            self.assertDictEqual(
                messages.MENTORSHIP_RELATION_WAS_CANCELLED_SUCCESSFULLY,
                json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
