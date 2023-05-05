import logging
from logging.handlers import RotatingFileHandler

from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import config_dict
from flask import Flask

# 定义redis_store变量
redis_store = None


# 定义工厂方法
def create_app(config_name):
    # 调用日志方法，记录软件运行信息
    log_file()

    app = Flask(__name__)

    # 根据传入的配置类名称，取出对应的配置类
    config = config_dict.get(config_name)

    # 加载配置类
    app.config.from_object(config)

    # 创建SQLAlchemy对象，关联app
    db = SQLAlchemy(app)

    # 创建redis对象
    global redis_store  # global将局部变量升级为全局变量
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # 创建Session对象，读取app中session的信息
    Session(app)

    # 使用CSRFProtect保护app
    CSRFProtect(app)

    # 将首页蓝图index_blue，注册到app中
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    return app


def log_file():
    # 设置日志的记录等级，常见的有四种，大小关系如下：DEBUG < INFO < WARNING < ERROR
    logging.basicConfig(level=logging.DEBUG)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)
