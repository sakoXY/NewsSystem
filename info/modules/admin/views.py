from datetime import datetime, timedelta
import time
from flask import render_template, request, session, redirect, current_app, g

from . import admin_blue
from ...models import User, News
from ...utils.commons import user_login_data


# 获取/设置新闻审核列表
# 请求路径: /admin/news_review
# 请求方式: GET
# 请求参数: GET, p,keywords
# 返回值:渲染user_list.html页面,data字典数据
@admin_blue.route('/news_review')
def news_review():
    """
      1. 获取参数,p
      2. 参数类型转换
      3. 分页查询用户数据
      4. 获取分页对象属性,总页数,当前页,当前页对象列表
      5. 将对象列表,转成字典列表
      6. 拼接数据,渲染页面
      :return:
      """
    # 1. 获取参数,p
    page = request.args.get("p", "1")
    keywords = request.args.get("keywords", "")

    # 2. 参数类型转换
    try:
        page = int(page)
    except Exception as e:
        page = 1

    # 3. 分页查询待审核,未通过的新闻数据
    try:

        # 3.1判断是否有填写搜索关键
        filters = [News.status != 0]
        if keywords:
            filters.append(News.title.contains(keywords))

        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page=page, max_per_page=3)
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/news_review.html", errmsg="获取新闻失败")

    # 4. 获取分页对象属性,总页数,当前页,当前页对象列表
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5. 将对象列表,转成字典列表
    news_list = []
    for news in items:
        news_list.append(news.to_review_dict())

    # 6. 拼接数据,渲染页面
    data = {
        "totalPage": totalPage,
        "currentPage": currentPage,
        "news_list": news_list
    }
    return render_template("admin/news_review.html", data=data)


# 用户列表
# 请求路径: /admin/user_list
# 请求方式: GET
# 请求参数: p
# 返回值:渲染user_list.html页面,data字典数据
@admin_blue.route('/user_list')
def user_list():
    """
    1. 获取参数,p
    2. 参数类型转换
    3. 分页查询用户数据
    4. 获取分页对象属性,总页数,当前页,当前页对象列表
    5. 将对象列表,转成字典列表
    6. 拼接数据,渲染页面
    :return:
    """
    # 1. 获取参数,p
    page = request.args.get("p", "1")

    # 2. 参数类型转换
    try:
        page = int(page)
    except Exception as e:
        page = 1

    # 3. 分页查询用户数据
    try:
        paginate = User.query.filter(User.is_admin == False).order_by(User.create_time.desc()).paginate(page=page,
                                                                                                        max_per_page=10)
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/user_list.html", errmsg="获取用户失败")

    # 4. 获取分页对象属性,总页数,当前页,当前页对象列表
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5. 将对象列表,转成字典列表
    user_list = []
    for user in items:
        user_list.append(user.to_admin_dict())

    # 6. 拼接数据,渲染页面
    data = {
        "totalPage": totalPage,
        "currentPage": currentPage,
        "user_list": user_list
    }
    return render_template("admin/user_list.html", data=data)


