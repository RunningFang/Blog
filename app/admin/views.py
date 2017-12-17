#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/4 22:03
# @Author  : fangjie
# @email   : 838379742@qq.com
# @File    : views.py
from datetime import datetime

__metaclass__ = type

from flask import render_template, redirect, url_for,request, jsonify
from flask_login import login_required,login_user,logout_user,current_user
from jinja2 import Markup
from ConfigParser import ConfigParser

from app.tools import SetPersonalIntroduction
from forms import  PersonalIntroduceForm
from . import admin
from ..models import User, Category, Article, Setting
from .. import db,photos
from config import BASE_DIR,PHOTOS_DEST
from collections import OrderedDict
import os
import time
import hashlib
import json

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and user.verify_password(request.form.get('password')):
            login_user(user,True)
            return jsonify(result=1, url='/admin/article')
        else:
            return jsonify(result=0, url='/admin/login')
    return render_template("admin/login.html")



@admin.route('/login_out',methods=['GET','POST'])
@login_required
def login_out():
    logout_user()
    return redirect(url_for('admin.login'))


@admin.route('/edit_personal_information',methods=['GET','POST'])
@login_required
def edit_personal_information():
    if request.method == "POST":
        user = User.query.filter_by(email=current_user.email).first()
        if user is not None and user.verify_password(request.form.get('old_password')):
            user=User.query.filter_by(email=current_user.email).first()
            user.user_name=request.form.get('user_name')
            user.password=request.form.get('password')
            db.session.commit()
            return redirect(url_for('admin.login_out'))
        else:
            return redirect(url_for('admin.login_out'))
    return render_template('admin/edit_personal_information.html',user=current_user)


@admin.route('/article', methods=['GET','POST'])
@login_required
def article():
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.timestamp.desc()).paginate(page, per_page=20, error_out=False)
    articles=[]
    for article in pagination.items:
        if Category.query.filter_by(id=article.second_category_id).all()!=[]:
            article.second_category = Category.query.filter_by(id=article.second_category_id).all()
        else:
            article.second_category=[]
        articles.append(article)
    return render_template("admin/article.html",articles=articles,pagination=pagination)

@admin.route('/upload',methods=['POST'])
@login_required
def upload():
    file_hash = hashlib.md5('admin' + str(time.time())).hexdigest()[:15]

    file_hash=file_hash+"."+request.files.get('editormd-image-file').filename.split('.')[1]
    request.files.get('editormd-image-file').filename=file_hash
    filename=photos.save(request.files.get('editormd-image-file'))
    file_url=photos.url(filename)

    data = {'success': 1,'message' : "上传成功",'url': file_url}
    return json.dumps(data)




@admin.route('/add_article', methods=['GET','POST'])
@login_required
def add_article():
    categories=getCategories()
    if request.method=='POST':
        article=Article(title=request.form.get('title'),
                        first_category_id=request.form.get('select_one'),
                        second_category_id=request.form.get('select_two'),
                        auther_id = current_user.id,
                        timestamp = datetime.utcnow(),
                        keywords=request.form.get('keywords'),
                        description=request.form.get('description'),
                        body = request.form.get('body'))
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('admin.article'))
    return render_template("admin/add_article.html",categories=categories)

def getCategories():
    categories=OrderedDict()
    for father_node in Category.query.filter_by(father_node='0').all():
        child_nodes=[]
        if Category.query.filter_by(father_node=father_node.id).all()!=[]:
            for ca in Category.query.filter_by(father_node=father_node.id).all():
                child_nodes.append(ca)
        categories[father_node]=child_nodes
    return categories



@admin.route('/update_article/<id>', methods=['GET','POST'])
@login_required
def update_article(id):

    article=Article.query.filter_by(id=int(id)).first()
    categories = getCategories()
    if request.method=='POST':
        article.title = request.form.get('title')
        article.first_category_id = int(request.form.get('select_one'))
        article.second_category_id = request.form.get('select_two')
        article.auther_id = current_user.id
        article.timestamp = datetime.utcnow()
        article.keywords = request.form.get('keywords')
        article.description = request.form.get('description')
        article.body = request.form.get('body')
        db.session.commit()
        return redirect(url_for('admin.article'))
    return render_template("admin/update_article.html", categories=categories,article=article)


@admin.route('/delete_article/<id>', methods=['GET','POST'])
@login_required
def delete_article(id):
    article=Article.query.filter_by(id=int(id)).first()
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('admin.article'))








@admin.route('/category', methods=['GET','POST'])
@login_required
def category():
    choices=[('0','无')]
    for category in Category.query.filter_by(father_node=0).all():
        choices.append((str(category.id),category.show_name))
    if request.method=='POST':
        if request.form.get('id')=='0':
            addCategory(request)
        else:
            updateCategory(request)
        return redirect(url_for('admin.category'))
    if request.args.get('type')=='del':
        deleteCategory(request.args.get('id'))
        return redirect(url_for('admin.category'))
    categoryTable=getCategory()
    return render_template("admin/category.html",choices=choices,categoryTable=categoryTable)


def deleteCategory(id):
    category=Category.query.filter_by(id=int(id)).first()
    for child in Category.query.filter_by(father_node=id).all():
        db.session.delete(child)
        db.session.commit()
    db.session.delete(category)
    db.session.commit()


def getCategory():
    return Category.query.all()


def addCategory(request):
    category = Category(url_name=request.form.get('url_name'), show_name=request.form.get('show_name'),
                        father_node=request.form.get('father_node'))
    db.session.add(category)
    db.session.commit()


