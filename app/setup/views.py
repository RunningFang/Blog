#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 15:14
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : views.py


__metaclass__ = type
from ..tools import SetProfile
from flask import render_template,flash
from forms import SetupForm
from . import setup
from ..models import User
import os
import pickle
from config import BASE_DIR


@setup.route('/', methods=['GET','POST'])
def setup():
    setupForm = SetupForm()
    if setupForm.validate_on_submit():
        set_config(setupForm)
        add_user(setupForm)
        install_config()
        flash(u'请重启您的操作系统，并重新运行程序')
        return render_template('setup/setup.html', form=setupForm, flag=1)
    return render_template('setup/setup.html',form=setupForm)



def set_config(setupForm):
    set_mysql(setupForm)
    set_secret_key(setupForm)
    set_mail_server(setupForm)
    set_mail_port(setupForm)
    set_mail_use_protocol(setupForm)
    set_mail_username(setupForm)
    set_mail_password(setupForm)


def install_config():
    if SetProfile.get_system_name() == "Windows":
        url=os.path.abspath('app/scripts/blog.bat')
        os.system(url)

def add_user(setupForm):
    user = User(email=setupForm.email.data,
                password=setupForm.password.data,
                user_name=setupForm.user_name.data)
    user_pickle = pickle.dumps(user)
    with open(os.path.join(BASE_DIR, 'user.conf'),'w') as filename:
        filename.write(user_pickle)


def set_mysql(setupForm):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://"+setupForm.mysql_username.data+":"\
                            +setupForm.mysql_password.data+"@localhost/blog"
    command,filename = SetProfile.profile('SQLALCHEMY_DATABASE_URI', SQLALCHEMY_DATABASE_URI)
    SetProfile.write_file(command,filename,)

def set_secret_key(setupForm):
    SECRET_KEY = setupForm.secret_key.data
    command, filename = SetProfile.profile('SECRET_KEY', SECRET_KEY)
    SetProfile.write_file(command, filename)

def set_mail_server(setupForm):
    MAIL_SERVER = setupForm.mail_server.data
    command, filename = SetProfile.profile('MAIL_SERVER', MAIL_SERVER)
    SetProfile.write_file(command, filename)

def set_mail_port(setupForm):
    MAIL_PORT = setupForm.mail_port.data
    command, filename = SetProfile.profile('MAIL_PORT', MAIL_PORT)
    SetProfile.write_file(command, filename)

def set_mail_use_protocol(setupForm):
    protocal_name = setupForm.mail_use_protocol.data
    if protocal_name == 'tls':
        command, filename = SetProfile.profile('MAIL_USE_TLS', 'True')
    elif protocal_name == 'ssl':
        command, filename = SetProfile.profile('MAIL_USE_SSL', 'True')
    SetProfile.write_file(command, filename)

def set_mail_username(setupForm):
    MAIL_USERNAME = setupForm.mail_username.data
    command, filename = SetProfile.profile('MAIL_USERNAME', MAIL_USERNAME)
    SetProfile.write_file(command, filename)

def set_mail_password(setupForm):
    MAIL_PASSWORD = setupForm.mail_password.data
    command, filename = SetProfile.profile('MAIL_PASSWORD', MAIL_PASSWORD)
    SetProfile.write_file(command, filename)