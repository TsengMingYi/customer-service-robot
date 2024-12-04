#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/11 1:59 上午
@Author : www.mingerzeng@gmail.com
@File : router.py
"""
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler


    def register_router(self, app: Flask):
        """註冊路由"""
        # 1. 創建一個藍圖
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 2. 將url與對應的控制器方法做綁定
        bp.add_url_rule("/apps/<uuid:app_id>/debug", methods=["POST"], view_func=self.app_handler.debug)
        bp.add_url_rule("/apps/<uuid:app_id>/member", methods=["POST"], view_func=self.app_handler.member)


        # 4. 在應用上去註冊藍圖
        app.register_blueprint(bp)
