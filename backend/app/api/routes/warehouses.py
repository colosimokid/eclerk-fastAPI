import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import WarehouseCreate, WarehousePublic, WarehouseUpdate, Message

router = APIRouter(prefix="/warehouses", tags=["warehouse"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[WarehousePublic],
)
def read_warehouses(session: SessionDep, skip: int = 0, limit: int | None = None) -> Any:
    """
    Retrieve warehouses.
    """
    warehouses = crud.get_warehouses(session=session, skip=skip, limit=limit)
    return warehouses


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=WarehousePublic
)
def create_warehouse(*, session: SessionDep, warehouse_in: WarehouseCreate) -> Any:
    """
    Create new warehouse.
    """
    warehouse = crud.create_warehouse(session=session, warehouse_create=warehouse_in)
    return warehouse


@router.get(
    "/{warehouse_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=WarehousePublic,
)
def read_warehouse_by_id(warehouse_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific warehouse by id.
    """
    warehouse = crud.get_warehouse_by_id(session=session, warehouse_id=warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    return warehouse


@router.patch(
    "/{warehouse_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=WarehousePublic,
)
def update_warehouse(
    *, session: SessionDep, warehouse_id: uuid.UUID, warehouse_in: WarehouseUpdate
) -> Any:
    """
    Update a warehouse.
    """
    warehouse = crud.get_warehouse_by_id(session=session, warehouse_id=warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    update_data = warehouse_in.model_dump(exclude_unset=True)
    warehouse.sqlmodel_update(update_data)
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)
    return warehouse


@router.delete(
    "/{warehouse_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_warehouse(session: SessionDep, warehouse_id: uuid.UUID) -> Any:
    """
    Delete a warehouse.
    """
    warehouse = crud.get_warehouse_by_id(session=session, warehouse_id=warehouse_id)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    session.delete(warehouse)
    session.commit()
    return Message(message="Warehouse deleted successfully")