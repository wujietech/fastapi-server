'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:37:45
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 17:16:36
FilePath: /fastapi-server/backend/app/crud/workflow_log.py
Description: 工作流日志 CRUD 操作
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from typing import Optional

from sqlmodel import Session, select

from app.models.workflow_log import WorkflowLog, WorkflowLogBase


class CRUDWorkflowLog:
    def get(self, db: Session, id: int) -> Optional[WorkflowLog]:
        return db.get(WorkflowLog, id)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        workflow_id: Optional[int] = None,
        user_id: Optional[str] = None
    ) -> tuple[list[WorkflowLog], int]:
        statement = select(WorkflowLog)
        if workflow_id:
            statement = statement.where(WorkflowLog.workflow_id == workflow_id)
        if user_id:
            statement = statement.where(WorkflowLog.user_id == user_id)
        statement = statement.offset(skip).limit(limit)
        logs = db.exec(statement).all()
        total = db.exec(select(WorkflowLog)).all().__len__()
        return logs, total

    def create(self, db: Session, *, obj_in: WorkflowLogBase) -> WorkflowLog:
        db_obj = WorkflowLog.model_validate(obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: WorkflowLog,
        obj_in: WorkflowLogBase
    ) -> WorkflowLog:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[WorkflowLog]:
        obj = db.get(WorkflowLog, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_workflow_log = CRUDWorkflowLog() 