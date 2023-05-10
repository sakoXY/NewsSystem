"""
相关配置信息：
1. 数据库配置
2. redis配置
3. session配置
4. csrf配置
"""
from datetime import datetime, timedelta
from random import randint

from flask import current_app

from info import create_app, db, models  # 导入models的作用是让整个应用程序知道有models的存在
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from info.models import User

# 调取方法，获取app
app = create_app("product")

# 创建manager对象，管理app
manager = Manager(app)

# 使用Migrate关联app，db
Migrate(app, db)

# 给manager添加一条操作命令
manager.add_command("db", MigrateCommand)


# 定义方法，创建管理员对象
# @manager.option给manager添加一个脚本运行的方法
# 参数1：在调用方法的时候传递的参数名称
# 参数2：是对参数1的解释
# 参数3：目标参数，用来传递给形式参数使用的
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_superuser(username, password):
    # 1. 创建用户对象
    admin = User()

    # 2. 设置用户属性
    admin.nick_name = username
    admin.mobile = username
    admin.password = password
    admin.is_admin = True

    # 3.保存到数据库
    try:
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return "创建失败"

    return "创建成功"


# 为了图表好看,添加测试用户
@manager.option('-t', '--test', dest='test')
def add_test_user(test):
    # 1. 定义容器
    user_list = []

    # 2. for循环创建1000个用户
    for i in range(0, 1000):
        user = User()
        user.nick_name = "老王%s" % i
        user.mobile = "138%08d" % i
        user.password_hash = "pbkdf2:sha256:600000$kAovSighC9dCUwni$900c6222a2ff0819c113b96f8cee53243529262721ccfeaea4dec3472e86962e"
        # 设置用户的登陆时间为近31天的
        user.last_login = datetime.now() - timedelta(seconds=randint(0, 3600 * 24 * 31))

        user_list.append(user)

    # 3. 将用户添加到数据库中
    try:
        db.session.add_all(user_list)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return "添加测试用户失败"

    return "添加测试用户成功"


if __name__ == "__main__":
    manager.run()
