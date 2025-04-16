'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-16 16:40:00
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:40:00
FilePath: /fastapi-server/backend/app/api/errors.py
Description: 错误处理
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.models.base import ErrorResponse


def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    处理请求参数验证错误
    """
    details = []
    for error in exc.errors():
        details.append({
            "loc": error["loc"],  # 错误位置
            "msg": error["msg"],  # 错误信息
            "type": error["type"]  # 错误类型
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(ErrorResponse(
            code=422,
            message="参数验证错误",
            details=details
        ))
    ) 