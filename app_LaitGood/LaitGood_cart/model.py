
from app_LaitGood import db, mail # import初始化過的套件
from flask_mail import Message
from threading import Thread # 寄信用的多線程
from flask import current_app, render_template 
import collections # python內建模組，實現了提供特定目標的容器。`
import hashlib # Python 內建的 hashlib 模組可以用來計算資料的各種雜湊值
from urllib.parse import quote_plus # Python 內建 urllib.parse 模組可以幫助解析 URL 中的參數(query)，對參數進行新增或刪除

# 線上購物產品資料表：圖片檔、產品名、包裝規格、價格、產品說明
class Shoppingdata(db.Model):
    __tablename__='LaitGood_Shoppingdata'
    product_id = db.Column(db.Integer, primary_key=True)
    product_image = db.Column(db.String(80), nullable=False)
    product_name = db.Column(db.String(20), nullable=False)
    product_package  = db.Column(db.String(20))
    product_price = db.Column(db.Integer, nullable=False)
    product_sellprice = db.Column(db.Integer)
    product_intro = db.Column(db.String(200))

    # 產品加入購物車的(一對多)關聯式資料庫
    db_product_cart = db.relationship("shopping_cart", backref="product", lazy='dynamic') # backref用於設定取用該資料表內容時的代稱
    # 訂單產生的(一對多)關聯式資料庫
    db_product_order = db.relationship("shopping_order", backref="product", lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return 'product_name:%s, product_price:%s' % (self.product_name, self.product_price)

# 加入購物車資料表：產品圖、產品名、規格、價格、數量
class shopping_cart(db.Model):
    __tablename__='LaitGood_Shoppingcart'
    cart_id = db.Column(db.Integer, primary_key=True)
    cart_amount = db.Column(db.Integer, nullable=False)

    # 產品/會員和購物車的一對多關聯式資料庫
    product_id = db.Column(db.Integer, db.ForeignKey('LaitGood_Shoppingdata.product_id'), nullable=False)
    id =  db.Column(db.Integer, db.ForeignKey('LaitGood_UserRegister.id'), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

     # 後台顯示跟這裡有關
    def __repr__(self):
        return 'cart_amount:%s' % (self.cart_amount)

# 訂購人資料表
class order_pay(db.Model):
    __tablename__='LaitGood_orderpay'
    pay_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    cellphone = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(10))
    county = db.Column(db.String(5))
    district = db.Column(db.String(5))
    zipcode = db.Column(db.String(5))
    address = db.Column(db.String(80), nullable=False)
    pay_price = db.Column(db.Integer, nullable=False) # 訂單總金額
    pay_method = db.Column(db.String(10)) # 付款方式：到貨付款/線上付款

    # 訂購人-訂單關聯式資料庫
    db_pay_ordernum = db.relationship("order_number", backref="pay", lazy='dynamic') # 訂單標號

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    # 後台顯示的結果跟這裡有關
    def __repr__(self):
        return f'''訂購資料ID： { self.pay_id }；
           購買人： { self.username }；
           聯絡信箱： { self.email }；
           手機號碼： { self.cellphone }；
           聯絡電話： { self.phone }；
           寄送地址： { self.zipcode }  { self.county + self.district + self.address}；
           訂單總額： { self.pay_price }；
           付款方式： { self.pay_method }'''

# 訂單編號資料表
class order_number(db.Model):
    __tablename__='LaitGood_ordernumber'
    ordernum_id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(15), nullable=False) # 訂單編號規則(日期-6隨機碼流水號)：yyyymmddXXXXXX
    order_date = db.Column(db.Date) # 訂購日期
    order_paymethod = db.Column(db.String(10)) # 付款狀況：到貨付款/尚未付款/已付款-yyyymmdd
    order_deliver = db.Column(db.Boolean, default=False) # 出貨狀況：尚未出貨/已出貨，後臺手動更改
    order_finish = db.Column(db.Boolean, default=False) # 訂單配送完成，後臺手動更改
    
    # 關聯式資料庫
    id =  db.Column(db.Integer, db.ForeignKey('LaitGood_UserRegister.id'), nullable=False) # 會員資料
    pay_id = db.Column(db.Integer, db.ForeignKey('LaitGood_orderpay.pay_id'), nullable=False) # 訂購人資料

    db_ordernum_order = db.relationship("shopping_order", backref="ordernum", lazy='dynamic') # 關聯-訂單內容
    db_ordernum_trade = db.relationship("Transaction", backref="ordernum", lazy='dynamic') # 關聯-交易編號

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def __repr__(self):
        return f'''訂購資料ID： { self.pay_id }；
           會員資料ID： { self.id }；
           訂單編號： { self.order_number }；
           下訂日期： { self.order_date }'''

