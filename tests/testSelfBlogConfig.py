#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 9:19
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : testSelfBlogConfig.py
__metaclass__ = type

import unittest
from app.SelfBlogConfig import SelfBlogConfig


class TestSelfBlogConfig(unittest.TestCase):

    def testTitle(self):
        self.assertTrue(SelfBlogConfig.title)

    def testKeyWords(self):
        self.assertTrue(SelfBlogConfig.keywords)

    def testDescription(self):
        self.assertTrue(SelfBlogConfig.description)

