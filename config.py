import logging
from datetime import timedelta

from redis.client import StrictRedis


# 设置配置信息（基类配置信息）
class Config(object):
    # 调试信息
    DEBUG = True
    SECRET_KEY = "asdfghgfddfghj"

    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/info"
    SQLALCHEMY_TRACK_MODEFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True # 每当改变数据的内容之后，在视图函数结束的时候都会自动提交

    # redis 配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # Session配置信息
    SESSION_TYPE = "redis"  # 设置session存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 指定session存储的redis服务器
    SESSION_USE_SIGNER = True  # 设置签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)  # 设置session有效期2天

    # 默认的日志级别
    LEVEL_NAME = logging.DEBUG


# 开发环境配置信息
class DevelopConfig(Config):
    pass


# 生产（线上）环境配置信息
class ProductConfig(Config):
    LEVEL_NAME = logging.ERROR
    pass


# 测试环境配置信息
class TestConfig(Config):
    pass


# 提供一个统一的访问入口
config_dict = {
    "develop": DevelopConfig,
    "product": ProductConfig,
    "test": TestConfig
}
