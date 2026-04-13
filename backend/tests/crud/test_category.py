import uuid

from sqlmodel import Session

from app import crud
from app.models import Category, CategoryCreate, CategoryUpdate
from tests.utils.utils import random_name


def test_create_category(db: Session) -> None:
    nombre = random_name()
    category_in = CategoryCreate(nombre=nombre)
    category = crud.create_category(session=db, category_create=category_in)
    assert category.nombre == nombre
    assert category.is_active is True
    assert hasattr(category, "id")


def test_update_category(db: Session) -> None:
    nombre = random_name()
    category_in = CategoryCreate(nombre=nombre)
    category = crud.create_category(session=db, category_create=category_in)

    new_nombre = random_name()
    category_update = CategoryUpdate(nombre=new_nombre, is_active=False)
    updated_category = crud.update_category(
        session=db, db_category=category, category_in=category_update
    )
    assert updated_category.nombre == new_nombre
    assert updated_category.is_active is False


def test_get_category_by_id(db: Session) -> None:
    nombre = random_name()
    category_in = CategoryCreate(nombre=nombre)
    category = crud.create_category(session=db, category_create=category_in)

    retrieved_category = crud.get_category_by_id(session=db, category_id=category.id)
    assert retrieved_category
    assert retrieved_category.id == category.id
    assert retrieved_category.nombre == nombre


def test_get_categories(db: Session) -> None:
    # Create multiple categories
    categories = []
    for _ in range(3):
        nombre = random_name()
        category_in = CategoryCreate(nombre=nombre)
        category = crud.create_category(session=db, category_create=category_in)
        categories.append(category)

    retrieved_categories = crud.get_categories(session=db)
    assert len(retrieved_categories) >= 3
    # Check that our created categories are in the list
    created_ids = {cat.id for cat in categories}
    retrieved_ids = {cat.id for cat in retrieved_categories}
    assert created_ids.issubset(retrieved_ids)