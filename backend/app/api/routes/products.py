import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import ProductCreate, ProductPublic, ProductUpdate, Message

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[ProductPublic],
)
def read_products(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve products.
    """
    products = crud.get_products(session=session, skip=skip, limit=limit)
    return products


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=ProductPublic
)
def create_product(*, session: SessionDep, product_in: ProductCreate) -> Any:
    """
    Create new product.
    """
    product = crud.create_product(session=session, product_create=product_in)
    return product


@router.get(
    "/{product_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProductPublic,
)
def read_product_by_id(product_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific product by id.
    """
    product = crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch(
    "/{product_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ProductPublic,
)
def update_product(
    *, session: SessionDep, product_id: uuid.UUID, product_in: ProductUpdate
) -> Any:
    """
    Update a product.
    """
    product = crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product_in.model_dump(exclude_unset=True)
    product.sqlmodel_update(update_data)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_product(session: SessionDep, product_id: uuid.UUID) -> Any:
    """
    Delete a product.
    """
    product = crud.get_product_by_id(session=session, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return Message(message="Product deleted successfully")