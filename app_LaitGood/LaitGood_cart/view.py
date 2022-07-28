# 執行並渲染網頁的view
# 記得還要連接後台系統
# 以後台管理db再把其內容選染到前端功能的為主

from . import cart # blueprint，所有網址url_for都要加上前綴.cart 
from app_LaitGood import db, csrf # 從__init__.py 引入初始化的app
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app_LaitGood.LaitGood_cart.model import Shoppingdata, shopping_cart, shopping_order, order_number, order_pay, cart_sendmail, Params, Transaction
from app_LaitGood.LaitGood_admins.model import SaleActivity
from app_LaitGood.LaitGood_cart.form import ShoppingForm, OrderPayForm
import datetime
import random
import importlib.util # 設定綠界金流的SDK路徑

# 資料庫操作
@cart.route('/dbtable', methods=['GET', 'POST'])
def dbtable():   
    db.create_all() # 建置table
    return '建置資料庫註冊表'

# 攔截所有request的function，用於攔截尚未啟動的帳號
# 使用者狀況：登入、尚未啟動、endpoint不等於static(避免靜態資源的取用異常)及相關例外清單，否則重啟信件等request也會被攔截
@cart.before_request
def before_request():
    if (current_user.is_authenticated and
            not current_user.confirm and
            request.endpoint not in ['cart.receive_result', 'cart.trad_result', 'cart.LaitGood_toecpay'] and
            request.endpoint != 'static'): 

        return render_template('LaitGood_member/member_unactivate.html')

# 線上購物頁
@cart.route('/LaitGood_Shoppinglist', methods=['GET', 'POST'])
@cart.route('/LaitGood_Shoppinglist/<int:page>/', methods=['GET', 'POST'])
def LaitGood_Shoppinglist(page=1): # 預設page為1，代表以第1頁開始
    Shopping = Shoppingdata.query.paginate(page, 6, False) # paginate的參數：第一個page是代表頁次，第二個6代表每頁幾筆，第三個False是如果沒下一頁是否拋出異常。 
    shopform = ShoppingForm()

    if shopform.validate_on_submit():
        if current_user.is_authenticated:   
            cart = shopping_cart(
                product_id = request.form.get('product_id'), # 隱藏欄位預設值
                id = current_user.id,
                cart_amount = shopform.product_amount.data
            )

            db.session.add(cart)
            db.session.commit()

            # 資料表名稱使用backref的設定
            totalprice = cart.product.product_price*cart.cart_amount
            print(cart.product.product_name,'數量：', cart.cart_amount, '總共：$', totalprice)
            print('訂購人：' + cart.member.username)
            return redirect(request.referrer)

        else:
            flash('請先登入會員，謝謝！')
            return redirect(request.referrer)

    return render_template('LaitGood_cart/Shopping_list.html', Shopping=Shopping, form=shopform) 

# 產品販售頁
@cart.route('/LaitGood_Shoppingproduct', methods=['GET', 'POST'])
@cart.route('/LaitGood_Shoppingproduct/<int:product_id>/', methods=['GET', 'POST'])
def LaitGood_Shoppingproduct(product_id):
    products =  Shoppingdata.query.filter_by(product_id=str(product_id)).first()  # Flask 接收 GET 方式的網頁資料
    shopform = ShoppingForm()

    if shopform.validate_on_submit(): 
        if current_user.is_authenticated:   
            cart = shopping_cart(
                product_id = products.product_id,
                id = current_user.id,
                cart_amount = shopform.product_amount.data
            )

            db.session.add(cart)
            db.session.commit()
            
            # 資料表名稱使用backref的設定
            totalprice = cart.product.product_price*cart.cart_amount
            print(cart.product.product_name,'數量：', cart.cart_amount, '總共：$', totalprice)
            print('訂購人：' + cart.member.username)
            
            return redirect(request.referrer)
        else:
            flash('請先登入會員，謝謝！')
            return redirect(request.referrer) # request.referrer HTTP referrer是一個用來記錄請求發源地址的HTTP首部字段（HTTP_REFERER），即訪問來源

    return render_template('LaitGood_cart/Shopping_product.html', products=products, form=shopform)

