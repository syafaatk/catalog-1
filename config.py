"""config.py.

Production and development mode configurations classes.
"""

import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEV_DATABASE = 'sqlite:///{db}'.format(db=os.path.join(BASE_DIR, 'flasca.db'))


class Config(object):
    WTF_CSRF_TIME_LIMIT = None


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = '4dcfce2628d096af824e343f0294315821d3cf82ffd3ee'
    SQLALCHEMY_DATABASE_URI = DEV_DATABASE
