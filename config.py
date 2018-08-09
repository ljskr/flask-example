# -*- coding: utf-8 -*-

##############################
# 基本设置
##############################
# 本地开发时监听的 host 和 port
TEST_HOST = "0.0.0.0"
TEST_PORT = 8080

# Debug 开关
DEBUG = False
# Test 开关
TESTING = False
# 日志配置文件
LOG_CONFIG_FILE = "./log.conf"
# 模板目录名
TEMPLATE_FOLDER = "templates"
# 需要加载的模块列表
MODULES = [
    "webapp.core",
    "webapp.main",
]

##############################
# session 相关
##############################
#SESSION_TYPE = "filesystem"
#SECRET_KEY = '123456'
