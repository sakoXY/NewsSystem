# from info.modules.index import index_blue
from . import index_blue
from ... import redis_store
import logging
from flask import current_app, render_template


@index_blue.route('/')
def hello_world():
    # 测试redis存取数据
    # redis_store.set("name", "xiayao")
    # print(redis_store.get("name"))

    # 测试Session存取
    # session["name"] = "xxxy"
    # print(session.get("name"))

    # 没有继承日志之前，使用print输出，不方便做控制
    # print("helloworld")

    # 使用日志记录方法logging进行输出可控
    # logging.debug("输入调试信息")
    # logging.info("输入详细信息")
    # logging.warning("输入警告信息")
    # logging.error("输入错误信息")

    # 也可以使用current_app来输出日志信息，输出的时候有分割线，写在文件中完全一样
    # current_app.logger.debug("输入调试信息")
    # current_app.logger.info("输入详细信息")
    # current_app.logger.warning("输入警告信息")
    # current_app.logger.error("输入错误信息")

    return render_template("news/index.html")


# 处理网站logo
@index_blue.route("/favicon.ico")
def get_web_logo():
    return current_app.send_static_file("news/favicon.ico")
