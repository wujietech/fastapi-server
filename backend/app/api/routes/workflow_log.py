'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 17:37:48
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-17 17:12:56
FilePath: /fastapi-server/backend/app/api/routes/workflow_log.py
Description: 工作流日志接口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import uuid
from typing import Any
from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import WorkflowLog, WorkflowLogBase, WorkflowLogPublic
from app.models.base import Response, Message
from app.models.workflow_log import WorkflowLogList, BEIJING_TIMEZONE

router = APIRouter(prefix="/workflow-logs", tags=["workflow-logs"])

# 获取工作流日志列表
@router.get("/", response_model=Response[WorkflowLogList])
def read_workflow_logs(
    session: SessionDep, current_user: CurrentUser, pageNumber: int = 1, pageSize: int = 20
) -> Any:
    """
    Retrieve workflow logs.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(WorkflowLog)
        total = session.exec(count_statement).one()
        offset = (pageNumber - 1) * pageSize
        statement = select(WorkflowLog).offset(offset).limit(pageSize)
        workflow_logs = session.exec(statement).all()
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return Response(data=WorkflowLogList(
        items=workflow_logs,
        total=total
    ))

# 获取工作流日志详情
@router.get("/{workflow_log_id}", response_model=Response[WorkflowLogPublic])
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
    return Response(data=workflow_log)

# 创建工作流日志
@router.post("/", response_model=Response[WorkflowLogPublic])
def create_workflow_log(
    session: SessionDep,
    # current_user: CurrentUser, # 暂时关闭权限验证
    workflow_log_in: WorkflowLogBase
) -> Any:
    """
    Create a new workflow log.
    """
    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow_log_data = workflow_log_in.model_dump()
    
    # 处理 params 字段
    if workflow_log_data.get('params'):
        import json
        # 如果是字符串，尝试解析为字典
        if isinstance(workflow_log_data['params'], str):
            try:
                workflow_log_data['params'] = json.loads(workflow_log_data['params'])
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid params JSON format")
        # 如果是字典，转换为 JSON 字符串
        if isinstance(workflow_log_data['params'], dict):
            workflow_log_data['params'] = json.dumps(workflow_log_data['params'])

    # 确保 client_time 是北京时区
    if isinstance(workflow_log_data.get('client_time'), str):
        try:
            client_time = datetime.fromisoformat(workflow_log_data['client_time'].replace('Z', '+00:00'))
            if client_time.tzinfo is None:
                # 如果时间没有时区信息，假定是北京时间
                client_time = client_time.replace(tzinfo=BEIJING_TIMEZONE)
            workflow_log_data['client_time'] = client_time
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid client_time format")

    workflow_log = WorkflowLog(**workflow_log_data)
    session.add(workflow_log)
    session.commit()
    session.refresh(workflow_log)

    return Response(data=WorkflowLogPublic.from_orm(workflow_log))

# 更新工作流日志
@router.put("/{workflow_log_id}", response_model=Response[WorkflowLogPublic])
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

    return Response(data=workflow_log)

# 删除工作流日志
@router.delete("/{workflow_log_id}", response_model=Response[Message])
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

    return Response(data=Message(message="Workflow log deleted successfully"))
