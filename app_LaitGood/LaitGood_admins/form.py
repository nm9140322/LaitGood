# wtform建立各種需要的Form

from flask_wtf import FlaskForm # Flask表單
from wtforms import StringField, SubmitField, validators, PasswordField
from flask_babelex import lazy_gettext

# 後台系統管理者登入
class AdminLoginForm(FlaskForm):

    adminlogin = StringField(lazy_gettext('管理員帳號'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入管理者帳號')}, validators=[validators.DataRequired()])

    adminpassword = PasswordField(lazy_gettext('管理員密碼'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入管理者密碼')}, validators=[validators.DataRequired()])
    
    submit = SubmitField(lazy_gettext('登入後台'), render_kw={'class':'btn_login'})

