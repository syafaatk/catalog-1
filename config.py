"""config.py.

Production and development mode configurations classes.
"""

import os

from flask import request


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
DEV_DATABASE = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'catalog.db'))


class Config(object):
    UPLOADS_DEFAULT_DEST = BASE_DIR + '/usercontent/img/'
    UPLOADS_DEFAULT_URL = BASE_URL + '/usercontent/img/'
    UPLOADED_IMAGES_DEST = BASE_DIR + '/usercontent/img/'
    UPLOADED_IMAGES_URL = BASE_URL + '/usercontent/img/'
    WTF_CSRF_TIME_LIMIT = None


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = '4dcfce2628d096af824e343f0294315821d3cf82ffd3ee'
    SQLALCHEMY_DATABASE_URI = DEV_DATABASE
