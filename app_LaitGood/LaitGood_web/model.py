
from app_LaitGood import db, mail # import初始化過的套件
from jieba.analyse.analyzer import ChineseAnalyzer # 中文斷詞工具
from flask_mail import Message
from threading import Thread # 寄信用的多線程
from flask import current_app, render_template 

# 中文站內搜索功能：
class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['body', 'title']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.Integer, primary_key=True)


# 聯絡我們寄信區：
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
        print('聯絡我們寄信OK')

def contact_sendmail(subject, recipients, template, **kwargs):    
    app = current_app._get_current_object()
    msg = Message(subject,
                recipients = recipients)
    msg.html = render_template(template + '.html', **kwargs)

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr  

# 最新消息資料表：圖片檔、標題、重點、內文、日期
class Newsdata(db.Model):
    __tablename__='LaitGood_Newsdata'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    slogan = db.Column(db.String(80))
    content = db.Column(db.String(80))
    newsdate = db.Column(db.Date, nullable=False)

    def __init__(self, image, title, slogan, content, newsdate ):
        self.image = image
        self.title = title
        self.slogan = slogan
        self.content = content
        self.newsdate  = newsdate 

    def __repr__(self):
        return 'title:%s, newsdate:%s' % (self.title, self.newsdate)


# 好評推薦資料表：圖片檔、標題、重點、連結網址
class commends_data(db.Model):
    __tablename__='LaitGood_commends_data'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    slogan = db.Column(db.String(80))
    url = db.Column(db.String(80), nullable=False)

    def __init__(self, image, title, slogan, url):
        self.image = image
        self.title = title
        self.slogan = slogan
        self.url  = url

    def __repr__(self):
        return 'title:%s, url:%s' % (self.title, self.url)


