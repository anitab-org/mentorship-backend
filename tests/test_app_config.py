import unittest
import os
from datetime import timedelta

from flask import current_app
from flask_testing import TestCase
from run import application


class TestTestingConfig(TestCase):
    def create_app(self):
        application.config.from_object("config.TestingConfig")

        secret_key = os.getenv("SECRET_KEY", None)
        application.config["SECRET_KEY"] = (
            secret_key if secret_key else "TEST_SECRET_KEY"
        )
        return application

    def test_app_testing_config(self):
        self.assertIsNotNone(application.config["SECRET_KEY"])
        self.assertTrue(application.config["DEBUG"])
        self.assertTrue(application.config["TESTING"])
        self.assertFalse(application.config["SQLALCHEMY_TRACK_MODIFICATIONS"])
        self.assertEqual(
            "sqlite://", application.config["SQLALCHEMY_DATABASE_URI"]
        )
        self.assertIsNotNone(current_app)

        # testing JWT configurations
        self.assertEqual(
            timedelta(weeks=1), application.config['JWT_ACCESS_TOKEN_EXPIRES']
        )
        self.assertEqual(
            timedelta(weeks=4), application.config['JWT_REFRESH_TOKEN_EXPIRES']
        )


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        application.config.from_object("config.DevelopmentConfig")

        secret_key = os.getenv("SECRET_KEY", None)
        application.config["SECRET_KEY"] = (
            secret_key if secret_key else "TEST_SECRET_KEY"
        )
        return application

    def test_app_development_config(self):
        self.assertIsNotNone(application.config["SECRET_KEY"])
        self.assertTrue(application.config["DEBUG"])
        self.assertFalse(application.config["TESTING"])
        self.assertFalse(application.config["SQLALCHEMY_TRACK_MODIFICATIONS"])
        self.assertEqual(
            "sqlite:///dev_data.db",
            application.config["SQLALCHEMY_DATABASE_URI"],
        )
        self.assertIsNotNone(current_app)

        # testing JWT configurations
        self.assertEqual(
            timedelta(weeks=1), application.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )
        self.assertEqual(
            timedelta(weeks=4), application.config["JWT_REFRESH_TOKEN_EXPIRES"]
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        application.config.from_object("config.ProductionConfig")

        secret_key = os.getenv("SECRET_KEY", None)
        application.config["SECRET_KEY"] = (
            secret_key if secret_key else "TEST_SECRET_KEY"
        )
        return application

    def test_app_production_config(self):
        self.assertIsNotNone(application.config["SECRET_KEY"])
        self.assertFalse(application.config["DEBUG"])
        self.assertFalse(application.config["TESTING"])
        self.assertFalse(application.config["SQLALCHEMY_TRACK_MODIFICATIONS"])
        self.assertEqual(
            "sqlite:///prod_data.db",
            application.config["SQLALCHEMY_DATABASE_URI"],
        )
        self.assertIsNotNone(current_app)

        # testing JWT configurations
        self.assertEqual(
            timedelta(weeks=1), application.config["JWT_ACCESS_TOKEN_EXPIRES"]
        )
        self.assertEqual(
            timedelta(weeks=4), application.config["JWT_REFRESH_TOKEN_EXPIRES"]
        )


if __name__ == "__main__":
    unittest.main()
