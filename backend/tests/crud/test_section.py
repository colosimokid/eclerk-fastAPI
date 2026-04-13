import uuid

from sqlmodel import Session

from app import crud
from app.models import CategoryCreate, Section, SectionCreate, SectionUpdate
from tests.utils.utils import random_name


def test_create_section(db: Session) -> None:
    # Create a category first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    nombre = random_name()
    section_in = SectionCreate(nombre=nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)
    assert section.nombre == nombre
    assert section.category_id == category.id
    assert section.is_active is True
    assert hasattr(section, "id")


def test_update_section(db: Session) -> None:
    # Create a category first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    nombre = random_name()
    section_in = SectionCreate(nombre=nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    new_nombre = random_name()
    section_update = SectionUpdate(nombre=new_nombre, is_active=False)
    updated_section = crud.update_section(
        session=db, db_section=section, section_in=section_update
    )
    assert updated_section.nombre == new_nombre
    assert updated_section.is_active is False


def test_get_section_by_id(db: Session) -> None:
    # Create a category first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    nombre = random_name()
    section_in = SectionCreate(nombre=nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    retrieved_section = crud.get_section_by_id(session=db, section_id=section.id)
    assert retrieved_section
    assert retrieved_section.id == section.id
    assert retrieved_section.nombre == nombre
    assert retrieved_section.category_id == category.id


def test_get_sections(db: Session) -> None:
    # Create a category first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    # Create multiple sections
    sections = []
    for _ in range(3):
        nombre = random_name()
        section_in = SectionCreate(nombre=nombre, category_id=category.id)
        section = crud.create_section(session=db, section_create=section_in)
        sections.append(section)

    retrieved_sections = crud.get_sections(session=db)
    assert len(retrieved_sections) >= 3
    # Check that our created sections are in the list
    created_ids = {sec.id for sec in sections}
    retrieved_ids = {sec.id for sec in retrieved_sections}
    assert created_ids.issubset(retrieved_ids)


def test_get_sections_by_category(db: Session) -> None:
    # Create two categories
    category1_nombre = random_name()
    category1_in = CategoryCreate(nombre=category1_nombre)
    category1 = crud.create_category(session=db, category_create=category1_in)

    category2_nombre = random_name()
    category2_in = CategoryCreate(nombre=category2_nombre)
    category2 = crud.create_category(session=db, category_create=category2_in)

    # Create sections for category1
    sections_cat1 = []
    for _ in range(2):
        nombre = random_name()
        section_in = SectionCreate(nombre=nombre, category_id=category1.id)
        section = crud.create_section(session=db, section_create=section_in)
        sections_cat1.append(section)

    # Create one section for category2
    nombre = random_name()
    section_in = SectionCreate(nombre=nombre, category_id=category2.id)
    section_cat2 = crud.create_section(session=db, section_create=section_in)

    retrieved_sections = crud.get_sections_by_category(session=db, category_id=category1.id)
    assert len(retrieved_sections) == 2
    retrieved_ids = {sec.id for sec in retrieved_sections}
    created_ids = {sec.id for sec in sections_cat1}
    assert created_ids == retrieved_ids