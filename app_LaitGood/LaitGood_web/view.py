# 執行並渲染網頁的view

from . import web # blueprint，所有網址url_for都要加上前綴.web
from app_LaitGood import db # 從__init__.py 引入初始化的app
from flask import current_app, session, request, render_template,url_for,redirect, flash
from app_LaitGood.LaitGood_web.model import Post, contact_sendmail # 從model.py引入資料表
from app_LaitGood.LaitGood_web.form import FormContactus
from flask_login import login_required # 登入功能
from flask_babelex import refresh # 語系翻譯
import flask_whooshalchemyplus # 站內搜索


# 資料庫操作
@web.route('/dbtable', methods=['GET', 'POST'])
def dbtable():   
    db.create_all() # 建置table
    return '建置資料庫註冊表'

# 登入頁面 (測試用)
@web.route('/', methods=['GET', 'POST'])
def manager_login():
    if (request.method == 'POST'):
        username=request.form.get('username')
        if (username == 'gu'): #guest
            return redirect(url_for('web.LaitGood')) # 進入首頁
        elif (username == 'ad'): # admin
            return redirect(url_for('admins.LaitGood_adminlogin')) # 進入後台登入
        else:
            flash("帳號錯誤，請重新輸入！")  # 閃現訊息   
            return redirect(url_for('web.manager_login'))

    return render_template('LaitGood_web/manager_login.html') #  將HTML5的程式碼放在另一個檔案裡，藉由flask提供的函式render_template()去讀取

# 日果首頁
@web.route('/LaitGood', methods=['GET', 'POST']) # 利用利用jinja模板語法直接繼承基礎模板做出的首頁例子
def LaitGood():
    refresh()     
    return render_template('LaitGood_web/LaitGood.html') 

# 中文語系設置    
@web.route('/LaitGood_zh', methods=['GET', 'POST'])
def LaitGood_zh():    
    session['lang'] = 'zh_TW'
    refresh()
    return redirect(url_for('web.LaitGood'))
# 英文語系設置    
@web.route('/LaitGood_en', methods=['GET', 'POST'])
def LaitGood_en():
    session['lang'] = 'en'
    refresh()
    return redirect(url_for('web.LaitGood'))

# 站內關鍵字搜尋區，待修
@web.route('/search', methods = ['POST', 'GET'])
def search():
    if not request.form['search']:
        return redirect(url_for('web.LaitGood'))
    return redirect(url_for('.search_results', query = request.form['search']))

@web.route('/search_results/<query>')
def search_results(query):
    flask_whooshalchemyplus.whoosh_index(current_app, Post) 
    results = Post.query.whoosh_search(query).all()
    return render_template('LaitGood_web/search_results.html', query = query, results = results)


# 線上購物頁，待修
@web.route('/LaitGood_shop')
@login_required
def LaitGood_shop():

    return render_template('LaitGood_web/shopping.html') 

# 關於我們/品牌故事頁
@web.route('/LaitGood_Aboutus')
def LaitGood_Aboutus():

    return render_template('LaitGood_web/Aboutus.html') 

# 品質保證頁
@web.route('/LaitGood_QC')
def LaitGood_QC():

    return render_template('LaitGood_web/QC.html') 


# 聯絡我們頁
@web.route('/LaitGood_Contactus', methods=['GET', 'POST'])
def LaitGood_Contactus():
    form = FormContactus()
    #  寄出聯絡信件
    if form.validate_on_submit():
        contact_sendmail(
                subject='日果使用者來信聯絡',
                template='LaitGood_web/mail/contactus_mail',
                recipients = [current_app.config['MAIL_USERNAME']],
                form=form)
        flash('感謝您的來信，我們將盡快回覆您。')              
        return render_template('flashmessage.html')
    return render_template('LaitGood_web/Contactus.html', form=form) 

