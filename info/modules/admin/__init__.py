from flask import Blueprint

# 1.创建管理员蓝图对象
admin_blue = Blueprint("admin", __name__, url_prefix="/admin")

# 2.装饰视图函数
from . import views
