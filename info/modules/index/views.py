# from info.modules.index import index_blue
from . import index_blue
from ... import redis_store
import logging
from flask import current_app, render_template, session, jsonify

from ...models import User, News
from ...utils.response_code import RET


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

    # 3. 拼接用户数据，渲染页面
    data = {
        # 如果user有值，返回左边的内容，否则返回右边的值
        "user_info": user.to_dict() if user else "",
        "news_list": news_list
    }

    return render_template("news/index.html", data=data)


# 处理网站logo
@index_blue.route("/favicon.ico")
def get_web_logo():
    return current_app.send_static_file("news/favicon.ico")
