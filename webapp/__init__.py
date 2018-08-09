#-*- coding: utf-8 -*-
# Author: ljskryj@163.com
# Date: 2018-04-16

import os
import importlib
import logging

from flask import Flask


def register_module(app, modules):
    """
    注册 module 。 
    每个模块应该在 __init__.py 中定义一个 module_init 方法，模块的 blueprint 需要在该 module_init 方法中注册到 app 里。
    """
    logger = logging.getLogger()
    for module_name in modules:
        logger.debug("Load module [%s] start.", module_name)
        module = importlib.import_module(module_name)
        if hasattr(module, "module_init"):
            module_init = getattr(module, "module_init")
            # 调用 module_init 方法
            module_init(app)
            logger.debug("Load module [%s] success.", module_name)
        else:
            raise Exception("Can not init module '{0}' because it does not have 'module_init' function.".format(module_name))


def create_app(config):
    """
    创建 flask app
    """
    logger = logging.getLogger()
    logger.info("App create start.")

    app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER, instance_relative_config=True)

    # 从 config 中加载配置
    app.config.from_object(config)
    # 从 instance 文件夹中加载配置
    app.config.from_pyfile('config.py', silent=True)
    # 从环境变量中获取配置文件路径并加载配置
    app.config.from_envvar('APP_CONFIG_FILE', silent=True)

    # Load modules
    register_module(app, config.MODULES)

    logger.info("App create success!")
    return app


