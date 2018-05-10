# -*- coding: utf-8 -*-

import os
import json
import logging
import datetime

from flask import Blueprint, request, Response, render_template, redirect, send_from_directory, stream_with_context, g, jsonify

# 创建 blueprint
bp = Blueprint('main', __name__)


@bp.route("/", methods=["GET"])
def root_index():
    return render_template('index.html')

