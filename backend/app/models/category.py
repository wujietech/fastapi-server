'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:48:23
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-17 17:47:19
FilePath: /fastapi-server/backend/app/models/category.py
Description: 分类模型
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship
from app.models.time import get_beijing_time
from pydantic import ConfigDict

if TYPE_CHECKING:
    from .workflow import Workflow

class CategoryBase(SQLModel):
    name: str = Field(max_length=30, unique=True) # 分类名称
    description: str = Field(max_length=100) # 分类描述


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # 分类ID
    created_at: datetime = Field(default_factory=get_beijing_time) # 创建时间
    updated_at: datetime = Field(default_factory=get_beijing_time) # 更新时间
    workflows: List["Workflow"] = Relationship(back_populates="category") # 工作流列表
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }
    )

class CategoryPublic(CategoryBase):
    id: int # 分类ID
    created_at: datetime # 创建时间
    updated_at: datetime # 更新时间

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        }
    )


class CategoryList(SQLModel):
    items: List[CategoryPublic] # 分类列表
    total: int # 分类总数