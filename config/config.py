#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time   : 2024/8/12 上午9:41
@Author : www.mingerzeng@gmail.com
@File : config.py
"""
import os
from typing import Any
from .default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    """從環境變量中獲取配置項，如果找不到則返回默認值"""
    return os.environ.get(key,DEFAULT_CONFIG.get(key))
    # return os.getenv(key,DEFAULT_CONFIG.get(key))

def _get_bool_env(key : str) -> bool:
    """從環境變量中獲取布爾值型的配置項，如果找不到則返回默認值"""
    value : str = _get_env(key)
    return value.lower() == "true" if value is not None else False

class Config:
    def __init__(self):
        # 關閉wtf的csrf保護
        self.WTF_CSRF_ENABLED = _get_bool_env("WTF_CSRF_ENABLED")
       
        