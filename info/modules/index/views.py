# from info.modules.index import index_blue
from . import index_blue
from ... import redis_store
import logging
from flask import current_app, render_template, session, jsonify, request

from ...models import User, News, Category
from ...utils.response_code import RET


# 首页新闻列表
# 请求路径: /newslist
# 请求方式: GET
# 请求参数: cid,page,per_page
# 返回值: data数据
@index_blue.route('/newslist')
def newslist():
    """
    1. 获取参数
    2. 参数类型转换
    3. 分页查询
    4. 获取到分页对象中的属性,总页数,当前页,当前页的对象列表
    5. 将对象列表转成字典列表
    6. 携带数据,返回响应
    :return:
    """
    # 1. 获取参数
    cid = request.args.get("cid", "1")
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "10")

    # 2. 参数类型转换
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        page = 1
        per_page = 10

    # 3. 分页查询
    try:
        paginate = News.query.filter(News.category_id == cid).order_by(News.create_time.desc()).paginate(page, per_page,
                                                                                                         False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    # 4. 获取到分页对象中的属性,总页数,当前页,当前页的对象列表
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items

    # 5. 将对象列表转成字典列表
    news_list = []
    for news in items:
        news_list.append(news.to_dict())

    # 6. 携带数据,返回响应
    return jsonify(errno=RET.OK, errmsg="获取新闻成功", totalPage=totalPage, currentPage=currentPage,
                   newsList=news_list)


@index_blue.route('/', methods=['GET', 'POST'])
def hello_world():
    # 1. 获取用户的登录信息
    user_id = session.get("user_id")

    # 2. 通过user_id取出用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    # 3. 根据点击量，查询前10条新闻
    try:
        news = News.query.order_by(News.clicks.desc()).limit(10).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻失败")

    # 4. 将新闻对象列表转成字典列表
    news_list = []
    for item in news:
        news_list.append(item.to_dict())

    # 5. 查询所有的分类数据
    try:
        categories = Category.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取分类失败")

    # 6. 将分类的对象列表转成字典列表
    category_list = []
    for category in categories:
        category_list.append(category.to_dict())

    # 3. 拼接用户数据，渲染页面
    data = {
        # 如果user有值，返回左边的内容，否则返回右边的值
        "user_info": user.to_dict() if user else "",
        "news_list": news_list,
        "category_list": category_list,
    }

    return render_template("news/index.html", data=data)


# 处理网站logo
@index_blue.route("/favicon.ico")
def get_web_logo():
    return current_app.send_static_file("news/favicon.ico")
