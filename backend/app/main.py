'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-02 16:32:19
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-02 17:47:11
FilePath: /server/backend/app/main.py
Description: 主文件
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import sentry_sdk
from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

# 如果 SENTRY_DSN 存在且环境不是 local，则初始化 Sentry
if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# 设置所有 CORS 启用的源
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 包含路由，前缀是 API 版本
app.include_router(api_router, prefix=settings.API_V1_STR)
