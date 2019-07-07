from datetime import timedelta
import os


class BaseConfig(object):
    """Base configuration."""
    DEBUG = False
    TESTING = False

    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 3600

    # Example:
    # MySQL: mysql+pymysql://{db_user}:{db_password}@{db_endpoint}/{db_name}
    # SQLite: sqlite:///local_data.db
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{db_user}:{db_password}@{db_endpoint}/{db_name}'
    # .format(db_user=os.getenv('DB_USERNAME'), db_password=os.getenv('DB_PASSWORD'))
    ENV_DB_USERNAME = os.getenv('DB_USERNAME')
    ENV_DB_PASSWORD = os.getenv('DB_PASSWORD')

    # Flask JWT settings
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(weeks=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    # if not SECRET_KEY:
    #     raise ValueError('You need to export SECRET_KEY set for Flask application')

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')

    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True

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

    @staticmethod
    def get_db_uri(db_user_arg, db_password_arg, db_endpoint_arg, db_name_arg):
        return 'mysql+pymysql://{db_user}:{db_password}@{db_endpoint}/{db_name}'\
            .format(db_user=db_user_arg,
                    db_password=db_password_arg,
                    db_endpoint=db_endpoint_arg,
                    db_name=db_name_arg)


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_db_uri(db_user_arg=BaseConfig.ENV_DB_USERNAME,
                                                    db_password_arg=BaseConfig.ENV_DB_PASSWORD,
                                                    db_endpoint_arg='something',
                                                    db_name_arg='systers-mentorship-production')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_db_uri(db_user_arg=BaseConfig.ENV_DB_USERNAME,
                                                    db_password_arg=BaseConfig.ENV_DB_PASSWORD,
                                                    db_endpoint_arg='something',
                                                    db_name_arg='systers-mentorship-development')


class StagingConfig(BaseConfig):
    """Staging configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = BaseConfig.get_db_uri(db_user_arg=BaseConfig.ENV_DB_USERNAME,
                                                    db_password_arg=BaseConfig.ENV_DB_PASSWORD,
                                                    db_endpoint_arg='systers-mentorship-staging.cq6nzcssjayz.eu-central-1.rds.amazonaws.com:3306/',
                                                    db_name_arg='systers-mentorship-staging')


class LocalConfig(BaseConfig):
    """Local configuration."""
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///local_data.db'


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True

    # Use in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


def get_env_config():
    flask_config_name = os.getenv('FLASK_ENVIRONMENT_CONFIG', 'dev')
    if flask_config_name not in ['prod', 'test', 'dev', 'local', 'stag']:
        raise ValueError('The environment config value has to be within these values: prod, dev, test.')
    return CONFIGURATION_MAPPER[flask_config_name]


CONFIGURATION_MAPPER = {
    'dev': 'config.DevelopmentConfig',
    'prod': 'config.ProductionConfig',
    'stag': 'config.StagingConfig',
    'local': 'config.LocalConfig',
    'test': 'config.TestingConfig'
}
