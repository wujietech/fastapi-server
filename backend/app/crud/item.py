'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:37:45
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:46:02
FilePath: /fastapi-server/backend/app/crud/item.py
Description: 物品 CRUD 操作
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from typing import Any, Dict, Optional, Union

from sqlmodel import Session, select

from app.models.item import Item, ItemCreate, ItemUpdate


class CRUDItem:
    def get(self, db: Session, id: int) -> Optional[Item]:
        return db.get(Item, id)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        owner_id: Optional[int] = None
    ) -> tuple[list[Item], int]:
        statement = select(Item)
        if owner_id:
            statement = statement.where(Item.owner_id == owner_id)
        statement = statement.offset(skip).limit(limit)
        items = db.exec(statement).all()
        total = db.exec(select(Item)).all().__len__()
        return items, total

    def create(
        self,
        db: Session,
        *,
        obj_in: ItemCreate,
        owner_id: int,
    ) -> Item:
        db_obj = Item(
            title=obj_in.title,
            description=obj_in.description,
            owner_id=owner_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Item,
        obj_in: Union[ItemUpdate, Dict[str, Any]]
    ) -> Item:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Item]:
        obj = db.get(Item, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_item = CRUDItem() 