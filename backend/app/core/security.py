'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-02 16:32:19
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-02 17:44:02
FilePath: /server/backend/app/core/security.py
Description: 安全模块
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"

# 创建访问令牌
def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    # 计算过期时间
    expire = datetime.now(timezone.utc) + expires_delta
    # 编码 JWT
    to_encode = {"exp": expire, "sub": str(subject)}
    # 编码 JWT 生成 token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 验证密码
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# 获取密码哈希值
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
