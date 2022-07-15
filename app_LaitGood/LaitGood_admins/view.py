# 執行並渲染網頁的view
from . import admins # blueprint，所有網址都會加上前綴/admins
from app_LaitGood import db, admin, upload # 從__init__.py 引入初始化的app
from flask import request, render_template,url_for,redirect, flash
from app_LaitGood.LaitGood_member.model import UserRegister
from app_LaitGood.LaitGood_cart.model import Shoppingdata, order_number, order_pay, Transaction, cart_sendmail
from app_LaitGood.LaitGood_web.model import Newsdata, commends_data
from app_LaitGood.LaitGood_admins.model import SaleActivity
from app_LaitGood.LaitGood_admins.form import AdminLoginForm, NewsUploadForm, commendsUploadForm, ProductUploadForm, OrderDeliverForm
from flask_login import current_user, login_user, logout_user # 登入功能
from flask_admin import BaseView, expose # 後臺管理
from flask_admin.contrib.sqla import ModelView  # 後臺管理


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
                        confirmed_on='驗證日期',
                        roles='管理者',
                        agreecheck='電子報',
                        birthday='生日',
                        gender='性別',
                        cellphone='手機',
                        phone='電話',
                        zipcode='郵遞區號',
                        county='縣市',
                        district='地區',
                        address='地址',
                        )

    # 如果不想顯示特定爛位，可以遮蔽
    column_exclude_list = ['password_hash']

    # 設定為可搜尋的關鍵字及篩選項目
    column_searchable_list = ['id', 'username', 'email']
    column_filters = ['confirm']

    # 設定為可直接就地修改的欄位
    column_editable_list = ['agreecheck']
    
    # 設定編輯欄位
    form_columns = ['username', 'roles', 'agreecheck']

    # 設定不給新增/編輯的欄位
    # form_excluded_columns = ['password_hash']

    # 設定修改選項
    form_choices = {
        'gender': [
            ('Male', '男性'),
            ('Female', '女性'),
            ('Other', '其他')
        ]}

# 渲染後台管理db的頁面
admin.add_view(UserView(UserRegister, db.session, url='/LaitGood_member/',name='會員資訊', category='會員管理'))

# 後台管理-會員訂單管理
class UserOrderView(ModelView):
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
    
    # 自訂義column欄位名
    column_labels = dict(order_number='訂單編號', 
                        order_date='訂購日期', 
                        order_paymethod='付款狀況', 
                        order_deliver='出貨狀況',
                        order_finish='訂單完成',
                        member='訂購會員',
                        pay='訂購資訊'
                        )

    # 設定為可搜尋的關鍵字及篩選項目
    column_searchable_list = ['order_number']
    column_filters = ['order_deliver', 'order_finish', 'order_date', 'order_number']

    # 設定為可直接就地修改的欄位
    column_editable_list = ['order_finish']

    # 設定編輯欄位
    form_columns = ['order_paymethod','order_deliver', 'order_finish']

    # 設定修改選項 到貨付款/尚未付款/已付款
    form_choices = {
        'order_paymethod': [
            ('到貨付款', '到貨付款'),
            ('尚未付款', '尚未付款'),
            ('已付款', '已付款')
        ]}

# 渲染後台管理db的頁面
admin.add_view(UserOrderView(order_number, db.session, url='/LaitGood_member/order_number',name='訂單管理', category='會員管理'))

# 後台管理-訂單購買資訊管理
class UserOrderPayView(ModelView):
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
    can_delete = False
    can_edit = False
    can_create = False
    can_view_details = True # 可以看到所有欄位的完整內容
    
    # 自訂義column欄位名
    column_labels = dict(username='購買人', 
                        email='聯絡信箱', 
                        cellphone='手機號碼', 
                        phone='聯絡電話',
                        zipcode='郵遞區號',
                        district='縣市',
                        county='地區',
                        address='地址',
                        pay_price='訂單總額',
                        pay_method='付款方式'
                        )

    # 設定為可搜尋的關鍵字及篩選項目
    column_searchable_list = ['pay_id', 'username']
    column_filters = ['username', 'pay_method']

    # 設定不給新增/編輯的欄位
    form_excluded_columns = ['pay_price', 'db_pay_ordernum']

    # 設定修改選項
    form_choices = {
        'pay_method': [
            ('cash', '到貨付款'),
            ('ecpay', '線上付款')
        ]}

