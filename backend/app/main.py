'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:22:13
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-15 18:06:58
FilePath: /fastapi-server/backend/app/main.py
Description: 主文件
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import sentry_sdk
from fastapi import FastAPI, Request, status
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.models.base import ErrorResponse


def custom_generate_unique_id(route: APIRoute) -> str:
    """
    Generate a unique ID for the route based on its tag and name.
    If no tag is provided, use 'default' as the tag.
    """
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = []
    for error in exc.errors():
        details.append({
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(ErrorResponse(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="请求参数验证错误",
            details=details
        ))
    )


@app.exception_handler(ResponseValidationError)
async def response_validation_handler(request: Request, exc: ResponseValidationError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(ErrorResponse(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="响应数据验证错误",
            details=[{"msg": str(exc.errors())}]
        ))
    )


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
