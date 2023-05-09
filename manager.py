"""
相关配置信息：
1. 数据库配置
2. redis配置
3. session配置
4. csrf配置
"""
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


if __name__ == "__main__":

    manager.run()
