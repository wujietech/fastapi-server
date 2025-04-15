from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .workflow import Workflow


class WorkflowLogBase(SQLModel):
    workflow_version: int
    params: str = Field(max_length=100)
    result: str
    status: int = Field(default=0)
    retry: int = Field(default=0)
    reason: Optional[int] = None
    reason_text: Optional[str] = Field(default=None, max_length=100)
    client_time: datetime


class WorkflowLog(WorkflowLogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workflow_id: int = Field(foreign_key="workflow.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    workflow: Optional["Workflow"] = Relationship(back_populates="logs") 