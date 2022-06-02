# 使用工廠模式會讓app變成非全域，所以一定要配合藍圖Blueprint建立個模組功能自己的app路徑

from flask import Blueprint

#  定義
admins = Blueprint('admins', __name__)

#  關聯
from . import view
# import app_LaitGood.LaitGood_member.view