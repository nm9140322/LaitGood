# 寫出程式後執行會出現網址，成為網站伺服器，可以從瀏覽器看到內容運行 ，直到停止執行此程式
# 如果要24小時運行網站，就要利用雲端部署

from flask import Flask, request, render_template,url_for,redirect, flash

app = Flask(__name__) # __name__為python內建變數，代表目前執行的模組



# 函式的裝飾(Decorator)：以函式為基礎，提供附加的功能，按照所需的功能添加，可以有很多個，定義不同的根目錄即可

# 使用者按下登入頁面之後會驗證帳號密碼，驗證失敗就顯示登入失敗訊息，驗證成功則引導使用者到另一個頁面去
@app.route('/', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        username=request.form.get('username')
        if (username == 'CEO'):
            return redirect(url_for('LaitGood'))
        else:
            flash("帳號錯誤，請重新輸入！")  # 閃現訊息   
            return redirect(url_for('login'))

    return render_template('login.html') #  將HTML5的程式碼放在另一個檔案裡，藉由flask提供的函式render_template()去讀取


# @app.route('/LaitGoodmember') # preHTML測試用的
# def LaitGoodHomepage():
#     return render_template('LaitGoodHomepage.html') 


@app.route('/LaitGood', methods=['GET', 'POST']) # 利用利用jinja模板語法直接繼承基礎模板做出的首頁例子
def LaitGood():
    # if request.method == 'POST':
    #     return redirect(url_for('login'))
    return render_template('LaitGood.html') 


@app.route('/LaitGoodmember_login') # 利用利用jinja模板語法直接繼承基礎模板做出的會員登入頁面
def LaitGoodmember_login():

    return render_template('member_login.html') 

if __name__=='__main__': # 如果以__name__為主程式去執行
    app.config.from_object('config') # 啟動config.py中的金鑰
    app.run(debug = True) # 立刻啟動伺服器：.run()
