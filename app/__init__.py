#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 7:59
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : __init__.py
import jinja2

__metaclass__ = type
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from config import config
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_uploads import UploadSet, configure_uploads, patch_request_class
bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
pagedown=PageDown()

ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','ico')

login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='admin.login'

photos = UploadSet('photos', ALLOWED_EXTENSIONS)


def create_app(config_name):
    if(config_name == 'setup'):
        app = create_setup_app(config_name)
    else:
        app = create_normal_app(config_name)
    return app


def create_normal_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app()

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    configure_uploads(app, photos)
    patch_request_class(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    return app


def create_setup_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)

    from app.setup import setup as setup_blueprint
    app.register_blueprint(setup_blueprint)
    return app
