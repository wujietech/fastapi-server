'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:22:13
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-15 18:07:12
FilePath: /fastapi-server/backend/app/api/main.py
Description: API 路由入口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from fastapi import APIRouter

from app.api.routes import items, login, private, users, utils, category, workflow, workflow_log
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(category.router)
api_router.include_router(workflow.router)
api_router.include_router(workflow_log.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
