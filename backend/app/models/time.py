'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-17 17:30:00
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-17 17:30:00
FilePath: /fastapi-server/backend/app/models/time.py
Description: 时间工具模块
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from datetime import datetime
import pytz

# 使用 pytz 获取北京时区
BEIJING_TIMEZONE = pytz.timezone('Asia/Shanghai')

def get_beijing_time():
    """获取北京时间，确保时区信息正确"""
    utc_now = datetime.now(pytz.UTC)  # 先获取 UTC 时间
    return utc_now.astimezone(BEIJING_TIMEZONE)  # 转换为北京时间 