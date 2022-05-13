# 隨機生成資安防護用的金鑰：
# import os
# print (os.urandom(24))


import os 
from datetime import timedelta

class Config:
    # 資料庫連線(練習先用SQLite擋，有空再來慢慢改成MySQL)
    pjdir = os.path.abspath(os.path.dirname(__file__))
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                            os.path.join(pjdir, 'app_LaitGood\\static\\database\\laitgood_register.sqlite')
    SECRET_KEY = '\t>\xf2;\x89\x9d4e\xd1\x89\x8c\x9e\xf9>\xd02"2i.\x83\xf7\x97\x84' # 金鑰
    
    # 寄信STMP
    # os.environ.get用來取得環境變數，避免敏感資訊置於公開場合 (github)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587 # 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # 終端機設置 $env:MAIL_USERNAME = "YOUR MAIL COUNT"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 終端機設置 $env:MAIL_PASSWORD = "YOUR MAIL PASSWORD"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME # 可以省略sender設置

    # 註冊驗證用的token
    SECURITY_PASSWORD_SALT = '\x98"V\xb4\xc5\xa2K\xe9\xbb*\xca\xc7/\xcf7\xec\x9c\xcd\xb4u\xe3H\x14\xac' # salt為密碼學用語，會在重新編碼的過程中再加入此設定的東東，建議用user的註冊帳號做變化，不要用固定的

    # 登入功能中對session的安全等級設置
    SESSION_PROTECTION = 'strong'

    # 記得我功能期限，預設為365天
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    # 多國語系功能
    BABEL_DEFAULT_LOCALE = 'zh_TW'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    ALLOW_LANGUAGES = ['zh_TW', 'en']
    

