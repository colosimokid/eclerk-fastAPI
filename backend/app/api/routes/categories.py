import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.models import (
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
    Message,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[CategoryPublic],
)
def read_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve categories.
    """
    categories = crud.get_categories(session=session, skip=skip, limit=limit)
    return categories


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=CategoryPublic
)
def create_category(*, session: SessionDep, category_in: CategoryCreate) -> Any:
    """
    Create new category.
    """
    category = crud.create_category(session=session, category_create=category_in)
    return category


@router.get(
    "/{category_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=CategoryPublic,
)
def read_category_by_id(category_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific category by id.
    """
    category = crud.get_category_by_id(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.patch(
    "/{category_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=CategoryPublic,
)
def update_category(
    *, session: SessionDep, category_id: uuid.UUID, category_in: CategoryUpdate
) -> Any:
    """
    Update a category.
    """
    category = crud.get_category_by_id(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    update_data = category_in.model_dump(exclude_unset=True)
    category.sqlmodel_update(update_data)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete(
    "/{category_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_category(session: SessionDep, category_id: uuid.UUID) -> Any:
    """
    Delete a category.
    """
    category = crud.get_category_by_id(session=session, category_id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return Message(message="Category deleted successfully")