# 會員購物車頁面，排版待修
@cart.route('/LaitGood_membercart', methods=['GET', 'POST'])
@login_required
def LaitGood_membercart():
    member = shopping_cart.query.filter_by(id=current_user.id).first() # 使用者名稱
    membercart = shopping_cart.query.filter_by(id=current_user.id).all() # 購物車商品列表
    cart_number = shopping_cart.query.filter_by(id=current_user.id).count() # 項目總筆數

    # 總價 = 各項目價錢*價錢 
    totalprice = 0
    for productorder in range(0, cart_number, 1):
        productprice = membercart[productorder].product.product_sellprice # 售價為主
        if productprice == None:
            productprice = membercart[productorder].product.product_price # 沒有售價就用定價計 
        productamount = membercart[productorder].cart_amount
        totalprice = productprice*productamount + totalprice # 商品總額
    
    # 後台-行銷活動
    activity_allfeefree = SaleActivity.query.filter_by(id=1).first() # 全館免運
    activity_spendfeefree = SaleActivity.query.filter_by(id=2).first() # 滿額免運
    activity_alldiscount = SaleActivity.query.filter_by(id=3).first() # 全館打折
    activity_buyonegetfree = SaleActivity.query.filter_by(id=4).first() # 買一送多

    fee = activity_allfeefree.activity_dataset

    # 全館打折
    if activity_alldiscount.activity_on == True:
        new_totalprice = totalprice*activity_alldiscount.activity_dataset*0.01
    else:
        new_totalprice = totalprice

    # 全館免運/滿額免運
    freethreshold = activity_spendfeefree.activity_dataset-new_totalprice
    
    if activity_allfeefree.activity_on == True:
        fee = 0
    elif (activity_spendfeefree.activity_on == True) & (freethreshold <= 0):
        fee = 0
    else:
        pass
    
    # 訂單總價 (四捨五入)
    totalpricefee = round(new_totalprice + fee)
    user = current_user
    payform = OrderPayForm(obj=user) # 訂購人表單
    
    # 刪除項目/進入填寫訂購資訊頁
    if request.method == 'POST':
        delete = request.form.get('delete')
        paydata = request.form.get('paydata')
    
        if delete == '刪除':
            delete_cart_id = request.form.get('cart_id')
            product_del = shopping_cart.query.filter_by(cart_id=delete_cart_id).first()
            db.session.delete(product_del)
            db.session.commit()
            flash('已從購物車中刪除該品項！')
            return redirect(url_for('cart.LaitGood_membercart'))

        elif paydata == '填寫資料':
            # 先從會員表代入資料，使用者可以修改且不會動到原本的會員資料
            payform.populate_obj(user)
            return render_template('LaitGood_cart/member_pay.html', payform=payform, user=user)
         
        else:
            # 訂購人資料填寫
            if payform.validate():
                orderpay = order_pay(
                    username = payform.username.data,
                    email = payform.email.data,
                    cellphone = payform.cellphone.data,
                    phone = payform.phone.data,
                    zipcode = request.form.get('zipcode'),
                    county = request.form.get('county'),
                    district = request.form.get('district'),
                    address = payform.address.data,
                    pay_price = totalpricefee,
                    pay_method = payform.pay_method.data
                    )

                db.session.add(orderpay)
                db.session.commit()
                print('新增訂購人資料：', orderpay.username)
                return redirect(url_for('cart.LaitGood_memberorder', pay_id=orderpay.pay_id))
                
            else:
                flash('請確認資料填寫正確')
                return render_template('LaitGood_cart/member_pay.html', payform=payform, user=user)
        
    return render_template('LaitGood_cart/member_cart.html', 
                            membercart=membercart, 
                            member=member, 
                            totalprice=totalprice, 
                            new_totalprice=new_totalprice, 
                            fee=fee,
                            totalpricefee=totalpricefee, 
                            activity_alldiscount=activity_alldiscount, 
                            activity_allfeefree=activity_allfeefree, 
                            activity_spendfeefree=activity_spendfeefree, 
                            freethreshold=freethreshold, 
                            activity_buyonegetfree=activity_buyonegetfree
                            )

