# import unittest
# from tests.base_test_case import BaseTestCase
# from app.database.models.user import UserModel


# Testing User API resources
#
# TODO tests:
#     - authenticate when User table does not exist
#     - Users GET/POST/PUT/DELETE
#     - Check admin and non admin actions

# class TestUserApi(BaseTestCase):

    # Tests

    # def test_user_registration(self):
    #     # Ensure user registration behaves correctly.
    #
    #     response = self.client.post('/register', data=dict(
    #         name='Testing User',
    #         username='test_user',
    #         password='test_user',
    #         email='test@user.com',
    #         terms_and_conditions_checked=True
    #     ), follow_redirects=True)
    #
    #     print(response)
    #     user = UserModel.query.filter_by(email='test@user.com').first()
    #     if user is None:
    #         self.fail('POST /register failed to register Testing User! with error code = %d' % response.status_code)
    #     else:
    #         self.assertTrue(user.name == 'Testing User')
    #         self.assertTrue(user.username == 'test_user')
    #         self.assertTrue(user.email == 'test@user.com')
    #         self.assertFalse(user.is_admin)

    # def test_list_users_api_resource(self):
    #
    #     response = self.client.get('/users', follow_redirects=True)
    #     self.assertTrue(response.status_code == 201)



# if __name__ == "__main__":
#     unittest.main()
