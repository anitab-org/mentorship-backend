from datetime import timedelta
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv('SECRET_KEY')

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask JWT settings
    JWT_AUTH_URL_RULE = '/login'
    JWT_EXPIRATION_DELTA = timedelta(weeks=1)


class ProductionConfig(BaseConfig):
    ENV = 'production'

    # SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_data.db'


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_data.db'


class TestingConfig(BaseConfig):
    ENV = 'testing'
    DEBUG = True
    TESTING = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test_data.db'


def get_env_config():
    flask_config_name = os.getenv('FLASK_ENVIRONMENT_CONFIG', 'dev')
    if flask_config_name not in ['prod', 'test', 'dev']:
        raise ValueError('The environment config value has to be within these values: prod, dev, test.')
    return CONFIGURATION_MAPPER[flask_config_name]


CONFIGURATION_MAPPER = {
    'dev': 'config.DevelopmentConfig',
    'test': 'config.TestingConfig',
    'prod': 'config.ProductionConfig'
}
