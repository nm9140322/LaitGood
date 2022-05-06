# wtform建立各種需要的Form

from flask_wtf import FlaskForm # Flask表單
from wtforms import StringField, SubmitField, validators, PasswordField, EmailField, ValidationError, BooleanField
from app_LaitGood.LaitGood.model import UserRegister # 寫入使用者註冊資料前需要驗證email與username是否已被使用，從app_pack中Member資料夾裡的model.py引入UserReister (model)
from flask_babel import lazy_gettext

# 註冊用的form
class FormRegister(FlaskForm):
    username = StringField(lazy_gettext('會員帳號'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('中英文皆可')}, validators=[
        validators.DataRequired(),
    ])
    email = EmailField(lazy_gettext('信  箱'), render_kw={'class':'searchtext', 'placeholder':  lazy_gettext('請輸入有效註冊信箱')}, validators=[
        validators.DataRequired(),
        validators.Length(1, 50)
    ])
    password = PasswordField(lazy_gettext('密  碼'), render_kw={'class':'searchtext', 'placeholder':  lazy_gettext('請同時包含英文及數字')}, validators=[
        validators.DataRequired(),
        validators.Length(5, 10),  
        validators.Regexp('\d.*[a-zA-Z]|[a-zA-Z].*\d', message=lazy_gettext('密碼請同時包含英文及數字'))     
    ])
    password2 = PasswordField(lazy_gettext('確認密碼'), render_kw={'class':'searchtext'}, validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message=lazy_gettext('密碼輸入有誤')) # 驗證兩次輸入的密碼是否相同，避免使用者輸入錯誤
    ])

    agreecheck = BooleanField(lazy_gettext('按下註冊鈕的同時，表示您已詳閱我們的資料使用政策與使用條款，同意使用 LaitGood 所提供的服務並訂閱電子報。'), default=True)
    
    submit = SubmitField(lazy_gettext('註冊會員'), render_kw={'class':'btn_login'})

    # 驗證註冊郵件存在與否
    def validate_email(self, field): # 自定義的驗證在命名規則上為validate_欄位
        if UserRegister.query.filter_by(email=field.data).first(): # 驗證郵件是否已存在資料庫內
            raise ValidationError(lazy_gettext('此信箱已被註冊，請重新輸入')) # 報告驗證錯誤

# 登入 (以email為主要登入帳號)
class FormLogin(FlaskForm):
    email = EmailField(lazy_gettext('信  箱'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的註冊信箱')}, validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email() # 需要安裝額外套件：pip install wtforms[email]
    ])

    password = PasswordField(lazy_gettext('密  碼'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請同時包含英文及數字')}, validators=[
        validators.DataRequired()
    ])

    confirm_num = StringField(lazy_gettext('驗證碼'), render_kw={'class':'searchtext', 'id':'input-val', 'placeholder': lazy_gettext('點圖可更換驗證碼（大小寫不拘）')}, validators=[
        validators.DataRequired(),
    ])

    remember_me = BooleanField(lazy_gettext('記住我'), default=True) # 記得我功能，預設為勾選

    submit = SubmitField(lazy_gettext('登入'), render_kw={'class':'btn_login'})

# 密碼變更
class FormChangePWD(FlaskForm):
    #  驗證舊密碼
    password_old = PasswordField(lazy_gettext('舊密碼'), validators=[
        validators.DataRequired()
    ])
    #  新密碼
    password_new = PasswordField(lazy_gettext('新密碼'), validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.Regexp('\d.*[a-zA-Z]|[a-zA-Z].*\d', message=lazy_gettext('密碼請同時包含英文及數字'))
    ])
    #  新密碼確認
    password_new_confirm = PasswordField(lazy_gettext('新密碼確認'), validators=[
        validators.DataRequired(),
        validators.EqualTo('password_new', message=lazy_gettext('密碼輸入有誤'))
    ])
    submit = SubmitField(lazy_gettext('更換密碼'), render_kw={'class':'btn_login'})

# 忘記密碼 (輸入信箱後才可以重設)
class FormResetPasswordMail(FlaskForm):
    email = EmailField(lazy_gettext('信  箱'), render_kw={'class':'searchtext', 'placeholder': lazy_gettext('請輸入您的註冊信箱')}, validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])
    submit = SubmitField(lazy_gettext('信箱驗證'), render_kw={'class':'btn_login'})

    # 驗證EMAIL在資料庫內，若沒有就不寄信
    def validate_email(self, field):
        if not UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError(lazy_gettext('此信箱未曾註冊，請重新確認。'))

#  重置密碼
class FormResetPassword(FlaskForm):
    password = PasswordField(lazy_gettext('重設密碼'), validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.Regexp('\d.*[a-zA-Z]|[a-zA-Z].*\d', message=lazy_gettext('密碼請同時包含英文及數字'))
        
    ])
    password_confirm = PasswordField(lazy_gettext('密碼確認'), validators=[
        validators.DataRequired(),
        validators.EqualTo('password', message=lazy_gettext('密碼輸入有誤'))
    ])
    submit = SubmitField(lazy_gettext('重設密碼'), render_kw={'class':'btn_login'})