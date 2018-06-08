import unittest
from datetime import timedelta

from flask import current_app
from flask_testing import TestCase
from run import application


class TestTestingConfig(TestCase):
    def create_app(self):
        application.config.from_object('config.TestingConfig')
        return application

    def test_app_testing_config(self):
        self.assertEqual(application.config['SECRET_KEY'], 'EXAMPLE_SECRET_KEY')
        self.assertTrue(application.config['DEBUG'])
        self.assertTrue(application.config['TESTING'])
        self.assertFalse(application.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(application.config['SQLALCHEMY_DATABASE_URI'], 'sqlite://')
        self.assertFalse(current_app is None)

        # testing JWT configurations
        self.assertTrue(application.config['JWT_AUTH_URL_RULE'] == '/login')
        self.assertEqual(application.config['JWT_EXPIRATION_DELTA'], timedelta(weeks=1))


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        application.config.from_object('config.DevelopmentConfig')
        return application

    def test_app_development_config(self):
        self.assertEqual(application.config['SECRET_KEY'], 'EXAMPLE_SECRET_KEY')
        self.assertTrue(application.config['DEBUG'])
        self.assertFalse(application.config['TESTING'])
        self.assertFalse(application.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(application.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///dev_data.db')
        self.assertFalse(current_app is None)

        # testing JWT configurations
        self.assertEqual(application.config['JWT_AUTH_URL_RULE'], '/login')
        self.assertEqual(application.config['JWT_EXPIRATION_DELTA'], timedelta(weeks=1))


class TestProductionConfig(TestCase):
    def create_app(self):
        application.config.from_object('config.ProductionConfig')
        return application

    def test_app_production_config(self):
        self.assertEqual(application.config['SECRET_KEY'], 'EXAMPLE_SECRET_KEY')
        self.assertFalse(application.config['DEBUG'])
        self.assertFalse(application.config['TESTING'])
        self.assertFalse(application.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(application.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///prod_data.db')
        self.assertFalse(current_app is None)

        # testing JWT configurations
        self.assertTrue(application.config['JWT_AUTH_URL_RULE'] == '/login')
        self.assertEqual(application.config['JWT_EXPIRATION_DELTA'], timedelta(weeks=1))


if __name__ == '__main__':
    unittest.main()
