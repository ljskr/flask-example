# -*- coding: utf8 -*-

from .views import bp

def module_init(app):
    """
    flask 模块初始化。(注册 blueprint 等)
    """
    app.register_blueprint(bp)

