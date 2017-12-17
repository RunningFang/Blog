#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 8:50
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : manage.py
__metaclass__ = type
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from app import create_app
from app.models import User,Article,Category
from app import db


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app,db)


def make_shell_context():
    return dict(app=app,User=User,Article=Article,Category=Category)


manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

if __name__=='__main__':
    manager.run()