import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
class CeleryDevelopmentConfig():
    TESTING = False
    WTF_CSRF_ENABLED = False


class CeleryTestingConfig():
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
