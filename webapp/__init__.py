#-*- coding: utf-8 -*-
# Author: ljskryj@163.com
# Date: 2018-04-16

import os
import importlib
import logging
import logging.config

from flask import Flask


def register_module(app, modules):
    """
    注册 module 。
    每个模块应该在 __init__.py 中定义一个 module_init 方法，模块的 blueprint 需要在该 module_init 方法中注册到 app 里。
    """
    for module_name in modules:
        app.logger.debug("Load module [%s] start.", module_name)
        module = importlib.import_module(module_name)
        if hasattr(module, "module_init"):
            module_init = getattr(module, "module_init")
            # 调用 module_init 方法
            module_init(app)
            app.logger.debug("Load module [%s] success.", module_name)
        else:
            raise Exception("Can not init module '{0}' because it does not have \
                'module_init' function.".format(module_name))


def create_app(config,
               use_instance_config=True,
               instance_relative_config=True,
               instance_path="instance",
               instance_config_file="config.py",
               use_env_config=True,
               env_config_name="APP_CONFIG_FILE"):
    """
    创建 flask app

    Args:
        config: 配置信息。

        use_instance_config: 是否加载 instance 配置文件，默认 True 。 当设为 False 时， instance 的相关配置会忽略。
        instance_relative_config: 是否使用 instance 目录，默认 True 。
        instance_path: instance 目录。
        instance_config_file: instance 配置文件名。

        use_env_config: 是否加载 环境变量 配置文件，默认 True 。
        env_config_name: 环境变量名称。

        配置文件加载顺序说明： 首先从 config 中获取配置信息，然后从 instance 中获取配置信息，最后从 环境变量 中获取配置信息。
    """

    if use_instance_config:
        package_path = os.getcwd()
        instance_absolute_path = os.path.join(package_path, instance_path)
    else:
        instance_absolute_path = None

    # 加载 log 配置文件
    logging.config.fileConfig(config.LOG_CONFIG_FILE)

    app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER,
                instance_relative_config=instance_relative_config,
                instance_path=instance_absolute_path)
    app.logger.info("App create start.")

    # 从 config 中加载配置
    app.logger.debug("Load config.")
    app.config.from_object(config)
    # 从 instance 文件夹中加载配置
    if use_instance_config:
        ret = app.config.from_pyfile(instance_config_file, silent=True)
        app.logger.debug("Load config from instance file {}.".format("success" if ret else "failed"))
    # 从环境变量中获取配置文件路径并加载配置
    if use_env_config:
        ret = app.config.from_envvar(env_config_name, silent=True)
        app.logger.debug("Load config from environment {}.".format("success" if ret else "failed"))

    # Load modules
    register_module(app, config.MODULES)

    app.logger.info("App create success!")

    return app
