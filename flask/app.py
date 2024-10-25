#!/usr/bin/env python3
# ! -*- coding=utf-8 -*-
'''
**************************************************************
** @Create：2024/2/18 10:35
** @Author：anonymous
** @Description：管理系统后台框架
**************************************************************
'''
# import settings
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager, Command
# from apps import create_app
# # 即使app.py用不到该模型，这里也必须导入模型，否则数据迁移不了
# from apps.car.model import *
# from apps.brand.model import *
# # from apps.permission.model import *
# from apps.role.model import *
# from apps.User.model import User
# from apps.comment.model import *
#
#
# #创建app，通过manager来接管app，不用app.run来启动项目，要用manager.run来启动
# app=create_app()
# manager = Manager(app=app)
#
# #命令行工具配置
# migrate=Migrate(app=app,db=db)
#
# # 对python app.py 新增命令行参数db
# manager.add_command('db', MigrateCommand)
# # 知识点1:命令行输入python app.py welcome egg(参数),就可以执行这个定制命令,运行@manager.command所装饰的函数
#
#
#
# @manager.option('-c', '--config', dest='config_name', default='default')
# def runserver(config_name):
#     app.run(host=settings.Config.SERVER_IP, port=settings.Config.SERVER_PORT)
#
# @manager.option('-h', '--host', dest='host', help='server lisen address,default: 0.0.0.0', default='0.0.0.0')
# @manager.option('-p', '--port', dest='port', help='server lisen port,default: 5000', default=5000)
# def cmd(name, url, host, port):
#     print(name, url, host, port)


# if __name__ == '__main__':
#     manager.run()

import click
import settings
from flask import Flask
from flask_migrate import Migrate
from apps import create_app
# 即使app.py用不到该模型，这里也必须导入模型，否则数据迁移不了
from apps.car.model import *
from apps.brand.model import *
# from apps.permission.model import *
from apps.role.model import *
from apps.User.model import User
from apps.comment.model import *
from flask_cors import CORS

# 创建 app
app = create_app()

# 配置 CORS
# CORS(app, supports_credentials=True, resources={r"/login": {"origins": "http://localhost:5173"}})

# 添加跨域支持
CORS(app, supports_credentials=True)  # 默认允许所有域名跨域访问

# 数据库迁移
migrate = Migrate(app=app, db=db)


# Flask CLI 命令
@app.cli.command("runserver")
@click.option('-c', '--config', default='default', help='配置名称')
@click.option('-h', '--host', default='localhost', help='服务器监听地址，默认: 0.0.0.0')
@click.option('-p', '--port', default=5000, help='服务器监听端口，默认: 5000')
def runserver(config, host, port):
    """运行服务器"""
    if config == 'development':
        app.run(host=settings.DevelopmentConfig.SERVER_IP, port=5000)
    else:
        app.run(host=settings.ProductionConfig.SERVER_IP, port=5000)

if __name__ == '__main__':
    app.run()