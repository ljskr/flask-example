#-*- coding: utf-8 -*-

import os
import importlib

from flask import Flask

# 定义需加载的模块列表
modules = [
    "webapp.core",
    "webapp.main",
]

def register_module(app):
    """
    注册 module 。 
    每个模块应该在 __init__.py 中定义一个 module_init 方法，模块的 blueprint 需要在该 module_init 方法中注册到 app 里。
    """
    for module_name in modules:
        module = importlib.import_module(module_name)
        if hasattr(module, "module_init"):
            module_init = getattr(module, "module_init")
            # 调用 module_init 方法
            module_init(app)
        else:
            raise Exception("Can not init module '{0}' because it does not have 'module_init' function.".format(module_name))


def create_app(config):
    """
    创建 flask app
    """
    app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER, instance_relative_config=True)

    # 从 config 中加载配置
    app.config.from_object(config)
    # 从 instance 文件夹中加载配置
    app.config.from_pyfile('config.py', silent=True)
    # 从环境变量中获取配置文件路径并加载配置
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    # Load modules
    register_module(app)

    return app


