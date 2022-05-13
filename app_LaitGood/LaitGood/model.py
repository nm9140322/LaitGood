
from app_LaitGood import db, bcrypt, mail, login, babel # import初始化過的套件
from flask_login import UserMixin # 多重繼承
from itsdangerous import URLSafeTimedSerializer # 產生驗證token
from flask import request, current_app, render_template # current_app類似定義user，但是直接連接目前的使用者
from threading import Thread # 寄信用的多線程
from flask_mail import Message
from jieba.analyse.analyzer import ChineseAnalyzer # 中文斷詞工具


# 記錄會員註冊的資料表
class UserRegister(UserMixin, db.Model):
    __tablename__ = 'LaitGood_UserRegister' # 資料表名稱
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(50), nullable=False) # 保存加密過後密碼
    registered_on = db.Column(db.DateTime, nullable=False) # 註冊日期
    confirm = db.Column(db.Boolean, default=False) # 記錄用戶是否已啟動驗證程序，預設為False
    confirmed_on = db.Column(db.DateTime, nullable=True) # 驗證通過日期
    roles = db.Column(db.Boolean, default=False) # 必須手動開通設定管理員身分

    # password利用裝飾器property變更屬性，在使用的時候實際上是hash並且賦值給予password_hash
    @property
    def password(self): # 禁止使用get來取得密碼
        raise AttributeError('password is not a readable attribute')
    @password.setter 
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf8')

    # 密碼驗證，確保輸入的密碼和資料庫的加密密碼相符
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'username:%s, email:%s' % (self.username, self.email)


    # 利用itsdangerou產生驗證用的token (URL)
    # URLSafeTimedSerializer在使用者註冊時得到的email地址生成一個token，實際上的email在token中被編碼
    # confirm_token()中用loads()方法，它接管token和過期時間：一個小時（3600秒）內有效
    # # 只要token沒過期就會返回一個email
    def create_confirm_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    
    def confirm_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
            )
        except:
            print ('驗證功能錯誤，請重新確認')
            return False
        return email

# 登入功能
@login.user_loader
def load_user(user_id):  
    return UserRegister.query.get(int(user_id))


# 寄信功能區
def send_async_email(app, msg):

    with app.app_context():
        mail.send(msg)
        print('寄信OK')

def send_mail(recipients, subject, template, mailtype, **kwargs):

    app = current_app._get_current_object()
    msg = Message(subject,
                recipients = recipients)
    if mailtype == 'html':
        msg.html = render_template(template + '.html', **kwargs)
    elif mailtype == 'txt':
        msg.body = render_template(template + '.txt', **kwargs)
    else:
        msg.body = template

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr  


# 中文站內搜索功能：
class Post(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['body', 'title']
    __analyzer__ = ChineseAnalyzer()

    id = db.Column(db.Integer, primary_key=True)