# 渲染後台管理db的頁面
admin.add_view(UserOrderPayView(order_pay, db.session, url='/LaitGood_member/order_pay',name='訂購資訊', category='會員管理'))

# 後台管理-線上交易編號
class ECpayTransaction(ModelView):
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
    can_delete = False
    can_edit = False
    can_create = False
    can_view_details = True # 可以看到所有欄位的完整內容

    # 自訂義column欄位名
    column_labels = dict(trade_num='交易編號', 
                        total_price='交易金額', 
                        status='交易狀態',
                        ordernum='訂單資訊'
                        )
    

# 渲染後台管理db的頁面
admin.add_view(ECpayTransaction(Transaction, db.session, url='/Transaction/',name='線上交易', category='會員管理'))

# 後台管理-訂單出貨
class OrderDeliver(BaseView):
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
    
    @expose('/', methods=['GET','POST'])
    def OrderDeliverSendMail(self):
        deliverform =  OrderDeliverForm()

        if deliverform.validate_on_submit():
            ordernumber = deliverform.order_number.data # 訂單編號
            orderdeliver = order_number.query.filter_by(order_number=ordernumber).first()
            # 寄信通知會員產品出貨
            cart_sendmail(
                subject='您訂購的日果產品已出貨',
                template='LaitGood_admins/mail/orderdeliver_mail',
                recipients = [orderdeliver.pay.email],
                orderdeliver=orderdeliver
                )
            # 改訂單的出貨狀態
            orderdeliver.order_deliver = True
            db.session.commit()
            print('訂單編號', orderdeliver.order_number,'出貨狀況改為「已出貨」')
            flash('訂單編號：%s，出貨狀態改為「已出貨」並寄信通知客戶囉！' % (orderdeliver.order_number))
        
        return self.render('LaitGood_admins/admin_deliversendmail.html', form = deliverform)

admin.add_view(OrderDeliver(name='訂單出貨', category='會員管理', url='/OrderDeliverSendMail/'))

# 後台管理-管理最新消息
class NewsContent(ModelView):
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
    create_modal = False
    edit_modal = True

    # 自訂義column欄位名
    column_labels = dict(image='封面圖檔', 
                        title='消息標題', 
                        slogan='消息重點', 
                        content='詳細內容', 
                        newsdate='消息日期'
                        )

# 渲染後台管理db的頁面
admin.add_view(NewsContent(Newsdata, db.session, url='/LaitGood_news/',name='消息列表', category='最新消息'))

# 後台管理-上傳最新消息
class Newsupload(BaseView):
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
    
    @expose('/', methods=['GET','POST']) # /Newsupload/
    def Newsupload(self):
        newsform = NewsUploadForm()

        if newsform.validate_on_submit():
            file_name = upload.save(newsform.imgbtn_uploads.data)
            file_url = upload.url(file_name)
            print('成功上傳圖檔：' + file_name,'；圖檔路徑：'+ file_url)
            news =  Newsdata(
                image = file_url,
                title = newsform.title.data,
                slogan= newsform.slogan.data, 
                content= newsform.content.data, 
                newsdate= newsform.newsdate.data
            )
            db.session.add(news)
            db.session.commit()

            flash('已成功上傳此消息，若需刪改請至消息列表進行管理。')
            return redirect(url_for('newsupload.Newsupload', newsform=newsform, file_url=file_url))   

        else:
            file_url=None

        return self.render('LaitGood_admins/admin_newsupload.html', newsform=newsform, file_url = file_url)

admin.add_view(Newsupload(name='消息上傳', category='最新消息', url='/Newsupload/'))


# 後台管理-管理好評推薦
class commendsContent(ModelView):
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
    create_modal = False
    edit_modal = True

    # 自訂義column欄位名
    column_labels = dict(image='封面圖檔', 
                        title='推薦標題', 
                        slogan='推薦重點', 
                        url='連結網址'
                        )

