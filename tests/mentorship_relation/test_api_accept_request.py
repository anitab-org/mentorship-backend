import json
import unittest

from app import messages
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestAcceptMentorshipRequestApi(MentorshipRelationBaseTestCase):

    def setUp(self):
        super(TestAcceptMentorshipRequestApi, self).setUp()

    def test_accept_mentorship_request(self):
        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)
        with self.client:
            response = self.client.put(
                '/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED,
                             self.mentorship_relation.state)
            self.assertDictEqual(
                messages.MENTORSHIP_RELATION_WAS_ACCEPTED_SUCCESSFULLY,
                json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
