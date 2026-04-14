import uuid

from sqlmodel import Session

from app import crud
from app.models import Brand, BrandCreate, BrandUpdate
from tests.utils.utils import random_name


def test_create_brand(db: Session) -> None:
    nombre = random_name()
    brand_in = BrandCreate(nombre=nombre)
    brand = crud.create_brand(session=db, brand_create=brand_in)

    assert brand.nombre == nombre
    assert brand.is_active is True
    assert hasattr(brand, "id")
    assert isinstance(brand.id, uuid.UUID)


def test_update_brand(db: Session) -> None:
    nombre = random_name()
    brand_in = BrandCreate(nombre=nombre)
    brand = crud.create_brand(session=db, brand_create=brand_in)

    new_nombre = random_name()
    brand_update = BrandUpdate(nombre=new_nombre, is_active=False)
    updated_brand = crud.update_brand(session=db, db_brand=brand, brand_in=brand_update)

    assert updated_brand.nombre == new_nombre
    assert updated_brand.is_active is False


def test_get_brand_by_id(db: Session) -> None:
    nombre = random_name()
    brand_in = BrandCreate(nombre=nombre)
    brand = crud.create_brand(session=db, brand_create=brand_in)

    retrieved_brand = crud.get_brand_by_id(session=db, brand_id=brand.id)
    assert retrieved_brand is not None
    assert retrieved_brand.id == brand.id
    assert retrieved_brand.nombre == nombre


def test_get_brands(db: Session) -> None:
    brands = []
    for _ in range(3):
        nombre = random_name()
        brand_in = BrandCreate(nombre=nombre)
        brands.append(crud.create_brand(session=db, brand_create=brand_in))

    retrieved_brands = crud.get_brands(session=db)
    assert len(retrieved_brands) >= 3
    created_ids = {brand.id for brand in brands}
    retrieved_ids = {brand.id for brand in retrieved_brands}
    assert created_ids.issubset(retrieved_ids)
