
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

