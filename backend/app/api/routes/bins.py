import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import BinCreate, BinPublic, BinUpdate, Message

router = APIRouter(prefix="/bins", tags=["bin"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[BinPublic],
)
def read_bins(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve bins.
    """
    bins = crud.get_bins(session=session, skip=skip, limit=limit)
    return bins


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=BinPublic
)
def create_bin(*, session: SessionDep, bin_in: BinCreate) -> Any:
    """
    Create new bin.
    """
    bin_obj = crud.create_bin(session=session, bin_create=bin_in)
    return bin_obj


@router.get(
    "/{bin_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=BinPublic,
)
def read_bin_by_id(bin_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific bin by id.
    """
    bin_obj = crud.get_bin_by_id(session=session, bin_id=bin_id)
    if not bin_obj:
        raise HTTPException(status_code=404, detail="Bin not found")
    return bin_obj


@router.patch(
    "/{bin_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=BinPublic,
)
def update_bin(
    *, session: SessionDep, bin_id: uuid.UUID, bin_in: BinUpdate
) -> Any:
    """
    Update a bin.
    """
    bin_obj = crud.get_bin_by_id(session=session, bin_id=bin_id)
    if not bin_obj:
        raise HTTPException(status_code=404, detail="Bin not found")
    update_data = bin_in.model_dump(exclude_unset=True)
    bin_obj.sqlmodel_update(update_data)
    session.add(bin_obj)
    session.commit()
    session.refresh(bin_obj)
    return bin_obj


@router.delete(
    "/{bin_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_bin(session: SessionDep, bin_id: uuid.UUID) -> Any:
    """
    Delete a bin.
    """
    bin_obj = crud.get_bin_by_id(session=session, bin_id=bin_id)
    if not bin_obj:
        raise HTTPException(status_code=404, detail="Bin not found")
    session.delete(bin_obj)
    session.commit()
    return Message(message="Bin deleted successfully")


@router.get(
    "/warehouse/{warehouse_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[BinPublic],
)
def read_bins_by_warehouse(warehouse_id: uuid.UUID, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Get bins for a specific warehouse.
    """
    bins = crud.get_bins_by_warehouse(session=session, warehouse_id=warehouse_id, skip=skip, limit=limit)
    return bins