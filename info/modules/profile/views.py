from flask import render_template, g, redirect, request

from . import profile_blue
from ...utils.commons import user_login_data


# 获取/设置用户基本信息
# 请求路径: /user/base_info
# 请求方式:GET,POST
# 请求参数:POST请求有参数,nick_name,signature,gender
# 返回值:errno,errmsg
@profile_blue.route('/base_info', methods=['GET', 'POST'])
@user_login_data
def base_info():
    """
    1. 判断请求方式,如果是get请求
    2. 携带用户数据,渲染页面
    3. 如果是post请求
    4. 获取参数
    5. 校验参数,为空校验
    6. 修改用户的数据
    7. 返回响应
    :return:
    """
    # 1. 判断请求方式,如果是get请求
    if request.method == 'GET':
        # 2. 携带用户数据,渲染页面
        return render_template("users/user_base_info.html", user_info=g.user.to_dict())

    # 3. 如果是post请求
    pass
    # 4. 获取参数
    # 5. 校验参数,为空校验
    # 6. 修改用户的数据
    # 7. 返回响应


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
