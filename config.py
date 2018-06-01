

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'EXAMPLE_SECRET_KEY'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_data.db'


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_data.db'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test_data.db'
