from decouple import config

class Config:
    SECRET_KEY = config('APP_SECRET_KEY')
    TIMEZONE = config('APP_TIMEZONE')
    PROPAGATE_EXCEPTIONS = False

    # API
    API_TITLE = 'My API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.2'

    # DATABASE
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=config('PGSQL_USER'),
        password=config('PGSQL_PASSWORD'),
        host=config('PGSQL_HOST'),
        port=config('PGSQL_PORT'),
        database=config('PGSQL_DATABASE')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig
}