import unittest
from http import HTTPStatus

from app import messages
from app.api.dao.user import UserDAO
from app.database.models.user import UserModel
from tests.base_test_case import BaseTestCase


class TestUpdateUserDao(BaseTestCase):
    def test_dao_update_user(self):

        self.assertIsNotNone(self.admin_user.name)
        self.assertIsNone(self.admin_user.bio)
        self.assertIsNone(self.admin_user.location)
        self.assertIsNone(self.admin_user.occupation)
        self.assertIsNone(self.admin_user.organization)
        self.assertIsNone(self.admin_user.slack_username)
        self.assertIsNone(self.admin_user.social_media_links)
        self.assertIsNone(self.admin_user.skills)
        self.assertIsNone(self.admin_user.interests)
        self.assertIsNone(self.admin_user.resume_url)
        self.assertIsNone(self.admin_user.photo_url)

        data = dict(
            name="good_name",
            bio="good_bio",
            location="good_location",
            occupation="good_developer",
            organization="good_org",
            slack_username="good_slack_username",
            social_media_links="good_social_media_links",
            skills="good_skills",
            interests="good_interests",
            resume_url="good_resume_url",
            photo_url="good_photo_url",
        )
        UserDAO.update_user_profile(self.admin_user.id, data)

        self.assertEqual("good_name", self.admin_user.name)
        self.assertEqual("good_bio", self.admin_user.bio)
        self.assertEqual("good_location", self.admin_user.location)
        self.assertEqual("good_developer", self.admin_user.occupation)
        self.assertEqual("good_org", self.admin_user.organization)
        self.assertEqual("good_slack_username", self.admin_user.slack_username)
        self.assertEqual("good_social_media_links", self.admin_user.social_media_links)
        self.assertEqual("good_skills", self.admin_user.skills)
        self.assertEqual("good_interests", self.admin_user.interests)
        self.assertEqual("good_resume_url", self.admin_user.resume_url)
        self.assertEqual("good_photo_url", self.admin_user.photo_url)

    def test_update_fields_with_empty_data(self):

        name_before_update = self.admin_user.name
        self.assertIsNotNone(self.admin_user.name)

        self.assertIsNone(self.admin_user.bio)
        self.assertIsNone(self.admin_user.location)
        self.assertIsNone(self.admin_user.occupation)
        self.assertIsNone(self.admin_user.organization)
        self.assertIsNone(self.admin_user.slack_username)
        self.assertIsNone(self.admin_user.social_media_links)
        self.assertIsNone(self.admin_user.skills)
        self.assertIsNone(self.admin_user.interests)
        self.assertIsNone(self.admin_user.resume_url)
        self.assertIsNone(self.admin_user.photo_url)

        data = dict(
            name="",
            bio="",
            location="",
            occupation="",
            organization="",
            slack_username="",
            social_media_links="",
            skills="",
            interests="",
            resume_url="",
            photo_url="",
        )
        UserDAO.update_user_profile(self.admin_user.id, data)

        name_after_update = self.admin_user.name
        self.assertIsNotNone(self.admin_user.name)
        self.assertEqual(name_before_update, name_after_update)

        self.assertIsNone(self.admin_user.bio)
        self.assertIsNone(self.admin_user.location)
        self.assertIsNone(self.admin_user.occupation)
        self.assertIsNone(self.admin_user.organization)
        self.assertIsNone(self.admin_user.slack_username)
        self.assertIsNone(self.admin_user.social_media_links)
        self.assertIsNone(self.admin_user.skills)
        self.assertIsNone(self.admin_user.interests)
        self.assertIsNone(self.admin_user.resume_url)
        self.assertIsNone(self.admin_user.photo_url)

    def test_update_user_that_does_not_exist(self):

        user = UserModel.query.filter_by(id=2).first()
        self.assertIsNone(user)

        data = dict(occupation="good_developer", organization="good_org")
        dao_result = UserDAO.update_user_profile(user, data)

        self.assertEqual(
            (messages.USER_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND), dao_result
        )


if __name__ == "__main__":
    unittest.main()
