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
    SubSection,
    SubSectionCreate,
    SubSectionPublic,
    SubSectionUpdate,
    Message,
)

router = APIRouter(prefix="/sub-sections", tags=["sub-sections"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[SubSectionPublic],
)
def read_sub_sections(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve sub-sections.
    """
    sub_sections = crud.get_sub_sections(session=session, skip=skip, limit=limit)
    return sub_sections


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=SubSectionPublic
)
def create_sub_section(*, session: SessionDep, sub_section_in: SubSectionCreate) -> Any:
    """
    Create new sub-section.
    """
    sub_section = crud.create_sub_section(session=session, sub_section_create=sub_section_in)
    return sub_section


@router.get(
    "/{sub_section_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SubSectionPublic,
)
def read_sub_section_by_id(sub_section_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific sub-section by id.
    """
    sub_section = crud.get_sub_section_by_id(session=session, sub_section_id=sub_section_id)
    if not sub_section:
        raise HTTPException(status_code=404, detail="Sub-section not found")
    return sub_section


@router.patch(
    "/{sub_section_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SubSectionPublic,
)
def update_sub_section(
    *, session: SessionDep, sub_section_id: uuid.UUID, sub_section_in: SubSectionUpdate
) -> Any:
    """
    Update a sub-section.
    """
    sub_section = crud.get_sub_section_by_id(session=session, sub_section_id=sub_section_id)
    if not sub_section:
        raise HTTPException(status_code=404, detail="Sub-section not found")
    update_data = sub_section_in.model_dump(exclude_unset=True)
    sub_section.sqlmodel_update(update_data)
    session.add(sub_section)
    session.commit()
    session.refresh(sub_section)
    return sub_section


@router.delete(
    "/{sub_section_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_sub_section(session: SessionDep, sub_section_id: uuid.UUID) -> Any:
    """
    Delete a sub-section.
    """
    sub_section = crud.get_sub_section_by_id(session=session, sub_section_id=sub_section_id)
    if not sub_section:
        raise HTTPException(status_code=404, detail="Sub-section not found")
    session.delete(sub_section)
    session.commit()
    return Message(message="Sub-section deleted successfully")