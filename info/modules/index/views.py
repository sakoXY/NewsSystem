# from info.modules.index import index_blue
from . import index_blue
from ... import redis_store


@index_blue.route('/')
def hello_world():
    # 测试redis存取数据
    redis_store.set("name", "xiayao")
    print(redis_store.get("name"))

    # 测试Session存取
    # session["name"] = "xxxy"
    # print(session.get("name"))

    return "helloworld"
