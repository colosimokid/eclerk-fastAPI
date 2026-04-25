import uuid
from typing import Any

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    Item,
    ItemCreate,
    Section,
    SectionCreate,
    SectionUpdate,
    SubSection,
    SubSectionCreate,
    SubSectionUpdate,
    Brand,
    BrandCreate,
    BrandUpdate,
    Warehouse,
    WarehouseCreate,
    WarehouseUpdate,
    Bin,
    BinCreate,
    BinUpdate,
    Product,
    ProductCreate,
    ProductUpdate,
    StorageDetail,
    StorageDetailCreate,
    StorageDetailPublic,
    StorageDetailUpdate,
    User,
    UserCreate,
    UserUpdate,
)


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
        verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# Category CRUD
def create_category(*, session: Session, category_create: CategoryCreate) -> Category:
    db_obj = Category.model_validate(category_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_category(
    *, session: Session, db_category: Category, category_in: CategoryUpdate
) -> Any:
    category_data = category_in.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


def get_category_by_id(*, session: Session, category_id: uuid.UUID) -> Category | None:
    statement = select(Category).where(Category.id == category_id)
    return session.exec(statement).first()


def get_categories(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Category]:
    statement = select(Category).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# Section CRUD
def create_section(*, session: Session, section_create: SectionCreate) -> Section:
    db_obj = Section.model_validate(section_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_section(
    *, session: Session, db_section: Section, section_in: SectionUpdate
) -> Any:
    section_data = section_in.model_dump(exclude_unset=True)
    db_section.sqlmodel_update(section_data)
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section


def get_section_by_id(*, session: Session, section_id: uuid.UUID) -> Section | None:
    statement = select(Section).where(Section.id == section_id)
    return session.exec(statement).first()


def get_sections(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Section]:
    statement = select(Section).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_sections_by_category(
    *, session: Session, category_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[Section]:
    statement = select(Section).where(Section.category_id == category_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# Brand CRUD

def create_brand(*, session: Session, brand_create: BrandCreate) -> Brand:
    db_obj = Brand.model_validate(brand_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_brand(*, session: Session, db_brand: Brand, brand_in: BrandUpdate) -> Any:
    brand_data = brand_in.model_dump(exclude_unset=True)
    db_brand.sqlmodel_update(brand_data)
    session.add(db_brand)
    session.commit()
    session.refresh(db_brand)
    return db_brand


def get_brands(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Brand]:
    statement = select(Brand).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# SubSection CRUD
def create_sub_section(*, session: Session, sub_section_create: SubSectionCreate) -> SubSection:
    db_obj = SubSection.model_validate(sub_section_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_sub_section(
    *, session: Session, db_sub_section: SubSection, sub_section_in: SubSectionUpdate
) -> Any:
    sub_section_data = sub_section_in.model_dump(exclude_unset=True)
    db_sub_section.sqlmodel_update(sub_section_data)
    session.add(db_sub_section)
    session.commit()
    session.refresh(db_sub_section)
    return db_sub_section


def get_sub_sections(*, session: Session, skip: int = 0, limit: int | None = None) -> list[SubSection]:
    statement = select(SubSection).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_sub_sections_by_section(
    *, session: Session, section_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[SubSection]:
    statement = select(SubSection).where(SubSection.section_id == section_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# Warehouse CRUD
def create_warehouse(*, session: Session, warehouse_create: WarehouseCreate) -> Warehouse:
    db_obj = Warehouse.model_validate(warehouse_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_warehouse(
    *, session: Session, db_warehouse: Warehouse, warehouse_in: WarehouseUpdate
) -> Any:
    warehouse_data = warehouse_in.model_dump(exclude_unset=True)
    db_warehouse.sqlmodel_update(warehouse_data)
    session.add(db_warehouse)
    session.commit()
    session.refresh(db_warehouse)
def get_warehouses(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Warehouse]:
    statement = select(Warehouse).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))
    return session.exec(statement).first()


def get_warehouses(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Warehouse]:
    statement = select(Warehouse).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# Bin CRUD
def create_bin(*, session: Session, bin_create: BinCreate) -> Bin:
    db_obj = Bin.model_validate(bin_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_bin(
    *, session: Session, db_bin: Bin, bin_in: BinUpdate
) -> Any:
    bin_data = bin_in.model_dump(exclude_unset=True)
    db_bin.sqlmodel_update(bin_data)
    session.add(db_bin)
    session.commit()
    session.refresh(db_bin)
    return db_bin


def get_bin_by_id(*, session: Session, bin_id: uuid.UUID) -> Bin | None:
    statement = select(Bin).where(Bin.id == bin_id)
    return session.exec(statement).first()


def get_bins(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Bin]:
    statement = select(Bin).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_bins_by_warehouse(
    *, session: Session, warehouse_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[Bin]:
    statement = select(Bin).where(Bin.warehouse_id == warehouse_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# Product CRUD
def create_product(*, session: Session, product_create: ProductCreate) -> Product:
    db_obj = Product.model_validate(product_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_product(
    *, session: Session, db_product: Product, product_in: ProductUpdate
) -> Any:
    product_data = product_in.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(product_data)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


def get_products(*, session: Session, skip: int = 0, limit: int | None = None) -> list[Product]:
    statement = select(Product).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_product_by_id(*, session: Session, product_id: uuid.UUID) -> Product | None:
    statement = select(Product).where(Product.id == product_id)
    return session.exec(statement).first()


def get_products_by_category(
    *, session: Session, category_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[Product]:
    statement = select(Product).where(Product.category_id == category_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_products_by_section(
    *, session: Session, section_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[Product]:
    statement = select(Product).where(Product.section_id == section_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_products_by_sub_section(
    *, session: Session, sub_section_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[Product]:
    statement = select(Product).where(Product.sub_section_id == sub_section_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def get_products_by_brand(
    *, session: Session, brand_id: uuid.UUID, skip: int = 0, limit: int | None = None
) -> list[Product]:
    statement = select(Product).where(Product.brand_id == brand_id).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


# StorageDetail CRUD

def create_storage_detail(*, session: Session, storage_detail_create: StorageDetailCreate) -> StorageDetail:
    db_obj = StorageDetail.model_validate(storage_detail_create)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_storage_detail(
    *, session: Session, db_storage_detail: StorageDetail, storage_detail_in: StorageDetailUpdate
) -> Any:
    storage_detail_data = storage_detail_in.model_dump(exclude_unset=True)
    db_storage_detail.sqlmodel_update(storage_detail_data)
    session.add(db_storage_detail)
    session.commit()
    session.refresh(db_storage_detail)
    return db_storage_detail
def get_storage_details(

    *, session: Session, skip: int = 0, limit: int | None = None
) -> list[StorageDetail]:
    statement = select(StorageDetail).offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))


def search_storage_details(
    *, session: Session,
    warehouse_id: uuid.UUID | None = None,
    bin_id: uuid.UUID | None = None,
    product_query: str | None = None,
    skip: int = 0,
    limit: int | None = None
) -> list[StorageDetail]:
    from app.models import Bin, Product
    statement = select(StorageDetail).options(selectinload(StorageDetail.product))
    if bin_id:
        statement = statement.where(StorageDetail.bin_id == bin_id)
    elif warehouse_id:
        statement = statement.join(Bin, StorageDetail.bin_id == Bin.id)
        statement = statement.where(Bin.warehouse_id == warehouse_id)
    if product_query:
        statement = statement.join(Product, StorageDetail.product_id == Product.id)
        like = f"%{product_query}%"
        statement = statement.where(
            (Product.codigo.ilike(like)) |
            (Product.referencia.ilike(like)) |
            (Product.descripcion.ilike(like)) |
            (Product.cod_barras_1.ilike(like)) |
            (Product.cod_barras_2.ilike(like))
        )
    statement = statement.offset(skip)
    if limit is not None:
        statement = statement.limit(limit)
    return list(session.exec(statement))
