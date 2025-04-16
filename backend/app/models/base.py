'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:36:34
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:36:10
FilePath: /fastapi-server/backend/app/models/base.py
Description: 

Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from typing import Any, Dict, List, Optional
from sqlmodel import SQLModel


class Message(SQLModel):
    message: str


class ErrorResponse(SQLModel):
    code: int = 500  # 错误码
    message: str  # 错误信息
    details: Optional[List[Dict[str, Any]]] = None  # 详细错误信息 