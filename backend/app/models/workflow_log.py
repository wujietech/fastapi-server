'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:53:17
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-17 17:11:34
FilePath: /fastapi-server/backend/app/models/workflow_log.py
Description: 工作流日志模型
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship
from app.models.time import get_beijing_time, BEIJING_TIMEZONE

if TYPE_CHECKING:
    from .workflow import Workflow


class WorkflowLogBase(SQLModel):
    workflow_id: int = Field(foreign_key="workflow.id") # 工作流ID
    workflow_version: int # 工作流版本
    params: str = Field(max_length=100) # 工作流参数
    result: str # 工作流结果
    status: int = Field(default=0) # 工作流状态
    retry: int = Field(default=0) # 重试次数
    reason: Optional[int] = None # 失败原因
    reason_text: Optional[str] = Field(default=None, max_length=100) # 失败原因文本
    client_time: datetime # 客户端时间


class WorkflowLog(WorkflowLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # 工作流日志ID
    created_at: datetime = Field(default_factory=get_beijing_time) # 创建时间
    updated_at: datetime = Field(default_factory=get_beijing_time) # 更新时间
    workflow: Optional["Workflow"] = Relationship(back_populates="logs") # 工作流


class WorkflowLogPublic(WorkflowLogBase):
    id: int # 工作流日志ID
    workflow_id: int # 工作流ID
    created_at: datetime # 创建时间
    updated_at: datetime # 更新时间

class WorkflowLogList(SQLModel):
    items: List[WorkflowLogPublic] # 工作流日志列表
    total: int # 工作流日志总数