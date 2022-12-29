# 隨機生成資安防護用的金鑰：
# import os
# print (os.urandom(24))

import os 
from datetime import timedelta

# SQLite資料庫連線
pjdir = os.path.abspath(os.path.dirname(__file__))
def create_sqlite_uri(db_name):
    return "sqlite:///" + os.path.join(pjdir, db_name)


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False # True會追蹤各種改變的信號而消耗額外的記憶體
    SECRET_KEY = '\t>\xf2;\x89\x9d4e\xd1\x89\x8c\x9e\xf9>\xd02"2i.\x83\xf7\x97\x84' # 金鑰
    # WTF_CSRF_SECRET_KEY = os.urandom(24) # CSRF金鑰，沒有特別設定就是預設直接共用SECRET_KEY
    
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

    # GOOGLE登入功能
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None) # 終端機設置 $env:GOOGLE_CLIENT_ID = "YOUR GOOGLE_CLIENT_ID"

    # 檔案上傳功能，『DEF』來自實作UploadSet的參數 (__init__.py)
    UPLOADED_DEF_DEST = './app_LaitGood/static/image_upload' # 檔案上傳放置路徑
    UPLOADED_DEF_URL = '/static/image_upload/' # 調用文件時的連結

class DevelopmentConfig(BaseConfig): # 開發環境
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('app_LaitGood\\static\\database\\laitgood_register.sqlite')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') 
    # 終端機設置 $env:DATABASE_URI = "mysql+pymysql://帳號:密碼@localhost:3306/laitgood_db" # MySQL
    # 終端機設置 $env:DATABASE_URI = "postgres://HEROKU的API" # HEROKU部署-pg
    
class TestingConfig(BaseConfig): # 測試環境
    TESTING = True
    WTF_CSRF_ENABLED = False # flask-wtf 用 csrf_token處理 CSRF 的攻擊，測試時不會像正常使用一樣實際按下送出，而是直接傳資料到後端會被 csrf_token 擋下來，所以要關掉。  
    # SQLALCHEMY_DATABASE_URI = create_sqlite_uri('app_LaitGood\\static\\database\\test_laitgood_register.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') 
    

class ProductionConfig(BaseConfig): # 正式環境
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_DATABASE_URI = create_sqlite_uri('app_LaitGood\\static\\database\\official_laitgood_register.sqlite')

# 環境配置更換時
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}