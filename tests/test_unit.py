# 單元測試用：pip install Flask-Testing
# 只要將想要運行的 py 檔，放置於此 tests 文件中，運行指令時就會被運行到
# 測試文件檔名必須以 test 為開頭，以及測試文件內的 Class 以及 Function 也必須以 test 開頭

import unittest
from flask import url_for
from flask_testing import TestCase
from app_LaitGood  import create_app, db

class SettingBase(TestCase):
    def create_app(self):
        return create_app("testing") # 工廠模式

      # setUp()：在運行測試之前會先被執行
    def setUp(self):
        db.create_all()
        self.username = "test@a.com"
        self.passwords = "666666"
        self.role = 0

      # tearDown()：在結束測試時會被執行
    def tearDown(self):
        db.session.remove()
        db.drop_all()