# -*- coding: utf-8 -*-
# Author: ljskryj@163.com
# Date: 2018-04-16

import logging
from logging.config import dictConfig
import yaml

import config
import webapp

# 初始化 logging
log_config_file = config.LOG_CONFIG_FILE
logging.config.dictConfig(yaml.load(open(log_config_file)))

# 创建 app
app = webapp.create_app(config)

if __name__ == '__main__':
    app.run(host=config.TEST_HOST, port=config.TEST_PORT)
