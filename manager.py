"""
相关配置信息：
1. 数据库配置
2. redis配置
3. session配置
4. csrf配置
"""
from datetime import timedelta

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)

# 加载配置类
app.config.from_object(Config)

# 创建SQLAlchemy对象，关联app
db = SQLAlchemy(app)

# 创建redis对象
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

# 创建Session对象，读取app中session的信息
Session(app)

# 使用CSRFProtect保护app
CSRFProtect(app)


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
