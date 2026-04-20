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
    Section,
    SectionCreate,
    SectionPublic,
    SectionUpdate,
    Message,
)

router = APIRouter(prefix="/sections", tags=["sections"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=list[SectionPublic],
)
def read_sections(session: SessionDep, skip: int = 0, limit: int | None = None) -> Any:
    """
    Retrieve sections.
    """
    sections = crud.get_sections(session=session, skip=skip, limit=limit)
    return sections


@router.post(
    "/", dependencies=[Depends(get_current_active_superuser)], response_model=SectionPublic
)
def create_section(*, session: SessionDep, section_in: SectionCreate) -> Any:
    """
    Create new section.
    """
    section = crud.create_section(session=session, section_create=section_in)
    return section


@router.get(
    "/{section_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SectionPublic,
)
def read_section_by_id(section_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific section by id.
    """
    section = crud.get_section_by_id(session=session, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section


@router.patch(
    "/{section_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=SectionPublic,
)
def update_section(
    *, session: SessionDep, section_id: uuid.UUID, section_in: SectionUpdate
) -> Any:
    """
    Update a section.
    """
    section = crud.get_section_by_id(session=session, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    update_data = section_in.model_dump(exclude_unset=True)
    section.sqlmodel_update(update_data)
    session.add(section)
    session.commit()
    session.refresh(section)
    return section


@router.delete(
    "/{section_id}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=Message,
)
def delete_section(session: SessionDep, section_id: uuid.UUID) -> Any:
    """
    Delete a section.
    """
    section = crud.get_section_by_id(session=session, section_id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    session.delete(section)
    session.commit()
    return Message(message="Section deleted successfully")