# 渲染後台管理db的頁面
admin.add_view(commendsContent(commends_data, db.session, url='/LaitGood_commends/',name='推薦列表', category='好評推薦'))

# 後台管理-上傳好評推薦
class commendsupload(BaseView):
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

    @expose('/', methods=['GET','POST'])
    def commendsupload(self):
        commendsform = commendsUploadForm()

        if commendsform.validate_on_submit():
            file_name = upload.save(commendsform.imgbtn_uploads.data)
            file_url = upload.url(file_name)
            print('成功上傳圖檔：' + file_name,'；圖檔路徑：'+ file_url)
            commends =  commends_data(
                image = file_url,
                title = commendsform.title.data,
                slogan= commendsform.slogan.data, 
                url= commendsform.url.data
            )
            db.session.add(commends)
            db.session.commit()

            flash('已成功上傳此消息，若需刪改請至推薦列表進行管理。')
            return redirect(url_for('commendsupload.commendsupload', commendsform=commendsform, file_url=file_url))   

        else:
            file_url=None

        return self.render('LaitGood_admins/admin_commendsupload.html', commendsform=commendsform, file_url = file_url)

admin.add_view(commendsupload(name='推薦上傳', category='好評推薦', url='/commendsupload/'))

# 後台管理-管理線上購物產品
class ProductContent(ModelView):
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
    create_modal = False
    edit_modal = True

    # 自訂義column欄位名
    column_labels = dict(product_image='產品圖檔', 
                        product_name='產品名', 
                        product_package='包裝規格', 
                        product_price='定價', 
                        product_sellprice='售價',
                        product_intro='產品說明'
                        )
    
    # 設定編輯欄位
    form_columns = ['product_name', 'product_package', 'product_price', 'product_sellprice', 'product_intro']

# 渲染後台管理db的頁面
admin.add_view(ProductContent(Shoppingdata, db.session, url='/LaitGood_cart/Product',name='線上購物', category='產品購物'))

# 後台管理-上傳線上購物產品
class Productupload(BaseView):
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
   
    @expose('/', methods=['GET','POST']) 
    def Productupload(self):
        productform = ProductUploadForm()

        if productform.validate_on_submit():
            file_name = upload.save(productform.imgbtn_uploads.data)
            file_url = upload.url(file_name)
            print('成功上傳圖檔：' + file_name,'；圖檔路徑：'+ file_url)
            
            product =  Shoppingdata(
                product_image = file_url,
                product_name = productform.product_name.data,
                product_package = productform.product_package.data, 
                product_price = productform.product_price.data, 
                product_sellprice = productform.product_sellprice.data,
                product_intro = productform.product_intro.data
            )
            db.session.add(product)
            db.session.commit()

            flash('已成功上傳此產品，若需刪改請至消息列表進行管理。')
            return redirect(url_for('productupload.Productupload', productform=productform, file_url=file_url))   

        else:
            file_url=None

        return self.render('LaitGood_admins/admin_productupload.html', productform=productform, file_url = file_url)

admin.add_view(Productupload(name='產品上傳', category='產品購物', url='/LaitGood_cart/Productupload/'))

# 後台管理-行銷優惠活動
class SaleActivitySet(ModelView):
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
    can_delete = False
    can_edit = True
    can_create = False
    can_view_details = True # 可以看到所有欄位的完整內容

    # 自訂義column欄位名
    column_labels = dict(activity_name='行銷活動', 
                        activity_on='是否開啟', 
                        activity_dataset='數據設定', 
                        activity_intro='功能介紹'
                        )
    
    # 設定編輯欄位
    form_columns = ['activity_on', 'activity_dataset']
    # 設定為可直接就地修改的欄位
    column_editable_list = ['activity_on', 'activity_dataset']

# 渲染後台管理db的頁面
admin.add_view(SaleActivitySet(SaleActivity, db.session, url='/SaleActivity/',name='行銷活動', category='產品購物'))
