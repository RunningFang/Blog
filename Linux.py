#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 22:00
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : Linux.py
__metaclass__ = type
import os
with open('/etc/profile.d/blog.sh','a') as file:
    file.write('export JA=/var/mysoft/jdk1.7.0_80\n')
os.system('chmod 755 /etc/profile.d/blog.sh')