'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 17:37:48
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-15 18:07:38
FilePath: /fastapi-server/backend/app/api/routes/workflow.py
Description: 工作流接口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Workflow, WorkflowBase, WorkflowPublic, WorkflowsPublic, Message

router = APIRouter(prefix="/workflow", tags=["workflow"])

# 获取工作流列表
@router.get("/", response_model=WorkflowsPublic)
def read_workflows(
    session: SessionDep, current_user: CurrentUser, pageNumber: int = 1, pageSize: int = 20
) -> Any:
    """
    Retrieve workflows.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Workflow)
        count = session.exec(count_statement).one()
        offset = (pageNumber - 1) * pageSize
        statement = select(Workflow).offset(offset).limit(pageSize)
        workflows = session.exec(statement).all()
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return WorkflowsPublic(data=workflows, count=count)

# 获取工作流详情
@router.get("/{workflow_id}", response_model=WorkflowPublic)
def read_workflow(
    session: SessionDep, current_user: CurrentUser, workflow_id: int
) -> Any:
    """
    Retrieve a workflow.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

# 创建工作流
@router.post("/", response_model=WorkflowPublic)
def create_workflow(
    session: SessionDep, current_user: CurrentUser, workflow_in: WorkflowBase
) -> Any:
    """
    Create a new workflow.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow = Workflow(**workflow_in.model_dump())
    session.add(workflow)
    session.commit()
    session.refresh(workflow)

    return workflow

# 更新工作流
@router.put("/{workflow_id}", response_model=WorkflowPublic)
def update_workflow(
    session: SessionDep, current_user: CurrentUser, workflow_id: int, workflow_in: WorkflowBase
) -> Any:
    """
    Update a workflow.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    update_data = workflow_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workflow, field, value)
    
    session.add(workflow)
    session.commit()
    session.refresh(workflow)

    return workflow

# 删除工作流
@router.delete("/{workflow_id}", response_model=Message)
def delete_workflow(
    session: SessionDep, current_user: CurrentUser, workflow_id: int
) -> Any:
    """
    Delete a workflow.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    session.delete(workflow)
    session.commit()

    return {"message": "Workflow deleted successfully"}
