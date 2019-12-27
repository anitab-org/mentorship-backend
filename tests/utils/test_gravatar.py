import unittest

from libgravatar import Gravatar


class TestGravatar(unittest.TestCase):

    def test_works(self):
        valid_photo_url = "http://www.gravatar.com/avatar/b642b4217b34b1e8d3bd915fc65c4452?size=512"

        gravatar = Gravatar("test@test.com")
        photo_url = gravatar.get_image(size=512)

        self.assertEqual(valid_photo_url, photo_url)


if __name__ == '__main__':
    unittest.main()