# 產生正式訂單資訊頁
@cart.route('/LaitGood_memberorder', methods=['GET', 'POST'])
@cart.route('/LaitGood_memberorder/<int:pay_id>/', methods=['GET', 'POST'])
@login_required
def LaitGood_memberorder(pay_id):
    try:
        ordernum = order_number.query.filter_by(pay_id = str(pay_id)).first()

        # 產生新的訂單
        if ordernum == None:
            # 付款方式除了選到貨付款，其他都會是尚未付款，後面再進入付款頁
            orderpay = order_pay.query.filter_by(pay_id = str(pay_id)).first()
            if orderpay.pay_method == 'cash':
                order_paymethod = '到貨付款'
            else:
                order_paymethod = '尚未付款'                
            
            # 先產生訂單編號，連結會員及訂購人資料
            ordernum = order_number(
                order_number = datetime.datetime.today().strftime("%Y%m%d")+ str(random.randrange(1, 999999)).zfill(6),
                order_date = datetime.date.today(),
                order_paymethod = order_paymethod, 
                id = current_user.id,
                pay_id = str(pay_id)
            )         
            
            db.session.add(ordernum)
            db.session.commit()
            print('產生訂單編號：', ordernum.order_number, '；訂單金額：', ordernum.pay.pay_price)
        
            # 產生實際訂單內容並將正式訂單存入資料庫，關聯訂單編號、會員、訂購人資料、產品內容及數量

            membercart = shopping_cart.query.filter_by(id=current_user.id).all() # 購物車商品列表
            cart_number = shopping_cart.query.filter_by(id=current_user.id).count() # 項目總筆數
            activity_buyonegetfree = SaleActivity.query.filter_by(id=4).first() # 行銷活動-買一送多

            for orders in range(0, cart_number, 1):
                # 買一送多
                if activity_buyonegetfree.activity_on == True:
                    order_amount = membercart[orders].cart_amount*activity_buyonegetfree.activity_dataset
                else:
                    order_amount = membercart[orders].cart_amount

                order = shopping_order(
                    ordernum_id = ordernum.ordernum_id,
                    id = membercart[orders].id,
                    product_id = membercart[orders].product_id,
                    order_amount = order_amount
                )
                db.session.add(order)
                db.session.commit()
                print('加入訂單內容：' + order.product.product_name, '，數量：', order.order_amount)
                db.session.delete(membercart[orders]) # 刪除購物車內容
                db.session.commit()
                print('清空購物車' )

            #  寄出確認訂購的信件
            cart_sendmail(
                subject='感謝您訂購日果產品！',
                template='LaitGood_cart/mail/cartorder_mail',
                recipients = [ordernum.pay.email],
                ordernum=ordernum
                )
            neworderlist = shopping_order.query.filter_by(ordernum_id = str(pay_id)).all()
            return redirect(url_for('cart.LaitGood_memberorder', pay_id=ordernum.pay_id, ordernum=ordernum, orderlist=neworderlist))
                
        elif request.method == 'POST':
            # 取消訂單
            cancel = request.form.get('cancel')
            if cancel == "取消訂單":
                #  寄出取消訂購的信件
                cart_sendmail(
                    subject='日果本次訂單已取消，隨時歡迎您再次光臨',
                    template='LaitGood_cart/mail/ordercancel_mail',
                    recipients = [ordernum.pay.email],
                    ordernum=ordernum
                    )

                db.session.query(shopping_order).filter_by(ordernum_id = str(pay_id)).delete() # 刪除訂單全部內容
                db.session.delete(ordernum) # 刪除訂單編號
                db.session.delete(ordernum.pay) # 刪除訂購資訊
                db.session.commit()
                flash('已取消本筆訂單，如有需要請重新下訂！')
                return redirect(url_for('cart.LaitGood_ordersearch'))
        else:
            orderlist = shopping_order.query.filter_by(ordernum_id = str(pay_id)).all()
            return render_template('LaitGood_cart/member_order.html', ordernum=ordernum, orderlist=orderlist)
    
    except:
        flash('非常抱歉，您剛剛的訂單似乎出了點問題，詳情請洽客服！')

    return render_template('LaitGood_cart/member_order.html', ordernum=ordernum)

