from flask import Blueprint

# 1. 创建蓝图对象
news_blue = Blueprint("news", __name__, url_prefix="/news")

# 2. 使用蓝图对象，装饰视图函数
from . import views
