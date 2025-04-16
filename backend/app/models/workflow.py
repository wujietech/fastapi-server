'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:48:23
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 17:30:29
FilePath: /fastapi-server/backend/app/models/workflow.py
Description: 工作流模型
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from .category import Category
    from .workflow_log import WorkflowLog

class WorkflowBase(SQLModel):
    name: str = Field(max_length=30, unique=True) # 工作流名称
    description: str = Field(max_length=100) # 工作流描述
    needLogin: int = Field(default=0) # 是否需要登录
    params: dict = Field(default={}, sa_type=JSONB) # 工作流参数
    version: int = Field(default=1) # 工作流版本
    workflow: dict = Field(default={}, sa_type=JSONB) # 工作流内容
    icon: str = Field(default="", max_length=100) # 工作流图标
    invalid: int = Field(default=0) # 是否失效
    ratelimit: int = Field(default=60) # 调用间隔时长，单位：秒


class Workflow(WorkflowBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id", default=1) # 工作流ID
    created_at: datetime = Field(default_factory=datetime.utcnow) # 创建时间
    updated_at: datetime = Field(default_factory=datetime.utcnow) # 更新时间
    category: Optional["Category"] = Relationship(back_populates="workflows") # 工作流分类
    logs: List["WorkflowLog"] = Relationship(back_populates="workflow") # 工作流日志

class WorkflowPublic(SQLModel):
    id: int # 工作流ID
    name: str # 工作流名称
    description: str # 工作流描述
    needLogin: int # 是否需要登录
    params: dict # 工作流参数
    version: int # 工作流版本
    icon: str # 工作流图标
    invalid: int # 是否失效
    ratelimit: int # 调用间隔时长
    category_id: int # 工作流分类ID
    created_at: datetime # 创建时间
    updated_at: datetime # 更新时间

class WorkflowDetail(SQLModel):
    name: str # 工作流名称
    description: str # 工作流描述
    workflow: dict = Field(default={}, sa_type=JSONB) # 工作流内容

class WorkflowList(SQLModel):
    items: List[WorkflowPublic] # 工作流列表
    total: int # 工作流总数
