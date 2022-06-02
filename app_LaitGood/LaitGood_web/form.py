# wtform建立各種需要的Form

from flask_wtf import FlaskForm # Flask表單
from wtforms import StringField, SubmitField, validators, EmailField, TextAreaField
from flask_babelex import lazy_gettext


# 聯絡我們表單區
class FormContactus(FlaskForm):
    username = StringField(lazy_gettext('姓  名'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的姓名')}, validators=[
        validators.DataRequired(),
    ])
    email = EmailField(lazy_gettext('信  箱'), render_kw={'class':'searchtext', 'placeholder':  lazy_gettext('請輸入您的聯絡信箱')}, validators=[
        validators.DataRequired(),
        validators.Length(1, 50)
    ])
    phone = StringField(lazy_gettext('聯絡電話'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的手機號碼')}, validators=[
        validators.DataRequired(),
        validators.Regexp("^[0][9][0-9]{8}$", message=lazy_gettext("手機格式不符"))
    ])
    comment = TextAreaField(lazy_gettext('備  註'), render_kw={'class':'searchtext', 'placeholder':  lazy_gettext('如有任何疑問，歡迎來信詢問')}, validators=[
        validators.DataRequired()
    ])
    submit = SubmitField(lazy_gettext('提  交'), render_kw={'class':'btn_login'})
