# -*- coding: utf8 -*-

import os
import logging

from flask import render_template, send_from_directory

def module_init(app):
    """
    flask 模块初始化。(注册 blueprint 等)
    """

    #logger = logging.getLogger()

    # 定义 favicon.ico 路由
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.errorhandler(500)
    def internal_error(error):
        #logger.error(error)
        return render_template('500.html'), 500

    @app.errorhandler(400)
    def bad_request(error):
        #logger.error(error)
        return render_template('404.html'), 400

    @app.errorhandler(404)
    def not_found(error):
        #logger.warn(error)
        return render_template('404.html'), 404


