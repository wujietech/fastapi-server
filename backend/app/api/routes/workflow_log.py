'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 17:37:48
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-15 18:07:32
FilePath: /fastapi-server/backend/app/api/routes/workflow_log.py
Description: 工作流日志接口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import WorkflowLog, WorkflowLogBase, WorkflowLogPublic, WorkflowLogsPublic, Message

router = APIRouter(prefix="/workflow-log", tags=["workflow-log"])

# 获取工作流日志列表
@router.get("/", response_model=WorkflowLogsPublic)
def read_workflow_logs(
    session: SessionDep, current_user: CurrentUser, pageNumber: int = 1, pageSize: int = 20
) -> Any:
    """
    Retrieve workflow logs.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(WorkflowLog)
        count = session.exec(count_statement).one()
        offset = (pageNumber - 1) * pageSize
        statement = select(WorkflowLog).offset(offset).limit(pageSize)
        workflow_logs = session.exec(statement).all()
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return WorkflowLogsPublic(data=workflow_logs, count=count)

# 获取工作流日志详情
@router.get("/{workflow_log_id}", response_model=WorkflowLogPublic)
def read_workflow_log(
    session: SessionDep, current_user: CurrentUser, workflow_log_id: int
) -> Any:
    """
    Retrieve a workflow log.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow_log = session.get(WorkflowLog, workflow_log_id)
    if not workflow_log:
        raise HTTPException(status_code=404, detail="Workflow log not found")
    return workflow_log

# 创建工作流日志
@router.post("/", response_model=WorkflowLogPublic)
def create_workflow_log(
    session: SessionDep, current_user: CurrentUser, workflow_log_in: WorkflowLogBase
) -> Any:
    """
    Create a new workflow log.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow_log = WorkflowLog(**workflow_log_in.model_dump())
    session.add(workflow_log)
    session.commit()
    session.refresh(workflow_log)

    return workflow_log

# 更新工作流日志
@router.put("/{workflow_log_id}", response_model=WorkflowLogPublic)
def update_workflow_log(
    session: SessionDep, current_user: CurrentUser, workflow_log_id: int, workflow_log_in: WorkflowLogBase
) -> Any:
    """
    Update a workflow log.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow_log = session.get(WorkflowLog, workflow_log_id)
    if not workflow_log:
        raise HTTPException(status_code=404, detail="Workflow log not found")
    
    update_data = workflow_log_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(workflow_log, field, value)
    
    session.add(workflow_log)
    session.commit()
    session.refresh(workflow_log)

    return workflow_log

# 删除工作流日志
@router.delete("/{workflow_log_id}", response_model=Message)
def delete_workflow_log(
    session: SessionDep, current_user: CurrentUser, workflow_log_id: int
) -> Any:
    """
    Delete a workflow log.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow_log = session.get(WorkflowLog, workflow_log_id)
    if not workflow_log:
        raise HTTPException(status_code=404, detail="Workflow log not found")
    session.delete(workflow_log)
    session.commit()

    return {"message": "Workflow log deleted successfully"}
