import app.run
import unittest

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_api_root_status_code(self):
        # sends HTTP GET request the root of the API
        result = self.app.get('/')

        # assert the status code of the response
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()
