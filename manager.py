# 啟動文件

from app_LaitGood import app

app.debug = True
app.run()

# print(app.url_map) # 透過app.url_map可以查詢專案所有路由清單，可以用來看執行狀況