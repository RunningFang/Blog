#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 15:17
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : __init__.py
__metaclass__ = type
from flask import Blueprint
setup = Blueprint('setup', __name__)
from . import forms,views
