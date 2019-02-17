import os

from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config(object):
	""" Base Configuration """
	DEBUG = False
	TESTING = False
	JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

class ProductionConfig(Config):
    """ Configuration for production environment"""
    DEBUG = False


class StagingConfig(Config):
    """ Configuration for devlopment environment"""
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Configuration for development environment
    """
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(Config):
    """ Configuration for testing environment"""
    DEBUG = True
    TESTING = True


config_obj = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
