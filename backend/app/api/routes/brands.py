import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import BrandCreate, BrandPublic, BrandUpdate, Message

router = APIRouter(prefix="/brands", tags=["brands"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[BrandPublic],
)
def read_brands(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve brands.
    """
    brands = crud.get_brands(session=session, skip=skip, limit=limit)
    return brands


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=BrandPublic
)
def create_brand(*, session: SessionDep, brand_in: BrandCreate) -> Any:
    """
    Create new brand.
    """
    brand = crud.create_brand(session=session, brand_create=brand_in)
    return brand


@router.get(
    "/{brand_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=BrandPublic,
)
def read_brand_by_id(brand_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific brand by id.
    """
    brand = crud.get_brand_by_id(session=session, brand_id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.patch(
    "/{brand_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=BrandPublic,
)
def update_brand(
    *, session: SessionDep, brand_id: uuid.UUID, brand_in: BrandUpdate
) -> Any:
    """
    Update a brand.
    """
    brand = crud.get_brand_by_id(session=session, brand_id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    update_data = brand_in.model_dump(exclude_unset=True)
    brand.sqlmodel_update(update_data)
    session.add(brand)
    session.commit()
    session.refresh(brand)
    return brand


@router.delete(
    "/{brand_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_brand(session: SessionDep, brand_id: uuid.UUID) -> Any:
    """
    Delete a brand.
    """
    brand = crud.get_brand_by_id(session=session, brand_id=brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    session.delete(brand)
    session.commit()
    return Message(message="Brand deleted successfully")
