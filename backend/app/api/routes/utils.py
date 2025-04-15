'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:22:13
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-15 17:57:51
FilePath: /fastapi-server/backend/app/api/routes/utils.py
Description: utils 相关接口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser, CurrentUser
from app.models import Message
from app.utils import generate_test_email, send_email

router = APIRouter(prefix="/utils", tags=["utils"])

# 测试邮件发送，需要管理员权限
@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)], # 需要管理员权限
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")

# 健康检查，未登录也能访问
@router.get("/health-check/")
async def health_check() -> bool:
    return True

# 需要登录访问测试
@router.get("/login-protected-route")
def protected_route(current_user: CurrentUser):
    # 如果代码能执行到这里，说明用户已经登录
    return {"message": "You are logged in", "user": current_user}