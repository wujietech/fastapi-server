'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:37:45
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:46:02
FilePath: /fastapi-server/backend/app/crud/category.py
Description: 分类 CRUD 操作
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from typing import Optional

from sqlmodel import Session, select

from app.models.category import Category, CategoryBase


class CRUDCategory:
    def get(self, db: Session, id: int) -> Optional[Category]:
        return db.get(Category, id)

    def get_by_name(self, db: Session, name: str) -> Optional[Category]:
        return db.exec(select(Category).where(Category.name == name)).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Category], int]:
        statement = select(Category).offset(skip).limit(limit)
        categories = db.exec(statement).all()
        total = db.exec(select(Category)).all().__len__()
        return categories, total

    def create(self, db: Session, *, obj_in: CategoryBase) -> Category:
        db_obj = Category.model_validate(obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Category,
        obj_in: CategoryBase
    ) -> Category:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Category]:
        obj = db.get(Category, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_category = CRUDCategory() 