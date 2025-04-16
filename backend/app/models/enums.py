'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-16 16:30:00
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:30:10
FilePath: /fastapi-server/backend/app/models/enums.py
Description: 枚举定义
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from enum import IntEnum


class PageSize(IntEnum):
    """页面大小枚举"""
    small = 10  # 小页面
    medium = 20  # 中页面
    large = 50  # 大页面
    extra_large = 100  # 超大页面 