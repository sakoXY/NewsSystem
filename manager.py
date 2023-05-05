"""
相关配置信息：
1. 数据库配置
2. redis配置
3. session配置
4. csrf配置
"""
from datetime import timedelta

from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session

app = Flask(__name__)


# 设置配置信息
class Config(object):
    # 调试信息
    DEBUG = True
    SECRET_KEY = "asdfghgfddfghj"

    # 数据库配置信息
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/info"
    SQLALCHEMY_TRACK_MODEFICATIONS = False

    # redis 配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # Session配置信息
    SESSION_TYPE = "redis"  # 设置session存储类型
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 指定session存储的redis服务器
    SESSION_USE_SIGNER = True  # 设置签名存储
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)  # 设置session有效期2天


app.config.from_object(Config)

# 创建SQLAlchemy对象，关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# 创建Session对象，读取app中session的信息
Session(app)


@app.route('/')
def hello_world():
    # 测试redis存取数据
    redis_store.set("name", "xiayao")
    print(redis_store.get("name"))

    # 测试Session存取
    session["name"] = "xxxy"
    print(session.get("name"))

    return "helloworld"


if __name__ == "__main__":
    app.run(debug=True)
