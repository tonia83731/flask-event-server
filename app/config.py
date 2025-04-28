import os
from datetime import timedelta
from dotenv import load_dotenv

env = os.getenv('FLASK_ENV', 'development')

# if env == 'development':
#     load_dotenv(".env/.env.dev")
# elif env == 'production':
#     load_dotenv(".env/.env.prod")
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

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DEBUG = True

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
    DEBUG=True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')

app_config = {
    'testing': TestingConfig,
    'development': DevConfig,
    'production': ProdConfig
}