# 訂單查詢頁
@cart.route('/LaitGood_ordersearch', methods=['GET', 'POST'])
@login_required
def LaitGood_ordersearch():
    ordernums_new = order_number.query.filter_by(id = current_user.id, order_finish = False).all() # 進行中訂單
    ordernums_old = order_number.query.filter_by(id = current_user.id, order_finish = True).all() # 歷史訂單

    return render_template('LaitGood_cart/member_ordersearch.html', ordernums_new=ordernums_new, ordernums_old=ordernums_old)

# 綠界付款頁
@cart.route('/LaitGood_toecpay', methods=['GET', 'POST'])
@cart.route('/LaitGood_toecpay/<int:ordernum_id>/', methods=['GET', 'POST'])
def LaitGood_toecpay(ordernum_id):
    # 設定SDK路徑
    spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",  # SDK檔名不用改
    "app_LaitGood/LaitGood_cart/ecpay_payment_sdk.py" # 放置此檔案的路徑位置
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    payordernum = order_number.query.filter_by(ordernum_id = str(ordernum_id)).first()
    host_name = request.host_url # 使用者網域
    date = datetime.datetime.today().strftime("%Y%m%d")
    trade_num = date + 'ordernum' + str(ordernum_id) # 建立線上交易編號
    total_price = payordernum.pay.pay_price
    orderprouct = '日果產品'
    ordernum_id = payordernum.ordernum_id
    
    # 客戶資訊
    # customer_name = payordernum.pay.username
    # customer_addr = payordernum.pay.zipcode, payordernum.pay.county, payordernum.pay.district, payordernum.pay.address
    # customer_phone = payordernum.pay.cellphone
    # customer_email = payordernum.pay.email

    # 建立線上付款訂單的交易資料
    trade = Transaction(
        trade_num = trade_num,  
        ordernum_id = ordernum_id, 
        total_price = total_price, 
        status = '未刷卡'
        )
    db.session.add(trade)
    db.session.commit()

    params = Params.get_params()

    # 設定傳送給綠界參數：將交易商品 ＆ 金額寫進參數，並呼叫綠界 SDK，跳轉至綠界
    order_params = {
        'MerchantTradeNo': datetime.datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': total_price,
        'TradeDesc': 'ToolsFactory',
        'ItemName': orderprouct,
        'ReturnURL': host_name + 'receive_result',
        'ChoosePayment': 'ALL',
        'ClientBackURL': host_name + 'trad_result',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': host_name + 'trad_result',
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': str(trade_num),
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }
    
    # ChoosePayment：ALL 或 ATM 付款方式
    extend_params_1 = {
        'ExpireDate': 7,  # 允許繳費有效天數
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php', # Server 端回傳付款相關資訊
        'ClientRedirectURL': '', # 看完付款資訊，要重導到哪裡
    }

    # ChoosePayment：ALL 或 CVS 或 BARCODE 付款方式
    extend_params_2 = {
        'StoreExpireDate': 15, #  超商繳費截止時間
        'Desc_1': '日果訂單付款交易，請於15天內完成付款', # 交易描述，若繳費超商為 family(全家)或 ibon(7-11)時，會顯示在超商繳費平台螢幕
        'Desc_2': '',
        'Desc_3': '',
        'Desc_4': '',
        'PaymentInfoURL': 'https://www.ecpay.com.tw/payment_info_url.php', # Server 端回傳付款相關資訊 
        'ClientRedirectURL': '', # Client 端回傳付款方式相關資訊 
    }
    # ChoosePayment：ALL 或  Credit 付款方式
    extend_params_3 = {
        'BindingCard': 0, #  記憶信用卡號：1是用，0是不用
        'MerchantMemberID': '', # 記憶卡號識別碼 (特店代號MerchantID+廠商會員編號) 
    }

    extend_params_4 = {
        'Redeem': 'N', # 信用卡是否使用紅利折抵
        'UnionPay': 0, # 銀聯卡交易選項 
    }
    
    # 發票資訊
    inv_params = {
    #     'RelateNumber': 'Tea0001', # 特店自訂編號
    #     'CustomerID': 'TEA_0000001', # 客戶編號
    #     'CustomerIdentifier': '53348111', # 統一編號
    #     'CustomerName': customer_name, # 客戶名稱
    #     'CustomerAddr': customer_addr, # 客戶地址
    #     'CustomerPhone': customer_phone, # 客戶手機號碼
    #     'CustomerEmail': customer_email,  # 客戶信箱
    #     'ClearanceMark': '2', # 通關方式
    #     'TaxType': '1', # 課稅類別
    #     'CarruerType': '', # 載具類別
    #     'CarruerNum': '', # 載具編號
    #     'Donation': '1', # 捐贈註記
    #     'LoveCode': '168001', # 捐贈碼
    #     'Print': '1',
    #     'InvoiceItemName': '測試商品1|測試商品2',
    #     'InvoiceItemCount': '2|3',
    #     'InvoiceItemWord': '個|包',
    #     'InvoiceItemPrice': '35|10',
    #     'InvoiceItemTaxType': '1|1',
    #     'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
    #       'DelayDay': '0', # 延遲天數
    #     'InvType': '07', # 字軌類別
    }

    ecpay_payment_sdk = module.ECPayPaymentSdk(MerchantID=params['MerchantID'],
                                               HashKey=params['HashKey'],
                                               HashIV=params['HashIV'])

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)
    order_params.update(extend_params_3)
    order_params.update(extend_params_4)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = params['action_url']
        html = ecpay_payment_sdk.gen_html_post_form(action_url,final_order_params)
        return html

    except Exception as error:
        print('An exception happened: ' + str(error))

