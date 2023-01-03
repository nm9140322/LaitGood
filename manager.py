# 啟動文件.py

# 工廠模式
from app_LaitGood import create_app
import os 

app = create_app('development') # development/production
# app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000)) # HEROKU部署不能用localhost，PORT也要抓他自己生成的
app.run(host='0.0.0.0',port=8000)
# app.run()


# print(app.url_map) # 透過app.url_map可以查詢專案所有路由清單，可以用來看執行狀況



# 單元測試，寫入 CLI
# 1. $env:FLASK_APP = "manager.py" # 指定運行檔
# 2. flask test # 運行測試
@app.cli.command()
def test():
    import unittest
    import sys

    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)



# Flask 內建的 command line script 指令，在終端機輸入以下指令來運行 Flask：
# 1. set FLASK_APP=manager.py # 環境設定待會 flask run 時，指定運行的 py 檔是 main.py
# 2. $env:FLASK_APP = "manager.py" (和第一步驟擇一，看哪個找得到)
# 3. flask run --reload --debugger --host 0.0.0.0 --port 80 # 運行 flask run


# 把該專案上傳至Github，在終端機輸入指令：
# 0. 在目前工作區 (Workspace) 內建立一個 .git folder(初次上傳才需要)：git init
# 1. 工作目錄內所有檔案建立索引：git add .
# 2. 建立索引的檔案提交至本地資料庫(自訂說明)：git commit -m "自訂說明"
# 3. 上傳至 GitHub：git push


# 3-1. 上傳所有分支至 Git 目錄：git push --all origin
# 3-2. 上傳指定分支至 Git 目錄：git push origin master


# 資料庫搬移更新：
# 1. flask檔案位置(Windows)：set FLASK_APP = 啟動檔名.py/$env:FLASK_APP = "啟動檔名.py"
# 2. 初始化該資料庫，設定migrations資料夾(只有初次需要)：flask db init
# 3. 設定migrations檔案並加入更新上傳之說明：flask db migrate -m "說明文字"
# 4. 將migrations檔案更新至資料庫中：flask db upgrade
