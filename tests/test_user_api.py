import unittest

TEST_DB = 'test.db'
LOCAL_ENDPOINT = 'http://localhost:5000'

class TestUserApi(unittest.TestCase):

    """
        Setup and teardown of test cases
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    """
        Tests
    """

    def test_main_page(self):
        #response = self.app.get('/', follow_redirects=True)
        #self.assertEqual(response.status_code, 200)
        self.assertTrue(True) # just to test that this is working

if __name__ == "__main__":
    unittest.main()
