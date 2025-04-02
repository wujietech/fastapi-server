'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-02 16:32:19
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-02 17:34:52
FilePath: /server/backend/app/api/main.py
Description: 路由入口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils
from app.core.config import settings

# 主路由
api_router = APIRouter()
api_router.include_router(login.router) # 登录
api_router.include_router(users.router) # 用户
api_router.include_router(utils.router) # 工具
api_router.include_router(items.router) # 商品

# 本地环境才包含私有路由
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
