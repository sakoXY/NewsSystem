from flask import render_template, g, redirect

from . import profile_blue
from ...utils.commons import user_login_data

# 获取用户信息首页
# 请求路径: /user/user_index
# 请求方式:GET
# 请求参数:无
# 返回值: user.html页面,用户字典data数据
@profile_blue.route('/user_index')
@user_login_data
def user_index():
    # 1. 判断用户是否登录
    if not g.user:
        return redirect("/")

    # 2. 携带数据渲染页面
    data = {
        "user_info": g.user.to_dict()
    }
    return render_template("users/user.html", data=data)
