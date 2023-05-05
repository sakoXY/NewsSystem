"""
相关配置信息：
1. 数据库配置
2. redis配置
3. session配置
4. csrf配置
"""

from info import create_app
# 调取方法，获取app
app = create_app("develop")

@app.route('/')
def hello_world():
    # 测试redis存取数据
    # redis_store.set("name", "xiayao")
    # print(redis_store.get("name"))

    # 测试Session存取
    # session["name"] = "xxxy"
    # print(session.get("name"))

    return "helloworld"


if __name__ == "__main__":
    app.run()