# 用户统计
# 请求路径: /admin/user_count
# 请求方式: GET
# 请求参数: 无
# 返回值:渲染页面user_count.html,字典数据
@admin_blue.route('/user_count')
def user_count():
    # 1. 获取用户总数
    try:
        total_count = User.query.filter(User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/user_count.html", errmsg="获取总人数失败")

    # 2. 获取月活人数
    localtime = time.localtime()
    try:
        # 2.1 先获取本月的1号的0点的, 字符串数据
        month_start_time_str = "%s-%s-01" % (localtime.tm_year, localtime.tm_mon)

        # 2.2 根据字符串,格式化日期对象
        month_start_time_date = datetime.strptime(month_start_time_str, "%Y-%m-%d")

        # 2.3 最后一次登陆的时间大于,本月的1号的0点钟的人数
        month_count = User.query.filter(User.last_login >= month_start_time_date, User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/user_count.html", errmsg="获取月活人数失败")

    # 3. 获取日活人数
    try:
        # 3.1 先获取本日的0点, 字符串数据
        day_start_time_str = "%s-%s-%s" % (localtime.tm_year, localtime.tm_mon, localtime.tm_mday)

        # 3.2 根据字符串,格式化日期对象
        day_start_time_date = datetime.strptime(day_start_time_str, "%Y-%m-%d")

        # 3.3 最后一次登陆的时间大于,本日0点钟的人数
        day_count = User.query.filter(User.last_login >= day_start_time_date, User.is_admin == False).count()
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/user_count.html", errmsg="获取日活人数失败")

    # 4. 获取活跃时间段内,对应的活跃人数
    active_date = []  # 获取活跃的日期
    active_count = []  # 获取活跃的人数
    for i in range(0, 31):
        # 当天开始时间A
        begin_date = day_start_time_date - timedelta(days=i)
        # 当天开始时间, 的后⼀一天B 
        end_date = day_start_time_date - timedelta(days=i - 1)
        # 添加当天开始时间字符串串到, 活跃⽇日期中
        active_date.append(begin_date.strftime("%Y-%m-%d"))
        # 查询时间A到B这⼀一天的注册⼈人数
        everyday_active_count = User.query.filter(User.is_admin == False, User.last_login >= begin_date,
                                                  User.last_login <= end_date).count()
        # 添加当天注册⼈人数到,获取数量量中
        active_count.append(everyday_active_count)

    # 为了图表显示方便,将容器反转
    active_count.reverse()
    active_date.reverse()

    # 5.携带数据渲染页面
    data = {
        "total_count": total_count,
        "month_count": month_count,
        "day_count": day_count,
        "active_date": active_date,
        "active_count": active_count
    }
    return render_template("admin/user_count.html", data=data)


# 请求路径: /admin/index
# 请求方式: GET
# 请求参数: 无
# 返回值:渲染页面index.html,user字典数据
@admin_blue.route('/index')
@user_login_data
def admin_index():
    data = {
        "user_info": g.user.to_dict() if g.user else ""
    }
    return render_template("admin/index.html", data=data)


# 获取/登陆,管理员登陆
# 请求路径: /admin/login
# 请求方式: GET,POST
# 请求参数:GET,无, POST,username,password
# 返回值: GET渲染login.html页面, POST,login.html页面,errmsg
@admin_blue.route('/login', methods=["GET", "POST"])
def admin_login():
    """
    1.判断请求方式,如果是GET,直接渲染页面
    2.如果是POST请求,获取参数
    3.校验参数,为空校验
    4.根据用户名取出管理员对象,判断管理员是否存在
    5.判断管理员的密码是否正确
    6.管理的session信息记录
    7.重定向到首页展示
    :return:
    """
    # 1.判断请求方式,如果是GET,直接渲染页面
    if request.method == "GET":

        # 判断管理员是否已经登陆过了,如果登陆过了指教跳转到首页
        if session.get("is_admin"):
            return redirect("/admin/index")

        return render_template("admin/login.html")

    # 2.如果是POST请求,获取参数
    username = request.form.get("username")
    password = request.form.get("password")

    # 3.校验参数,为空校验
    if not all([username, password]):
        return render_template("admin/login.html", errmsg="参数不全")

    # 4.根据用户名取出管理员对象,判断管理员是否存在
    try:
        admin = User.query.filter(User.mobile == username, User.is_admin == True).first()
    except Exception as e:
        current_app.logger.error(e)
        return render_template("admin/login.html", errmsg="用户查询失败")

    if not admin:
        return render_template("admin/login.html", errmsg="管理员不存在")

    # 5.判断管理员的密码是否正确
    if not admin.check_password(password):
        return render_template("admin/login.html", errmsg="密码错误")

    # 6.管理的session信息记录
    session["user_id"] = admin.id
    session["is_admin"] = True

    # 7.重定向到首页展示
    return redirect("/admin/index")
