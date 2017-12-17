#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 15:14
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : forms.py
__metaclass__ = type
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField
from wtforms.validators import DataRequired, Email, Regexp, EqualTo,Length



class SetupForm(FlaskForm):
    user_name = StringField(u"姓名", validators=[DataRequired(message=u'用户名不能为空'), \
                                              Regexp(u'[A-Za-z0-9._\u4E00-\u9FFF]+', \
                                                     message=u'只支持汉字，数字，字母，.和_'), \
                                              Length(min=1, max=64)])
    email = StringField(u"邮箱", validators=[Email(message=u'邮箱格式不对'),
                                                DataRequired(message=u'邮箱不能为空'),\
                                                Length(min=1, max=64)])
    password = PasswordField(u"后台登录密码", validators=[EqualTo('confirm_password'),
                                                DataRequired(message=u'密码不能为空')])
    confirm_password = PasswordField(u'确认密码', validators=[DataRequired(message=u'密码不能为空')])

    mysql_username = StringField(u"mysql用户名", validators=[DataRequired(message=u'数据库用户名不能为空')])
    mysql_password = PasswordField(u"mysql密码", validators=[DataRequired(message=u'数据库密码不能为空')])

    secret_key = StringField(u"安全密钥", validators=[DataRequired(message=u'数据库用户名不能为空')])
    mail_server = StringField(u"邮件服务器", validators=[DataRequired(message=u'数据库用户名不能为空')])
    mail_port = StringField(u"邮件服务器端口", validators=[DataRequired(message=u'数据库用户名不能为空')])
    mail_use_protocol = SelectField(u"邮箱协议", choices=[('tls', 'TLS'),('ssl','SSL')],\
                                            validators=[DataRequired(message=u'数据库用户名不能为空')])
    mail_username = StringField(u"邮箱账号", validators=[DataRequired(message=u'数据库用户名不能为空')])
    mail_password = PasswordField(u'邮箱密码', validators=[DataRequired(message=u'密码不能为空')])

    submit = SubmitField(u"确定")