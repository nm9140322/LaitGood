# 將LaitGoodProject內所有初始化設置於此(__init__.py)

from flask import Flask, request, session
from config import config # 參數設置
from flask_sqlalchemy import SQLAlchemy # 資料庫
from flask_bcrypt import Bcrypt # 加密
from flask_mail import Mail # 寄信用的flask_mail的初始化 
from flask_login import LoginManager # flask_login的初始化
from flask_babelex import Babel, gettext # 翻譯用的flask_babel的初始化
# import flask_whooshalchemyplus # 站內搜尋的flask_whooshalchemyplus初始化
from flask_admin import Admin # 後台管理系統
from flask_migrate import Migrate # 資料庫搬移
from flask_uploads import UploadSet, IMAGES, configure_uploads # 檔案上傳功能
from flask_wtf.csrf import CSRFProtect # CSRF token，解決來源信任的問題

db = SQLAlchemy()
mail = Mail() 
bcrypt = Bcrypt() 
admin = Admin(name='後台管理系統')
babel = Babel()
login = LoginManager()
migrate = Migrate()
upload = UploadSet(name='def', extensions=IMAGES)
csrf = CSRFProtect()

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name]) # 渲染參數

    db.init_app(app) # 資料庫
    mail.init_app(app) # 寄信
    bcrypt.init_app(app) # 加密
    admin.init_app(app) # 後台
    babel.init_app(app) # 翻譯
    migrate.init_app(app, db) # 資料庫搬移
    # flask_whooshalchemyplus.init_app(app) # 關鍵字搜尋
    configure_uploads(app, upload) # 圖檔上傳
    csrf.init_app(app) # csrf

    # 登入相關：
    login.init_app(app) 
    login.login_view = 'member.LaitGoodmember_login' # 路由有裝飾login_required時導向此
    login.login_message = gettext("請先登入再進行此操作")


    # Blueprint_member
    from app_LaitGood.LaitGood_member import member
    app.register_blueprint(member, url_prefix='/member') # 網址前綴/member
    # Blueprint_web    
    from app_LaitGood.LaitGood_web import web
    app.register_blueprint(web)
    # Blueprint_cart
    from app_LaitGood.LaitGood_cart import cart
    app.register_blueprint(cart)
    # Blueprint_admins
    from app_LaitGood.LaitGood_admins import admins
    app.register_blueprint(admins, url_prefix='/admins') # 網址前綴/admins

    return app


# 本地語系設置
@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang')
