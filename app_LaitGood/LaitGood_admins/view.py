# 執行並渲染網頁的view
from . import admins # blueprint，所有網址都會加上前綴/admins
from app_LaitGood import db, admin # 從__init__.py 引入初始化的app
from flask import request, render_template,url_for,redirect, flash
from app_LaitGood.LaitGood_member.model import UserRegister # 從model.py引入資料表
from app_LaitGood.LaitGood_admins.form import AdminLoginForm # 從form.py引入表格
from flask_login import current_user, login_user, logout_user # 登入功能
from flask_admin import BaseView, expose # 後臺管理
from flask_admin.contrib.sqla import ModelView # 後臺管理


# 資料庫操作
@admins.route('/dbtable', methods=['GET', 'POST'])
def dbtable():   
    db.create_all() # 建置table
    return '建置資料庫註冊表'

# 後台功能區：
# 後台登入頁面
@admins.route('/LaitGood_adminlogin', methods=['GET', 'POST'])
def LaitGood_adminlogin():
    form =  AdminLoginForm()
    if form.validate_on_submit():
        adminuser = UserRegister.query.filter_by(username=form.adminlogin.data).first()
        if adminuser:
            if adminuser.check_password(form.adminpassword.data):
                if adminuser.roles == True:
                    login_user(adminuser)
                    return redirect(url_for('admin.index'))
                else:
                    flash('此帳號不符合管理員權限。')
            else:
                flash('輸入密碼有誤，請重新確認。')
        else:
            flash('輸入帳號有誤，請重新確認。')   
                
    return render_template('LaitGood_admins/admin_login.html', form=form)

# 後台登出
class adminlogout(BaseView):
    def is_accessible(self): # 未登入看不到
        if current_user.is_authenticated:
            adminuser =  UserRegister.query.filter_by(username=current_user.username).first()
            if adminuser.roles == True:
                return current_user.is_authenticated
            else:
                flash('此帳號不符合管理員權限，請先登出並改以管理員身分重新登入。')
                return  False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        flash('請先以管理員身分登入！')
        return redirect(url_for('admins.LaitGood_adminlogin', next=request.url))

    @expose('/')  
    def adminlogout(self):
        logout_user()
        flash('已從後台管理系統登出！')
        return redirect(url_for('admins.LaitGood_adminlogin'))

# 渲染後台自訂登出頁面
admin.add_view(adminlogout(name='登出')) 


# 後台管理-會員資料
class UserView(ModelView):
    def is_accessible(self): # 未登入看不到
        if current_user.is_authenticated:
            adminuser =  UserRegister.query.filter_by(username=current_user.username).first()
            if adminuser.roles == True:
                return current_user.is_authenticated
            else:
                return  False
        else:
            return False

    def inaccessible_callback(self, name, **kwargs): # 未登入不得進入
        flash('請先以管理員身分登入！')     
        return redirect(url_for('admins.LaitGood_adminlogin', next=request.url))

    # 定義管理員是否可以進行刪除增改，預設為True
    can_delete = True
    can_edit = True
    can_create = False
    can_view_details = True # 可以看到所有欄位的完整內容
    
    # 改成彈出式視窗進行新增修改
    # create_modal = True
    # edit_modal = True

    # 自訂義column欄位名
    column_labels = dict(username='會員帳號', 
                        email='註冊信箱', 
                        registered_on='註冊日期', 
                        confirm='帳號驗證', 
                        confirmed_on='驗證日期'
                        )

    # 如果不想顯示特定爛位，可以遮蔽
    column_exclude_list = ['password_hash']

    # 設定為可搜尋的關鍵字及篩選項目
    column_searchable_list = ['username', 'email']
    column_filters = ['confirm']

    # 設定為可直接修改的欄位
    # column_editable_list = ['username']

# 渲染後台管理db的頁面
admin.add_view(UserView(UserRegister, db.session, url='/LaitGood_member/',name='會員資訊', category='會員管理'))


# 後台管理-最新消息