# 產生訂單資料表
class shopping_order(db.Model):
    __tablename__='LaitGood_Shoppingorder'
    order_id = db.Column(db.Integer, primary_key=True)
    order_amount = db.Column(db.Integer, nullable=False)

    # 產品/會員和購物車的一對多關聯式資料庫
    ordernum_id = db.Column(db.Integer, db.ForeignKey('LaitGood_ordernumber.ordernum_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('LaitGood_Shoppingdata.product_id'), nullable=False)
    id =  db.Column(db.Integer, db.ForeignKey('LaitGood_UserRegister.id'), nullable=False)
    t_id = db.Column(db.Integer, db.ForeignKey('LaitGood_Transaction.t_id')) # 線上付款交易資料

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# 訂單寄信功能區
def send_async_email(app, msg):

    with app.app_context():
        mail.send(msg)
        print('確認訂單寄信OK')

def cart_sendmail(subject, recipients, template, **kwargs):

    app = current_app._get_current_object()
    msg = Message(subject,
                recipients = recipients)
    msg.html = render_template(template + '.html', **kwargs)

    #  使用多線程
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr  

# 綠界金流串接區
class Params:
    def __init__(self):
        web_type = 'testing'
        if web_type == 'production':
            # 正式環境
            self.params = {
                'MerchantID': 'ID隱藏',
                'HashKey': 'Key 隱藏',
                'HashIV': 'IV 隱藏',
                'action_url':
                'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5'
            }
        else:
            # 測試環境（開發/測試），測試用的MerchantID、HashKey和HashIV
            self.params = {
                'MerchantID':
                '3002607',
                'HashKey':
                'pwFHCqoQZGmho4w6',
                'HashIV':
                'EkRm7iFT261dpevs',
                'action_url':
                'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'
            }

    @classmethod
    def get_params(cls):
        return cls().params

    # 驗證：綠界傳送的檢查碼 check_mac_value 值是否正確
    @classmethod
    def get_mac_value(cls, get_request_form):

        params = dict(get_request_form)
        if params.get('CheckMacValue'):
            params.pop('CheckMacValue')

        # 將傳遞參數依照字母排序
        ordered_params = collections.OrderedDict(
            sorted(params.items(), key=lambda k: k[0].lower()))

        # 參數最前面加上 HashKey、最後面加上 HashIV
        HahKy = cls().params['HashKey']
        HashIV = cls().params['HashIV']

        encoding_lst = []
        encoding_lst.append('HashKey=%s&' % HahKy)
        encoding_lst.append(''.join([
            '{}={}&'.format(key, value)
            for key, value in ordered_params.items()
        ]))
        encoding_lst.append('HashIV=%s' % HashIV)

        safe_characters = '-_.!*()'
        
        # 進行 URL encode，轉為小寫
        encoding_str = ''.join(encoding_lst)
        encoding_str = quote_plus(str(encoding_str),
                                  safe=safe_characters).lower()

        # 以 SHA256 加密方式來產生雜凑值，再轉大寫產生 CheckMacValue
        check_mac_value = ''
        check_mac_value = hashlib.sha256(
            encoding_str.encode('utf-8')).hexdigest().upper()

        return check_mac_value

# 綠界-線上交易標號資料表
class Transaction(db.Model):
    __tablename__='LaitGood_Transaction'
    t_id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer, nullable=False)
    trade_num  = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(5), nullable=False)

    # 訂單編號的一對多關聯式資料庫
    ordernum_id = db.Column(db.Integer, db.ForeignKey('LaitGood_ordernumber.ordernum_id'), nullable=False)

    # 關聯式資料庫
    db_trade_order = db.relationship("shopping_order", backref="trade", lazy='dynamic') # 關聯-訂單內容

    def __init__(self, **kwargs):
        super().__init__(**kwargs)