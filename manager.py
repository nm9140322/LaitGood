# 啟動文件

from app_LaitGood import app

app.debug = True
app.run()

# print(app.url_map) # 透過app.url_map可以查詢專案所有路由清單，可以用來看執行狀況

# 把該專案上傳至Github，在終端機輸入指令：
# 0. 在目前工作區 (Workspace) 內建立一個 .git folder(初次上傳才需要)：git init
# 1. 工作目錄內所有檔案建立索引：git add .
# 2. 建立索引的檔案提交至本地資料庫(自訂說明)：git commit -m "自訂說明"
# 3. 上傳至 GitHub：git push


# 3-1. 上傳所有分支至 Git 目錄：git push --all origin
# 3-2. 上傳指定分支至 Git 目錄：git push origin master