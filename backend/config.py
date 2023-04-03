from decouple import config

class Config:
    SECRET_KEY = config('APP_SECRET_KEY')
    TIMEZONE = config('APP_TIMEZONE')

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig
}