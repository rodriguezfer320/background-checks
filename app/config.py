from decouple import config

class Config:
    # Set Flask config variables
    FLASK_ENV = config('APP_ENV')
    SECRET_KEY = config('APP_SECRET_KEY')
    DEBUG = config('APP_DEBUG')
    SERVER_NAME = config('APP_SERVER_NAME')
    TIMEZONE = config('APP_TIMEZONE')