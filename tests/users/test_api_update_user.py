import unittest
from random import SystemRandom
from string import ascii_lowercase

from flask import json

from app import messages
from app.api.validations.user import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH
from app.database.models.user import UserModel
from app.database.sqlalchemy_extension import db
from app.utils.validation_utils import get_length_validation_error_message
from tests.base_test_case import BaseTestCase
from tests.test_data import user1
from tests.test_utils import get_test_request_header
from datetime import timedelta


class TestUpdateUserApi(BaseTestCase):

    def test_update_user_api_resource_non_auth(self):
        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.put('/user', follow_redirects=True)

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_update_username_already_taken(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.commit()

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.USER_USES_A_USERNAME_THAT_ALREADY_EXISTS
        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(username=self.admin_user.username)),
                                          content_type='application/json')

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))

    def test_update_username_not_taken(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.commit()

        user1_new_username = "new_username"
        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.USER_SUCCESSFULLY_UPDATED
        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(username=user1_new_username)),
                                          content_type='application/json')

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))
        self.assertEqual(user1_new_username, self.first_user.username)

    def test_update_username_invalid_length(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.commit()

        field_name = 'username'
        secure_random = SystemRandom()
        random_generated_username = "".join(
            secure_random.choice(ascii_lowercase) for x in range(USERNAME_MAX_LENGTH + 1))

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = {"message": get_length_validation_error_message(field_name, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH)}
        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(username=random_generated_username)),
                                          content_type='application/json')

        self.assertEqual(400, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))
        self.assertNotEqual(random_generated_username, self.first_user.username)
        self.assertEqual(user1['username'], self.first_user.username)

    def test_update_availability_to_mentor_more_than_once(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True

        db.session.add(self.first_user)
        db.session.commit()

        expected_response = messages.USER_SUCCESSFULLY_UPDATED
        test_mentor_availability = True
        auth_header = get_test_request_header(self.first_user.id)

        self.assertEqual(False, self.first_user.available_to_mentor)

        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(available_to_mentor=test_mentor_availability)),
                                          content_type='application/json')

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        self.assertEqual(test_mentor_availability, self.first_user.available_to_mentor)

        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(available_to_mentor=not test_mentor_availability)),
                                          content_type='application/json')

        self.assertEqual(200, actual_response.status_code)
        self.assertEqual(expected_response, json.loads(actual_response.data))

        self.assertEqual(not test_mentor_availability, self.first_user.available_to_mentor)

    def test_update_availability_to_be_mentee_to_false(self):

        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True
        self.first_user.need_mentoring = True

        db.session.add(self.first_user)
        db.session.commit()

        expected_response = messages.USER_SUCCESSFULLY_UPDATED
        test_need_mentoring = False
        auth_header = get_test_request_header(self.first_user.id)

        self.assertEqual(True, self.first_user.need_mentoring)

        actual_response = self.client.put('/user', follow_redirects=True,
                                          headers=auth_header,
                                          data=json.dumps(dict(need_mentoring=test_need_mentoring)),
                                          content_type='application/json')

        self.assertEqual(200, actual_response.status_code)
        self.assertDictEqual(expected_response, json.loads(actual_response.data))
        self.assertEqual(test_need_mentoring, self.first_user.need_mentoring)

    #Change password to a different password from the current one (PASS)
    #Response= 201, PASSWORD_SUCCESSFULLY_UPDATED
    def test_password_change_differentpassword(self):
        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True
        db.session.add(self.first_user)
        db.session.commit()

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.PASSWORD_SUCCESSFULLY_UPDATED
        actual_response = self.client.put(
            '/user/change_password', follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(current_password=user1['password'],
                                 new_password="password")),
            content_type='application/json')

        self.assertEqual(201, actual_response.status_code)
        self.assertDictEqual(expected_response,
                             json.loads(actual_response.data))

    #Change password to an empty password (FAIL)
    #Response= 400, USER_ENTERED_EMPTY_PASSWORD_FOR_NEW_PASSWORD
    def test_password_change_emptypassword(self):
        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True
        db.session.add(self.first_user)
        db.session.commit()

        auth_header = get_test_request_header(self.first_user.id)
        actual_response = self.client.put(
            '/user/change_password', follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(current_password=user1['password'],
                                 new_password="")),
            content_type='application/json')
        expected_result = {"message": get_length_validation_error_message("new_password", PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH)}

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_result,
                             json.loads(actual_response.data))

    #Change password to a password with white spaces (FAIL)
    #Response= 400, USER_INPUTS_SPACE_IN_PASSWORD
    def test_password_change_passwordwithspaces(self):
        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True
        db.session.add(self.first_user)
        db.session.commit()

        auth_header = get_test_request_header(self.first_user.id)
        expected_response = messages.USER_INPUTS_SPACE_IN_PASSWORD
        actual_response = self.client.put(
            '/user/change_password', follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(current_password=user1['password'],
                                 new_password="h e l l o 1 2 3")),
            content_type='application/json')

        self.assertEqual(400, actual_response.status_code)
        self.assertDictEqual(expected_response,
                             json.loads(actual_response.data))

    #Valid user tries to change password with authentication token missing (FAIL)
    #Response= 401, AUTHORISATION_TOKEN_IS_MISSING
    def test_password_change_notoken(self):
        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True
        db.session.add(self.first_user)
        db.session.commit()

        expected_response = messages.AUTHORISATION_TOKEN_IS_MISSING
        actual_response = self.client.put(
            '/user/change_password', follow_redirects=True,
            data=json.dumps(dict(current_password=user1['password'],
                                 new_password="password")),
            content_type='application/json')

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response,
                             json.loads(actual_response.data))

    #Valid user tries to change password with authentication token expired (FAIL)
    #Response= 401, TOKEN_HAS_EXPIRED
    def test_password_change_expiredtoken(self):
        self.first_user = UserModel(
            name=user1['name'],
            email=user1['email'],
            username=user1['username'],
            password=user1['password'],
            terms_and_conditions_checked=user1['terms_and_conditions_checked']
        )
        self.first_user.is_email_verified = True
        db.session.add(self.first_user)
        db.session.commit()

        auth_header = get_test_request_header(self.first_user.id, token_expiration_delta=timedelta(minutes=-7))
        expected_response = messages.TOKEN_HAS_EXPIRED
        actual_response = self.client.put(
            '/user/change_password', follow_redirects=True,
            headers=auth_header,
            data=json.dumps(dict(current_password=user1['password'],
                                 new_password="password")),
            content_type='application/json')

        self.assertEqual(401, actual_response.status_code)
        self.assertDictEqual(expected_response,
                             json.loads(actual_response.data))

if __name__ == "__main__":
    unittest.main()
