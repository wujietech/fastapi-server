'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:48:23
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-15 17:21:05
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
    name: str = Field(max_length=30, unique=True)
    description: str = Field(max_length=100)
    needLogin: int = Field(default=0)
    params: dict = Field(default={}, sa_type=JSONB)
    version: int = Field(default=1)
    workflow: dict = Field(default={}, sa_type=JSONB)
    icon: str = Field(default="", max_length=100)
    invalid: int = Field(default=0)
    ratelimit: int = Field(default=60)


class Workflow(WorkflowBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id", default=1)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    category: Optional["Category"] = Relationship(back_populates="workflows")
    logs: List["WorkflowLog"] = Relationship(back_populates="workflow")
