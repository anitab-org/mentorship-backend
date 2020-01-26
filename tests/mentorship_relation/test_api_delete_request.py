import json
import unittest

from app import messages
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import \
    MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestDeleteMentorshipRequestApi(MentorshipRelationBaseTestCase):

    # Setup consists of adding 2 users into the database
    # User 1 is the mentorship relation requester = action user
    # User 2 is the receiver
    def setUp(self):
        super(TestDeleteMentorshipRequestApi, self).setUp()

    def test_sender_delete_mentorship_request(self):
        request_id = self.mentorship_relation.id

        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=request_id).first())

        with self.client:
            response = self.client.delete(
                '/mentorship_relation/%s' % request_id,
                headers=get_test_request_header(self.first_user.id))

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            messages.MENTORSHIP_RELATION_WAS_DELETED_SUCCESSFULLY,
            json.loads(response.data))
        self.assertIsNone(
            MentorshipRelationModel.query.filter_by(id=request_id).first())

    def test_receiver_delete_mentorship_request(self):
        request_id = self.mentorship_relation.id

        self.assertEqual(MentorshipRelationState.PENDING,
                         self.mentorship_relation.state)
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=request_id).first())

        with self.client:
            response = self.client.delete(
                '/mentorship_relation/%s' % request_id,
                headers=get_test_request_header(self.second_user.id))

        self.assertEqual(400, response.status_code)
        self.assertDictEqual(messages.CANT_DELETE_UNINVOLVED_REQUEST,
                             json.loads(response.data))
        self.assertIsNotNone(
            MentorshipRelationModel.query.filter_by(id=request_id).first())


if __name__ == "__main__":
    unittest.main()
