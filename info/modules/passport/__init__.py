from flask import Blueprint

# 1. 创建认证蓝图对象
passport_blue = Blueprint("passport", __name__, url_prefix="/passport")

# 2. 导入views装饰视图函数
from . import views
