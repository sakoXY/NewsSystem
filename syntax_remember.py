"""
1. python中的三元运算
    "语句1" if 条件A else "语句2"
    执行特点:
        如果条件A为True, 那么返回语句1, 否则返回语句2


2. 使用g对象配合装饰器使用
    装饰器作用: 给已经存在的方法,添加额外的功能, 而不应该改变原有函数的结构
    解决办法: 不改变原有函数的结构,functools. wraps可以解决该问题

    如果不使用wraps修饰函数,那么报错
     View function mapping is overwriting an existing endpoint function: wrapper

"""
# 1. python中的三元运算
"""
a = "hello" if False else "world"
print(a) #world

b = "hello" if "" else "world"
print(b)

c = "hello" if [] else "world"
print(c)

d = "hello" if None else "world"
print(d)

e = "hello" if [1,2,3] else "world"
print(e)
"""

from functools import wraps
from flask import Flask

haha = Flask(__name__)


# 2.定义装饰器
def user_data(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        """wrapper..doc"""
        print("我是装饰器,给已经存在的函数添加了额外的功能")
        return view_func(*args, **kwargs)

    return wrapper


@haha.route("/index1")
@user_data
def test1():
    """test1..doc"""
    print("test1")


@haha.route("/index2")
@user_data
def test2():
    """test2..doc"""
    print("test2")


print(test1.__name__)
print(test1.__doc__)

print(test2.__name__)
print(test2.__doc__)

# test1()
