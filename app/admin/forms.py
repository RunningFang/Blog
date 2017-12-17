#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 21:59
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : forms.py
__metaclass__ = type
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,TextAreaField,SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Email, Regexp, EqualTo
from .. import photos
from flask_pagedown.fields import PageDownField

class PersonalInformationForm(FlaskForm):
    user_name = StringField(u"姓名", validators=[DataRequired(message=u'用户名不能为空'),\
                                                Regexp(u'[A-Za-z0-9_.\u4E00-\u9FFF]+',\
                                                message=u'只支持汉字，数字，字母，.和_')],
                                               render_kw = {'class': 'form-control','placeholder': u'请输入姓名'})
    email = StringField(u"邮箱", validators=[DataRequired(message=u'用户名不能为空'), Email()],
                        render_kw={'class': 'form-control', 'placeholder': u'请输入邮箱'})
    old_password=PasswordField(u"原密码", validators=[DataRequired(message=u'原密码不能为空')],
                                   render_kw={'class': 'form-control', 'placeholder': u'请输入原密码'}
                                   )
    password = PasswordField(u"密码", validators=[EqualTo('confirm_password',message="两次输入的新密码必须相同"),
                                                DataRequired(message=u'密码不能为空')],
                                    render_kw={'class': 'form-control', 'placeholder': u'请输入新密码'})
    confirm_password = PasswordField(u'确认密码', validators=[DataRequired(message=u'密码不能为空')],
                                     render_kw={'class': 'form-control', 'placeholder': u'请再次输入新原密码'})

    submit = SubmitField(u"确定", render_kw={'class':"btn btn-primary"})


class SettingForm(FlaskForm):
    title = StringField(u'标题',render_kw = {'class': 'form-control','placeholder': u'请输入站点名称'})
    second_title = StringField(u'副标题',render_kw = {'class': 'form-control','placeholder': u'请输入站点副标题'})
    keywords = StringField(u'关键字',render_kw = {'class': 'form-control','placeholder': u'请输入关键字'})
    description = StringField(u'站点描述',render_kw = {'class': 'form-control','placeholder': u'请输入站点描述'})
    icp_number = StringField(u'ICP备案号',render_kw = {'class': 'form-control','placeholder': u'请输入ICP备案号'})
    deposit = StringField(u'托管',render_kw = {'class': 'form-control','placeholder': u'请输入托管站点名'})
    icon = FileField(u'图标', validators=[FileAllowed(photos, u'只能上传图片！'), FileRequired(u'必须选择文件')],
                     render_kw = {'class': 'form-control','placeholder': u'请上传站点图标'})
    protocol=StringField(u'站长统计代码',render_kw = {'class': 'form-control','placeholder': u'请输入站长工具代码'})
    submit = SubmitField(u"确定", render_kw={'class': "btn btn-primary"})


class PersonalIntroduceForm(FlaskForm):
    name = StringField(u'姓名',render_kw = {'class': 'form-control'})
    image = FileField(u'头像',validators=[FileAllowed(photos, u'只能上传图片！'), FileRequired(u'必须选择文件')],
                     render_kw = {'class': 'form-control','placeholder': u'请上传个人头像'})
    introduction = TextAreaField(u'个人介绍',render_kw={'class':'form-control','placeholder': u'请输入个人描述'})
    submit = SubmitField(u"确定", render_kw={'class': "btn btn-primary"})

class ArticleForm(FlaskForm):
    title=StringField(u"标题",validators=[DataRequired('标题不能为空')])
    keys=StringField(u"关键字")
    description=StringField(u"描述")
    submit=SubmitField(u"提交")
