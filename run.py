#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 8:50
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : run.py
__metaclass__ = type

from app import create_app,db
import os
from config import BASE_DIR
from app.models import User,Article,Category,Setting,Tag
import pickle

def check_setup():
    if os.path.isfile(os.path.join(BASE_DIR,'user.conf')):
        db.create_all()
        with open(os.path.join(BASE_DIR,'user.conf'),'r') as filename:
            user=pickle.loads(filename.read())
        db.session.add(user)
        db.session.commit()
        os.remove(os.path.join(BASE_DIR,'user.conf'))

if __name__ == '__main__':
    if os.environ.get('MAIL_SERVER') is None:
        config_name='setup'
    else:
        config_name='default'
    app = create_app(config_name)
    with app.app_context():
        check_setup()

    app.run()
