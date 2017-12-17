#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 7:58
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : models.py
__metaclass__ = type
from . import db
from datetime import datetime
from werkzeug import security
from flask_login import UserMixin
from . import login_manager
import bleach
from markdown import markdown


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True,index=True)
    first_category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    second_category_id=db.Column(db.Integer)
    auther_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    visit_number = db.Column(db.Integer)
    comment_number = db.Column(db.Integer)
    loves_number = db.Column(db.Integer)
    share_number = db.Column(db.Integer)
    title=db.Column(db.TEXT)
    body = db.Column(db.TEXT)
    keywords=db.Column(db.TEXT)
    description=db.Column(db.TEXT)

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py
        seed()
        u=User.query.offset(0).first()
        for i in range(count):
            a=Article(title=forgery_py.lorem_ipsum.title(randint(1,3)),body=forgery_py.lorem_ipsum.sentences(randint(1,3)),timestamp=forgery_py.date.date(True),author=u)
            db.session.add(a)
            db.session.commit()

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True,index=True)
    user_name=db.Column(db.String(64))
    password_hash = db.Column(db.String(256))
    blogs = db.relationship('Article', backref='author', lazy='dynamic')

    @property
    def password(self):
        return AttributeError(u'密码不是一个可读属性')

    @password.setter
    def password(self,password):
        self.password_hash=security.generate_password_hash(password)

    def verify_password(self,password):
        return security.check_password_hash(self.password_hash,password)



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, index=True)
    url_name = db.Column(db.String(64), unique=True, index=True)
    show_name = db.Column(db.String(64))
    father_node = db.Column(db.Integer)
    blogs = db.relationship('Article',backref='first_category',lazy='dynamic')


class Tag(db.Model):
    __tablename__='tags'
    name = db.Column(db.String(64),primary_key=True)
    number = db.Column(db.Integer)


class Setting(db.Model):
    __tablename__='setting'
    title = db.Column(db.String(64),primary_key=True)
    keywords = db.Column(db.TEXT())
    description = db.Column(db.TEXT())
    icp_number = db.Column(db.String(64))
    deposit = db.Column(db.String(64))
    protocol = db.Column(db.TEXT())

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))