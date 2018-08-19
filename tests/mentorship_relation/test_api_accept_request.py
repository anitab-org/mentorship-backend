import json
import unittest
from datetime import datetime, timedelta

from app.database.models.tasks_list import TasksListModel
from app.database.sqlalchemy_extension import db
from app.database.models.mentorship_relation import MentorshipRelationModel
from app.utils.enum_utils import MentorshipRelationState
from tests.mentorship_relation.relation_base_setup import MentorshipRelationBaseTestCase
from tests.test_utils import get_test_request_header


class TestAcceptMentorshipRequestApi(MentorshipRelationBaseTestCase):

    def setUp(self):
        super(TestAcceptMentorshipRequestApi, self).setUp()

        self.notes_example = 'description of a good mentorship relation'

        self.now_datetime = datetime.now()
        self.end_date_example = self.now_datetime + timedelta(weeks=5)

        # create new mentorship relation

        self.mentorship_relation = MentorshipRelationModel(
            action_user_id=self.first_user.id,
            mentor_user=self.first_user,
            mentee_user=self.second_user,
            creation_date=self.now_datetime.timestamp(),
            end_date=self.end_date_example.timestamp(),
            state=MentorshipRelationState.PENDING,
            notes=self.notes_example,
            tasks_list=TasksListModel()
        )

        db.session.add(self.mentorship_relation)
        db.session.commit()

    def test_accept_mentorship_request(self):
        self.assertEqual(MentorshipRelationState.PENDING, self.mentorship_relation.state)
        with self.client:
            response = self.client.put('/mentorship_relation/%s/accept' % self.mentorship_relation.id,
                                       headers=get_test_request_header(self.second_user.id))

            self.assertEqual(200, response.status_code)
            self.assertEqual(MentorshipRelationState.ACCEPTED, self.mentorship_relation.state)
            self.assertEqual({'message': 'Mentorship relation was accepted successfully.'},
                             json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
