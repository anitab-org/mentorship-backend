import unittest

from tests.base_test_case import BaseTestCase


class TestFlaskApp(BaseTestCase):
    def test_index(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertTrue(response.status_code == 200)


if __name__ == "__main__":
    unittest.main()
