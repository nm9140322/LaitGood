# wtform建立最新消息需要的Form
from flask_babelex import lazy_gettext
from flask_wtf import FlaskForm # Flask表單
from wtforms import StringField, SubmitField, IntegerField, EmailField, SelectField, validators

class ShoppingForm(FlaskForm):
    product_amount = IntegerField(lazy_gettext('數量'), default=1, render_kw={'class':'searchtext'}, validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    submit = SubmitField(lazy_gettext('加入購物車'), render_kw={'class':'btn_login'})

class OrderPayForm(FlaskForm):
    username = StringField(lazy_gettext('訂購人*'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('英/數')}, validators=[
        validators.DataRequired(),
        ])
    email = EmailField(lazy_gettext('聯絡信箱*'), render_kw={'class':'searchtext', 'placeholder':  lazy_gettext('請輸入有效註冊信箱')}, validators=[
        validators.DataRequired(),
        validators.Length(1, 50)
        ])
    cellphone = StringField(lazy_gettext('手機號碼*'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的手機號碼')}, validators=[
        validators.DataRequired(),
        validators.Optional(),
        validators.Regexp("^[0][9][0-9]{8}$", message=lazy_gettext("手機格式不符"))
    ])
    phone = StringField(lazy_gettext('聯絡電話'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的電話號碼')}, validators=[
        validators.Optional(),
        validators.Regexp("(\d{2,3}-?|\(\d{2,3}\))\d{3,4}-?\d{4}", message=lazy_gettext("電話號碼格式不符"))
    ])
    address = StringField(lazy_gettext('聯絡地址*'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的聯絡地址')}, validators=[
        validators.DataRequired()
        ])
    pay_method = SelectField(lazy_gettext('付款方式*'), choices=[('cash','到貨付款'),('ecpay','線上付款')])
    submit = SubmitField(lazy_gettext('確認購買'), render_kw={'class':'btn_login'})