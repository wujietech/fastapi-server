'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 17:37:48
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 17:36:50
FilePath: /fastapi-server/backend/app/api/routes/workflow.py
Description: 工作流接口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import uuid
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Workflow, WorkflowBase, WorkflowPublic
from app.models.enums import PageSize
from app.models.base import Response, Message
from app.models.workflow import WorkflowDetail, WorkflowList

router = APIRouter(prefix="/workflows", tags=["workflows"])

# 获取工作流列表
@router.get("/", response_model=Response[WorkflowList])
def read_workflows(
    session: SessionDep,
    # current_user: CurrentUser, # 暂时放开权限
    pageNumber: int = 1, 
    pageSize: PageSize = PageSize.medium, 
    cid: Optional[int] = None
) -> Any:
    """
    Retrieve workflows.
    """
    # 暂时放开权限
    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")

    # 构建基础查询
    statement = select(Workflow)
    count_statement = select(func.count()).select_from(Workflow)
    
    # 如果提供了分类ID，添加过滤条件
    if cid is not None:
        statement = statement.where(Workflow.category_id == cid)
        count_statement = count_statement.where(Workflow.category_id == cid)
    
    # 获取总数
    total = session.exec(count_statement).one()
    
    # 添加分页
    offset = (pageNumber - 1) * pageSize
    statement = statement.offset(offset).limit(pageSize)
    
    # 执行查询
    workflows = session.exec(statement).all()

    return Response(data=WorkflowList(
        items=workflows,
        total=total
    ))

# 获取工作流详情
@router.get("/{workflow_id}", response_model=Response[WorkflowDetail])
def read_workflow(
    # session: SessionDep, current_user: CurrentUser, workflow_id: int
    session: SessionDep, workflow_id: int
) -> Any:
    """
    Retrieve a workflow.
    """
    # 暂时放开权限
    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")

    workflow = session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # 转换为 WorkflowDetail 格式
    workflow_detail = WorkflowDetail(
        name=workflow.name,
        description=workflow.description,
        workflow=workflow.workflow  # 工作流内容，使用 workflow 字段
    )
    return Response(data=workflow_detail)

# 创建工作流
@router.post("/", response_model=Response[WorkflowPublic])
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

    return Response(data=workflow)

# 更新工作流
@router.put("/{workflow_id}", response_model=Response[WorkflowPublic])
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

    return Response(data=workflow)

# 删除工作流
@router.delete("/{workflow_id}", response_model=Response[Message])
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

    return Response(data=Message(message="Workflow deleted successfully"))
