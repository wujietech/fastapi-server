'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:37:45
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:46:02
FilePath: /fastapi-server/backend/app/crud/workflow.py
Description: 工作流 CRUD 操作
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from typing import Optional

from sqlmodel import Session, select

from app.models.workflow import Workflow, WorkflowBase


class CRUDWorkflow:
    def get(self, db: Session, id: int) -> Optional[Workflow]:
        return db.get(Workflow, id)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None
    ) -> tuple[list[Workflow], int]:
        statement = select(Workflow)
        if category_id:
            statement = statement.where(Workflow.category_id == category_id)
        statement = statement.offset(skip).limit(limit)
        workflows = db.exec(statement).all()
        total = db.exec(select(Workflow)).all().__len__()
        return workflows, total

    def create(self, db: Session, *, obj_in: WorkflowBase) -> Workflow:
        db_obj = Workflow.model_validate(obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Workflow,
        obj_in: WorkflowBase
    ) -> Workflow:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Workflow]:
        obj = db.get(Workflow, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_workflow = CRUDWorkflow() 