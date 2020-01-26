import json
import unittest

from app import messages
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestRejectMentorshipRequestApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestRejectMentorshipRequestApi, self).setUp()

    def test_reject_mentorship_request(self):
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)
        with self.client:
            response = self.client.put(
                '/mentorship_relation/%s/reject' % self.mentorship_relation.id,
                headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.REJECTED,
                             self.mentorship_relation.state)
            self.assertEqual(
                messages.MENTORSHIP_RELATION_WAS_REJECTED_SUCCESSFULLY,
                json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
