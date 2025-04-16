'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 16:37:45
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 16:46:02
FilePath: /fastapi-server/backend/app/crud/user.py
Description: 用户 CRUD 操作
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
from typing import Any, Dict, Optional, Union

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserCreate, UserUpdate


class CRUDUser:
    def get(self, db: Session, id: int) -> Optional[User]:
        return db.get(User, id)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.exec(select(User).where(User.email == email)).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[User], int]:
        statement = select(User).offset(skip).limit(limit)
        users = db.exec(statement).all()
        total = db.exec(select(User)).all().__len__()
        return users, total

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[User]:
        obj = db.get(User, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


crud_user = CRUDUser() 