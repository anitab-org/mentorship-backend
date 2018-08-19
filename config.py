from datetime import timedelta
import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=1)

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    # if not SECRET_KEY:
    #     raise ValueError('You need to export SECRET_KEY set for Flask application')

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    # TODO put this in dev only?

    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # email authentication
    MAIL_USERNAME = os.getenv('APP_MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('APP_MAIL_PASSWORD')

    # mail accounts
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


class ProductionConfig(BaseConfig):
    ENV = 'production'

    # SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_data.db'


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_data.db'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'certain@example.com'


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
