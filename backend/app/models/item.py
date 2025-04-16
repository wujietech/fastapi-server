'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:48:23
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 17:35:16
FilePath: /fastapi-server/backend/app/models/item.py
Description: 项目模型
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import uuid
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user import User


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="items")


# Properties to return via API
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemList(SQLModel):
    items: List[ItemPublic] # 项目列表
    total: int # 项目总数 