def updateCategory(request):
    category=Category.query.filter_by(id=int(request.form.get('id'))).first()
    category.url_name=request.form.get('url_name')
    category.show_name=request.form.get('show_name')
    category.father_node=request.form.get('father_node')
    db.session.commit()


@admin.route('/setting', methods=['GET','POST'])
@login_required
def setting():
    setting=Setting.query.all()
    if request.method=='POST':
        if setting==[]:
            setting=Setting(title=request.form.get('title'),
            keywords=request.form.get('keywords'),
            description=request.form.get('description'),
            icp_number=request.form.get('icp_number'),
            deposit=request.form.get('deposit'),
            protocol=request.form.get('protocol'))
            db.session.add(setting)
        else:
            setting = setting[0]
            setting.title=request.form.get('title')
            setting.keywords=request.form.get('keywords')
            setting.description=request.form.get('description')
            setting.icp_number=request.form.get('icp_number')
            setting.deposit=request.form.get('deposit')
            setting.protocol=request.form.get('protocol')
        if os.path.isfile(os.path.join(PHOTOS_DEST,'favicon.ico')):
            os.remove(os.path.join(PHOTOS_DEST,'favicon.ico'))
        photos.save(request.files.get('icon'),name='favicon.ico')
        db.session.commit()
        return render_template("admin/setting.html",setting=setting)
    return render_template("admin/setting.html",setting=setting)












@admin.route('/about_me', methods=['GET','POST'])
@login_required
def about_me():
    personalIntroduceForm=PersonalIntroduceForm()
    if personalIntroduceForm.validate_on_submit():
        update_about_me(personalIntroduceForm)
    return render_template("admin/about_me.html",form=personalIntroduceForm,telValue=getTelHTML(),techValue=getTechHTML(),telNumValue=getTelNum(),techNumValue=getTechNum())


def getTechHTML():
    tech=[]
    config=ConfigParser()
    config.read(os.path.join(BASE_DIR ,'PersonalIntroduction.conf'))
    techNum=config.get('tech','techNum')
    for i in range(1,int(techNum)+1):
        techName,techProportion=config.items('tech')[i]
        tech.append(Markup(
                  '<li class="li-side">' \
                    '<label>技能名：</label>' \
                  '</li>'\
                  '<li class="li-side">' \
                    '<input type="text" id="techName' + str(i) + '" value="'+techName+'" name="techName' + str(i) + '">' \
                  '</li>'\
                  '<li class="li-side">' \
                    '<label>技能值：</label>' \
                  '</li>'\
                  '<li class="li-side">' \
                    '<input type="range" style="width: 100px;" value="'+techProportion+'" onchange="checkField(this.id)" id="techProportion' + str(i) + '" name="techProportion' + str(i) + '">' \
                  '</li>'\
                  '<li class="li-side">' \
                    '<label id="techProportionValue' + str(i) + '">'+techProportion+'</label></li>'\
                    '<li class="li-side"><input id = "' + str(i) + '" type="button" onclick="delTech(this.id);" value="-" /></li>'
        ))
    return tech

def getTelHTML():
    tel=[]
    config = ConfigParser()
    config.read(os.path.join(BASE_DIR, 'PersonalIntroduction.conf'))
    telNum = config.get('tel', 'telNum')
    for i in range(1,int(telNum)+1):
        telName, telValue = config.items('tel')[i]
        tel.append(Markup(
            '<li class="li-side">' \
                '<label>联系方式类型：</label>' \
            '</li>'\
            '<li class="li-side">' \
                '<input type="text" value="'+telName+'" name="telName' + str(i) + '">' \
            '</li>'\
            '<li class="li-side">' \
                '<label>联系方式值：</label>' \
            '</li>'\
            '<li class="li-side">' \
                '<input type="text" value="'+telValue+'" name="telValue' + str(i) + '" style="width: 100px;">' \
            '</li>'\
            '<li class="li-side"><input id = "'+str(i)+'" type="button" onclick="delTel(this.id);" value="-" />' \
            '</li>'))
    return tel

def getTelNum():
    config=ConfigParser()
    config.read(os.path.join(BASE_DIR ,'PersonalIntroduction.conf'))
    return config.get('tel','telNum')

def getTechNum():
    config = ConfigParser()
    config.read(os.path.join(BASE_DIR, 'PersonalIntroduction.conf'))
    return config.get('tech', 'techNum')

def update_about_me(personalIntroduceForm):
    name=personalIntroduceForm.name.data
    image=personalIntroduceForm.image.data
    introduction=personalIntroduceForm.introduction.data
    techNum=request.form['techNum']
    telNum = request.form['telNum']
    tel={}
    tech={}
    for i in range(int(techNum)+1):
        techName = request.form['techName'+str(i)]
        techProportion = request.form['techProportion'+str(i)]
        tech[techName] = techProportion
    for i in range(int(telNum)+1):
        telName = request.form['telName' + str(i)]
        telValue = request.form['telValue' + str(i)]
        tel[telName] = telValue

    file_hash = hashlib.md5('admin' + str(time.time())).hexdigest()[:15]
    file_hash=file_hash+"."+personalIntroduceForm.image.data.filename.split('.')[1]
    personalIntroduceForm.image.data.filename=file_hash
    filename=photos.save(personalIntroduceForm.image.data)
    file_url=photos.url(filename)
    config=ConfigParser()
    config=SetPersonalIntroduction.setNormal(config,name,introduction)
    config=SetPersonalIntroduction.setImage(config,file_url)
    config=SetPersonalIntroduction.setTech(config,tech,techNum)
    config=SetPersonalIntroduction.setTel(config,tel,telNum)

    with open(os.path.join(BASE_DIR ,'PersonalIntroduction.conf'),'w') as config_file:
        config.write(config_file)



