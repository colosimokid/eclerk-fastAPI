import uuid

from sqlmodel import Session

from app import crud
from app.models import (
    BrandCreate,
    CategoryCreate,
    Product,
    ProductCreate,
    ProductUpdate,
    SectionCreate,
    SubSectionCreate,
)
from tests.utils.utils import random_name


def test_create_product(db: Session) -> None:
    # Create dependencies
    category_in = CategoryCreate(nombre=random_name())
    category = crud.create_category(session=db, category_create=category_in)

    section_in = SectionCreate(nombre=random_name(), category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    brand_in = BrandCreate(nombre=random_name())
    brand = crud.create_brand(session=db, brand_create=brand_in)

    codigo = random_name()
    descripcion = random_name()
    product_in = ProductCreate(
        category_id=category.id,
        section_id=section.id,
        codigo=codigo,
        descripcion=descripcion,
        brand_id=brand.id,
    )
    product = crud.create_product(session=db, product_create=product_in)

    assert product.codigo == codigo
    assert product.descripcion == descripcion
    assert product.category_id == category.id
    assert product.section_id == section.id
    assert product.brand_id == brand.id
    assert product.is_active is True
    assert hasattr(product, "id")
    assert isinstance(product.id, uuid.UUID)


def test_update_product(db: Session) -> None:
    # Create dependencies
    category_in = CategoryCreate(nombre=random_name())
    category = crud.create_category(session=db, category_create=category_in)

    section_in = SectionCreate(nombre=random_name(), category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    brand_in = BrandCreate(nombre=random_name())
    brand = crud.create_brand(session=db, brand_create=brand_in)

    codigo = random_name()
    descripcion = random_name()
    product_in = ProductCreate(
        category_id=category.id,
        section_id=section.id,
        codigo=codigo,
        descripcion=descripcion,
        brand_id=brand.id,
    )
    product = crud.create_product(session=db, product_create=product_in)

    new_codigo = random_name()
    new_descripcion = random_name()
    product_update = ProductUpdate(
        codigo=new_codigo, descripcion=new_descripcion, is_active=False
    )
    updated_product = crud.update_product(
        session=db, db_product=product, product_in=product_update
    )

    assert updated_product.codigo == new_codigo
    assert updated_product.descripcion == new_descripcion
    assert updated_product.is_active is False


def test_get_product_by_id(db: Session) -> None:
    # Create dependencies
    category_in = CategoryCreate(nombre=random_name())
    category = crud.create_category(session=db, category_create=category_in)

    section_in = SectionCreate(nombre=random_name(), category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    codigo = random_name()
    descripcion = random_name()
    product_in = ProductCreate(
        category_id=category.id,
        section_id=section.id,
        codigo=codigo,
        descripcion=descripcion,
    )
    product = crud.create_product(session=db, product_create=product_in)

    retrieved_product = crud.get_product_by_id(session=db, product_id=product.id)
    assert retrieved_product is not None
    assert retrieved_product.id == product.id
    assert retrieved_product.codigo == codigo
    assert retrieved_product.descripcion == descripcion


def test_get_products(db: Session) -> None:
    # Create dependencies
    category_in = CategoryCreate(nombre=random_name())
    category = crud.create_category(session=db, category_create=category_in)

    section_in = SectionCreate(nombre=random_name(), category_id=category.id)
    section = crud.create_section(session=db, section_create=section_in)

    products = []
    for _ in range(3):
        codigo = random_name()
        descripcion = random_name()
        product_in = ProductCreate(
            category_id=category.id,
            section_id=section.id,
            codigo=codigo,
            descripcion=descripcion,
        )
        products.append(crud.create_product(session=db, product_create=product_in))

    retrieved_products = crud.get_products(session=db)
    assert len(retrieved_products) >= 3
    created_ids = {product.id for product in products}
    retrieved_ids = {product.id for product in retrieved_products}
    assert created_ids.issubset(retrieved_ids)