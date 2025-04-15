from datetime import datetime
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .workflow import Workflow


class CategoryBase(SQLModel):
    name: str = Field(max_length=30, unique=True)
    description: str = Field(max_length=100)


class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    workflows: List["Workflow"] = Relationship(back_populates="category") 