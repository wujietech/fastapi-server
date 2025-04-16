'''
Author: 李明(liming@inmyshow.com)
Date: 2025-04-15 17:37:48
LastEditors: 李明(liming@inmyshow.com)
LastEditTime: 2025-04-16 15:46:52
FilePath: /fastapi-server/backend/app/api/routes/category.py
Description: 分类接口
Copyright (c) 2025 by 五街科技, All Rights Reserved. 
'''
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Category, CategoryBase, CategoryPublic, CategoriesPublic, Message

router = APIRouter(prefix="/categories", tags=["categories"])

# 获取分类列表
@router.get("/", response_model=CategoriesPublic)
def read_categories(
    session: SessionDep, 
    current_user: CurrentUser, 
    pageNumber: int = Query(default=1, ge=1, description="页码，从1开始"), 
    pageSize: int = Query(default=20, gt=0, le=100, description="每页记录数")
) -> Any:
    """
    Retrieve categories.
    """
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Category)
        count = session.exec(count_statement).one()
        
        # 计算偏移量
        offset = (pageNumber - 1) * pageSize
        statement = select(Category).offset(offset).limit(pageSize)
        categories = session.exec(statement).all()
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return CategoriesPublic(data=categories, count=count)

# 获取分类详情
@router.get("/{category_id}", response_model=CategoryPublic)
def read_category(
    session: SessionDep, current_user: CurrentUser, category_id: int
) -> Any:
    """
    Retrieve a category.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# 创建分类
@router.post("/", response_model=CategoryPublic)
def create_category(
    session: SessionDep, current_user: CurrentUser, category_in: CategoryBase
) -> Any:
    """
    Create a new category.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    category = Category(**category_in.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)

    return category

# 更新分类
@router.put("/{category_id}", response_model=CategoryPublic)
def update_category(
    session: SessionDep, current_user: CurrentUser, category_id: int, category_in: CategoryBase
) -> Any:
    """
    Update a category.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.update(**category_in.model_dump())
    session.commit()
    session.refresh(category)

    return category

# 删除分类
@router.delete("/{category_id}", response_model=Message)
def delete_category(
    session: SessionDep, current_user: CurrentUser, category_id: int
) -> Any:
    """
    Delete a category.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()

    return {"message": "Category deleted successfully"}

