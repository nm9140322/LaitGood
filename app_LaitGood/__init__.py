# 將LaitGoodProject內所有初始化設置於此(__init__.py)

from flask import Flask, request, session
from config import Config # 專案初始化的時候import參數，導入參數設置類別，渲染相關應用程式
from flask_sqlalchemy import SQLAlchemy # 資料庫
from flask_bcrypt import Bcrypt # 加密
from flask_mail import Mail # 寄信用的flask_mail的初始化 
from flask_login import LoginManager # flask_login的初始化
from flask_babelex import Babel, gettext # 翻譯用的flask_babel的初始化
# from flask_babel import Babel, gettext # 翻譯用的flask_babel的初始化
import flask_whooshalchemyplus # 站內搜尋的flask_whooshalchemyplus初始化
from flask_admin import Admin # 後台管理系統


# from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object(Config) # 渲染參數


db = SQLAlchemy(app) # 資料庫初始化
bcrypt = Bcrypt(app) # 加密用的flask_bcrypt的初始化
mail = Mail(app) # 寄信用的flask_mail的初始化 
login = LoginManager(app)  
login.login_view = 'LaitGoodmember_login' # 使用者登入功能所在的endpoint，通常為路由名稱
# 使用者尚未登入而試圖開啟網頁時且該路由有裝飾login_required的時候，就會將使用者引導至此。
login.login_message = gettext("請先登入再進行此操作")
flask_whooshalchemyplus.init_app(app)
admin = Admin(app, name='後台管理系統') # 初始後臺管理系統
babel = Babel(app) # 語系翻譯

# 使用者本地語系設置
# @babel.localeselector
# def get_locale():
#     return request.accept_languages.best_match(app.config['ALLOW_LANGUAGES'])

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang')


# bootstrap = Bootstrap(app)

# View的import一定要放後面，Python是個直述式語言，如果把View放在最上面去import會造成錯誤
# 原因是View內的相關物件這時候根本還沒有初始化生成，它無從import
import app_LaitGood.LaitGood.view
