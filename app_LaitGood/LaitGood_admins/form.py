# wtform建立各種需要的Form
from app_LaitGood import upload
from flask_wtf import FlaskForm # Flask表單
from wtforms import StringField, SubmitField, validators, PasswordField, DateField, TextAreaField, IntegerField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_babelex import lazy_gettext
import datetime

# 後台系統管理者登入
class AdminLoginForm(FlaskForm):

    adminlogin = StringField(lazy_gettext('管理員帳號'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入管理者帳號')}, validators=[validators.DataRequired()])

    adminpassword = PasswordField(lazy_gettext('管理員密碼'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入管理者密碼')}, validators=[validators.DataRequired()])
    
    submit = SubmitField(lazy_gettext('登入後台'), render_kw={'class':'btn_login'})

# 最新消息上傳表單
class NewsUploadForm(FlaskForm):
    imgbtn_uploads = FileField('選擇圖檔*', render_kw={'class':'btn_login'}, validators=[
    FileAllowed(upload, '請上傳圖檔'), # 只允許照片，第一個參數是UploadSet的物件名稱
    FileRequired('請上傳封面圖') # 必需有照片
    ])
    title =  StringField(lazy_gettext('消息標題*'), render_kw={'class':'searchtext'}, validators=[validators.DataRequired()])
    slogan =  StringField(lazy_gettext('消息重點'), render_kw={'class':'searchtext'})
    content = TextAreaField(lazy_gettext('詳細內容'), render_kw={'class':'searchtext'})
    newsdate = DateField(lazy_gettext('消息日期'), default=datetime.date.today, render_kw={'class':'searchtext'}, validators=[validators.DataRequired()])
    submit = SubmitField(lazy_gettext('消息上傳'), render_kw={'class':'btn_login'})

# 好評推薦上傳表單
class commendsUploadForm(FlaskForm):
    imgbtn_uploads = FileField('選擇圖檔*', render_kw={'class':'btn_login'}, validators=[
    FileAllowed(upload, '請上傳圖檔'), # 只允許照片，第一個參數是UploadSet的物件名稱
    FileRequired('請上傳封面圖') # 必需有照片
    ])
    title =  StringField(lazy_gettext('推薦標題*'), render_kw={'class':'searchtext'}, validators=[validators.DataRequired()])
    slogan =  StringField(lazy_gettext('推薦重點'), render_kw={'class':'searchtext'})
    url = StringField(lazy_gettext('連結網址'), render_kw={'class':'searchtext'}, validators=[validators.DataRequired()])
    submit = SubmitField(lazy_gettext('推薦內容上傳'), render_kw={'class':'btn_login'})


# 線上購物+產品販售頁表單
class ProductUploadForm(FlaskForm):
    imgbtn_uploads = FileField('選擇圖檔*', render_kw={'class':'btn_login'}, validators=[
    FileAllowed(upload, '請上傳圖檔'), # 只允許照片，第一個參數是UploadSet的物件名稱
    FileRequired('請上傳封面圖') # 必需有照片
    ])
    product_name =  StringField(lazy_gettext('產品名*'), render_kw={'class':'searchtext'}, validators=[validators.DataRequired()])
    product_package =  StringField(lazy_gettext('包裝規格'), render_kw={'class':'searchtext'})
    product_price = IntegerField(lazy_gettext('定價*'), render_kw={'class':'searchtext'}, validators=[validators.DataRequired(), validators.NumberRange(min=0)])
    product_sellprice = IntegerField(lazy_gettext('售價'), render_kw={'class':'searchtext'}, validators=[validators.Optional(), validators.NumberRange(min=0)])
    product_intro = TextAreaField(lazy_gettext('產品說明'), render_kw={'class':'searchtext'})
    submit = SubmitField(lazy_gettext('產品上傳'), render_kw={'class':'btn_login'})

# 訂單出貨表單
class OrderDeliverForm(FlaskForm):
    order_number = StringField(lazy_gettext('訂單編號*'), render_kw={'class':'searchtext'}, validators=[validators.DataRequired()])
    submit = SubmitField(lazy_gettext('產品出貨'), render_kw={'class':'btn_login'})