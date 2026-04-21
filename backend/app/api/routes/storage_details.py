import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app import crud

from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)

from app.models import (
    StorageDetailPublic,
)
from fastapi import Query
router = APIRouter(prefix="/storage_details", tags=["storage_details"])

@router.get(
    "/search",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[StorageDetailPublic],
)
def search_storage_details(
    session: SessionDep,
    warehouse_id: uuid.UUID | None = Query(None),
    bin_id: uuid.UUID | None = Query(None),
    product_query: str | None = Query(None),
    skip: int = 0,
    limit: int | None = None,
) -> Any:
    """
    Search storage details by warehouse, bin, and product fields.
    """
    return crud.search_storage_details(
        session=session,
        warehouse_id=warehouse_id,
        bin_id=bin_id,
        product_query=product_query,
        skip=skip,
        limit=limit,
    )
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import StorageDetailCreate, StorageDetailPublic, StorageDetailUpdate, Message



@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[StorageDetailPublic],
)
def read_storage_details(session: SessionDep, skip: int = 0, limit: int | None = None) -> Any:
    """
    Retrieve storage details.
    """
    storage_details = crud.get_storage_details(session=session, skip=skip, limit=limit)
    return storage_details


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=StorageDetailPublic,
)
def create_storage_detail(*, session: SessionDep, storage_detail_in: StorageDetailCreate) -> Any:
    """
    Create a new storage detail.
    """
    storage_detail = crud.create_storage_detail(
        session=session, storage_detail_create=storage_detail_in
    )
    return storage_detail


@router.get(
    "/{storage_detail_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=StorageDetailPublic,
)
def read_storage_detail_by_id(storage_detail_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific storage detail by id.
    """
    storage_detail = crud.get_storage_detail_by_id(
        session=session, storage_detail_id=storage_detail_id
    )
    if not storage_detail:
        raise HTTPException(status_code=404, detail="Storage detail not found")
    return storage_detail


@router.patch(
    "/{storage_detail_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=StorageDetailPublic,
)
def update_storage_detail(
    *, session: SessionDep, storage_detail_id: uuid.UUID, storage_detail_in: StorageDetailUpdate
) -> Any:
    """
    Update a storage detail.
    """
    storage_detail = crud.get_storage_detail_by_id(
        session=session, storage_detail_id=storage_detail_id
    )
    if not storage_detail:
        raise HTTPException(status_code=404, detail="Storage detail not found")
    updated_storage_detail = crud.update_storage_detail(
        session=session,
        db_storage_detail=storage_detail,
        storage_detail_in=storage_detail_in,
    )
    return updated_storage_detail


@router.delete(
    "/{storage_detail_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_storage_detail(session: SessionDep, storage_detail_id: uuid.UUID) -> Any:
    """
    Delete a storage detail.
    """
    storage_detail = crud.get_storage_detail_by_id(
        session=session, storage_detail_id=storage_detail_id
    )
    if not storage_detail:
        raise HTTPException(status_code=404, detail="Storage detail not found")
    session.delete(storage_detail)
    session.commit()
    return Message(message="Storage detail deleted successfully")
