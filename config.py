# -*- coding: utf-8 -*-

# 本地开发时监听的 host 和 port
TEST_HOST = "0.0.0.0"
TEST_PORT = 8080

DEBUG = False
TESTING = False
# 日志配置文件
LOG_CONFIG_FILE = "./log.conf"
# 模板目录名
TEMPLATE_FOLDER = "templates"

##############################
# session 相关
##############################
SESSION_TYPE = "filesystem"
SECRET_KEY = '123456'
