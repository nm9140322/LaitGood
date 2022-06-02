# 執行並渲染網頁的view
# 記得還要連接後台系統

from . import news # blueprint，所有網址url_for都要加上前綴.web
from app_LaitGood import db # 從__init__.py 引入初始化的app
from flask import current_app, session, request, render_template,url_for,redirect, flash
# from app_LaitGood.LaitGood_news.model import 
from app_LaitGood.LaitGood_news.form import FormNews


# 資料庫操作
@news.route('/dbtable', methods=['GET', 'POST'])
def dbtable():   
    db.create_all() # 建置table
    return '建置資料庫註冊表'


# 最新消息頁，施工中
@news.route('/LaitGood_News')
def LaitGood_News():

    return render_template('LaitGood_news/News.html') 


