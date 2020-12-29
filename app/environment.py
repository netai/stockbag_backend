import os

basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig():
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../stock.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig():
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../stock.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig():
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../stock.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

env = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)