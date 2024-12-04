#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/11 2:14 上午
@Author : www.mingerzeng@gmail.com
@File : app.py
"""
from flask_cors import CORS
from injector import Injector
from internal.router import Router
from internal.server.http import Http
import dotenv
from config import Config
from .module import ExtensionModule

# 將env加載到環境變量中
dotenv.load_dotenv()

conf = Config()


injector = Injector([ExtensionModule])

app = Http(__name__, conf=conf,router=injector.get(Router))
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

if __name__ == "__main__":
    app.run(host="0.0.0.0",
        port=5000,  # 使用 8080 端口或您需要的端口
        # ssl_context=("cert.pem", "key-no-pass.pem")  # 指定證書和私鑰
    )

