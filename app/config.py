import os
from datetime import timedelta
from dotenv import load_dotenv

env = os.getenv('FLASK_ENV', 'development')

if env == 'development':
    load_dotenv(".env.dev")
elif env == 'production':
    load_dotenv(".env.prod")

# docker need to include flask db init, include .env.prod

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_BLACKLIST_ENABLED=True
    JWT_TOKEN_LOCATION='headers'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')

    REGISTER_SCRET_KEY=os.getenv('REGISTER_SCRET_KEY')

    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    DEBUG=True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')

    REGISTER_SCRET_KEY=os.getenv('REGISTER_SCRET_KEY')

    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')

app_config = {
    'testing': TestingConfig,
    'development': DevConfig,
    'production': ProdConfig
}