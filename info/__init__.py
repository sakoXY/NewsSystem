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
