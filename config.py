#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 8:39
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : config.py
__metaclass__ = type
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PHOTOS_DEST=os.path.join(BASE_DIR, 'app','static','upload','photos')
DEFAULT_DEST = os.path.join(BASE_DIR, 'app', 'static', 'upload', 'default')
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY','hard to guess string')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_NATIVE_UNICODE = 'utf8'

    UPLOADED_PHOTOS_DEST = PHOTOS_DEST
    UPLOADED_DEFAULT_DEST = DEFAULT_DEST
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    @staticmethod
    def init_app():
        pass
#    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    if os.environ.get('MAIL_USE_SSL'):
        MAIL_USE_SSL = True
    else:
        MAIL_USE_TTL=True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DEV_DATABASE_URL')


class ProductionConfig(Config):
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    if os.environ.get('MAIL_USE_SSL'):
        MAIL_USE_SSL = True
    else:
        MAIL_USE_TTL=True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class SetupConfig:
    SECRET_KEY = 'None'
    DEBUG = True


config={
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'product': ProductionConfig,
    'default': ProductionConfig,
    'setup': SetupConfig
}
