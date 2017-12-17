#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 8:00
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : __init__.py
__metaclass__ = type

from flask import Blueprint
main = Blueprint('main', __name__)

from . import views, forms

from ..SelfBlogConfig import SelfBlogConfig


@main.app_context_processor
def inject_selfblogconfig():
    return dict(SelfBlogConfig=SelfBlogConfig)

