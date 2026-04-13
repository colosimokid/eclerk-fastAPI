import uuid

from sqlmodel import Session

from app import crud
from app.models import CategoryCreate, SectionCreate, SubSection, SubSectionCreate, SubSectionUpdate
from tests.utils.utils import random_name


def test_create_sub_section(db: Session) -> None:
    # Create a category and section first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    section_nombre = random_name()
    section_in = SectionCreate(nombre=section_nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    nombre = random_name()
    sub_section_in = SubSectionCreate(nombre=nombre, section_id=section.id)
    sub_section = crud.create_sub_section(session=db, sub_section_create=sub_section_in)
    assert sub_section.nombre == nombre
    assert sub_section.section_id == section.id
    assert sub_section.is_active is True
    assert hasattr(sub_section, "id")


def test_update_sub_section(db: Session) -> None:
    # Create a category and section first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    section_nombre = random_name()
    section_in = SectionCreate(nombre=section_nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    nombre = random_name()
    sub_section_in = SubSectionCreate(nombre=nombre, section_id=section.id)
    sub_section = crud.create_sub_section(session=db, sub_section_create=sub_section_in)

    new_nombre = random_name()
    sub_section_update = SubSectionUpdate(nombre=new_nombre, is_active=False)
    updated_sub_section = crud.update_sub_section(
        session=db, db_sub_section=sub_section, sub_section_in=sub_section_update
    )
    assert updated_sub_section.nombre == new_nombre
    assert updated_sub_section.is_active is False


def test_get_sub_section_by_id(db: Session) -> None:
    # Create a category and section first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    section_nombre = random_name()
    section_in = SectionCreate(nombre=section_nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    nombre = random_name()
    sub_section_in = SubSectionCreate(nombre=nombre, section_id=section.id)
    sub_section = crud.create_sub_section(session=db, sub_section_create=sub_section_in)

    retrieved_sub_section = crud.get_sub_section_by_id(session=db, sub_section_id=sub_section.id)
    assert retrieved_sub_section
    assert retrieved_sub_section.id == sub_section.id
    assert retrieved_sub_section.nombre == nombre
    assert retrieved_sub_section.section_id == section.id


def test_get_sub_sections(db: Session) -> None:
    # Create a category and section first
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    section_nombre = random_name()
    section_in = SectionCreate(nombre=section_nombre, category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    # Create multiple sub_sections
    sub_sections = []
    for _ in range(3):
        nombre = random_name()
        sub_section_in = SubSectionCreate(nombre=nombre, section_id=section.id)
        sub_section = crud.create_sub_section(session=db, sub_section_create=sub_section_in)
        sub_sections.append(sub_section)

    retrieved_sub_sections = crud.get_sub_sections(session=db)
    assert len(retrieved_sub_sections) >= 3
    # Check that our created sub_sections are in the list
    created_ids = {sub.id for sub in sub_sections}
    retrieved_ids = {sub.id for sub in retrieved_sub_sections}
    assert created_ids.issubset(retrieved_ids)


def test_get_sub_sections_by_section(db: Session) -> None:
    # Create a category and two sections
    category_nombre = random_name()
    category_in = CategoryCreate(nombre=category_nombre)
    category = crud.create_category(session=db, category_create=category_in)

    section1_nombre = random_name()
    section1_in = SectionCreate(nombre=section1_nombre, category_id=category.id)
    section1 = crud.create_section(session=db, section_create=section1_in)

    section2_nombre = random_name()
    section2_in = SectionCreate(nombre=section2_nombre, category_id=category.id)
    section2 = crud.create_section(session=db, section_create=section2_in)

    # Create sub_sections for section1
    sub_sections_sec1 = []
    for _ in range(2):
        nombre = random_name()
        sub_section_in = SubSectionCreate(nombre=nombre, section_id=section1.id)
        sub_section = crud.create_sub_section(session=db, sub_section_create=sub_section_in)
        sub_sections_sec1.append(sub_section)

    # Create one sub_section for section2
    nombre = random_name()
    sub_section_in = SubSectionCreate(nombre=nombre, section_id=section2.id)
    sub_section_sec2 = crud.create_sub_section(session=db, sub_section_create=sub_section_in)

    retrieved_sub_sections = crud.get_sub_sections_by_section(session=db, section_id=section1.id)
    assert len(retrieved_sub_sections) == 2
    retrieved_ids = {sub.id for sub in retrieved_sub_sections}
    created_ids = {sub.id for sub in sub_sections_sec1}
    assert created_ids == retrieved_ids