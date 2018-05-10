# -*- coding: utf-8 -*-

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

logger = logging.getLogger()
logger.info("app created!")

if __name__ == '__main__':
    app.run(host=config.TEST_HOST, port=config.TEST_PORT)
