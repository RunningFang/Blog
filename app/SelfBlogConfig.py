#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 8:56
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : SelfBlogConfig.py
__metaclass__ = type
from config import BASE_DIR
from jinja2 import Markup
import ConfigParser
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SelfBlogConfig:
    config=ConfigParser.ConfigParser()
    config.read(os.path.join(BASE_DIR,'SelfBlogConfig.conf'))
    if config.has_option('global', 'title'):
        title = config.get('global','title')
    if config.has_option('global', 'keywords'):
        keywords = config.get('global','keywords')
    if config.has_option('global', 'description'):
        description = config.get('global','description')
    if config.has_option('global','icp_number'):
        icp_number = config.get('global','icp_number')
    if config.has_option('global', 'deposit'):
        deposit = config.get('global','deposit')
    if config.has_option('global', 'protocol'):
        protocol= config.get('global','protocol')
        protocol = Markup(protocol)


if __name__=='__main__':
    print SelfBlogConfig.title
    print SelfBlogConfig.keywords
    print SelfBlogConfig.description