# 綠界回傳交易資訊（ReturnURL接收）頁
@csrf.exempt
@cart.route('/receive_result', methods=['POST'])
def end_return():
    result = request.form['RtnMsg']
    trade_num = request.form['CustomField1']
    trade_detail = Transaction.query.filter_by(trade_num=trade_num).first()
    trade_detail.status = '交易成功 sever post'
    db.session.add(trade_detail)
    db.session.commit()

    return '1|OK' # 如有接收成功，官方要求回應1|OK

# 綠界Client端回傳付款結果（ OrderResultURL 接收）頁
@csrf.exempt # 使用裝飾器排除crsf來源請求
@cart.route('/trad_result', methods=['GET', 'POST'])
def end_page():

    if request.method == 'GET':
        return redirect(url_for('cart.LaitGood_ordersearch'))

    if request.method == 'POST':
        check_mac_value = Params.get_mac_value(request.form)

        # 先檢驗綠界傳送的 check_mac_value 是否為正確
        if request.form['CheckMacValue'] != check_mac_value:
            return '請聯繫管理員'

        # 接收 ECpay 刷卡回傳資訊
        result = request.form['RtnMsg']
        trade_num= request.form['CustomField1']
        trade_detail = Transaction.query.filter_by(trade_num=trade_num).first()
        order = shopping_order.query.filter_by(ordernum_id=trade_detail.ordernum_id).first()

        # 判斷回傳資訊，交易成功則修改修資料庫並且跳轉至交易成功頁面
        if result == 'Succeeded':
            date = datetime.datetime.today().strftime("%Y%m%d")
            trade_detail.status = '訂單成立'
            trade_detail.ordernum.order_paymethod = '已付款-' + date # 待測
            order.t_id = trade_detail.t_id
            
            db.session.commit()
            flash('付款交易成功，感謝惠顧！')
            return render_template('flashmessage.html')

        # 判斷回傳資訊，失敗則跳轉至失敗頁面
        else:
            flash('付款交易失敗，詳情請洽客服')
            return render_template('flashmessage.html')

