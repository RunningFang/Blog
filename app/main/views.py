#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/1 9:24
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : views.py
__metaclass__ = type
from flask import render_template,url_for,request
from . import main
from ..models import Article, Category,Setting
from .. import db
from collections import OrderedDict


@main.route('/')
def index():
    page=request.args.get('page',1,type=int)
    setting=Setting.query.all()[0]
    pagination=Article.query.order_by(Article.timestamp.desc()).paginate(page,per_page=20,error_out=False)
    articles=pagination.items
    navbar=getNavbar()
    return render_template('main/index.html',articles=articles,pagination=pagination,navbar=navbar,setting=setting)


@main.route('/<name>/<article_id>',methods=['GET','POST'])
def article(name,article_id):
    article=Article.query.filter_by(id=article_id).first()
    setting = Setting.query.all()[0]
    navbar = getNavbar()
    breadcrumb=getBreadcrumb(article_id)
    return render_template('main/article.html',article=article,navbar=navbar,breadcrumb=breadcrumb,setting=setting)

def getBreadcrumb(article_id):
    first_category_id=Article.query.filter_by(id=article_id).all()[0].first_category_id
    second_category_id=Article.query.filter_by(id=article_id).all()[0].second_category_id
    first_category=Category.query.filter_by(id=first_category_id).all()[0]
    second_category = Category.query.filter_by(id=second_category_id).all()
    if second_category!=[]:
        second_category=second_category[0]
        return [first_category,second_category]
    else:
        return [first_category]

@main.route('/artilce/<name>',methods=['GET','POST'])
def list(name):
    page = request.args.get('page', 1, type=int)
    category_id=Category.query.filter_by(url_name=name).all()[0].id
    if Category.query.filter_by(id=category_id).all()[0].father_node==0:
        pagination=Article.query.filter_by(first_category_id=category_id).order_by(Article.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    else:
        pagination = Article.query.filter_by(second_category_id=category_id).order_by(Article.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    articles = pagination.items
    navbar = getNavbar()
    setting = Setting.query.all()[0]
    return render_template('main/index.html',articles=articles,pagination=pagination,navbar=navbar,setting=setting)



def getNavbar():
    categories=OrderedDict()
    for father_node in Category.query.filter_by(father_node='0').order_by(db.asc(Category.id)).all():
        child_nodes=[]
        if Category.query.filter_by(father_node=father_node.id).all()!=[]:
            for ca in Category.query.filter_by(father_node=father_node.id).all():
                child_nodes.append(ca)
        categories[father_node]=child_nodes
    return categories