import uuid
from typing import Any

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


def get_categories(*, session: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    statement = select(Category).offset(skip).limit(limit)
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


def get_sections(*, session: Session, skip: int = 0, limit: int = 100) -> list[Section]:
    statement = select(Section).offset(skip).limit(limit)
    return list(session.exec(statement))


def get_sections_by_category(
    *, session: Session, category_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[Section]:
    statement = select(Section).where(Section.category_id == category_id).offset(skip).limit(limit)
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


def get_sub_section_by_id(*, session: Session, sub_section_id: uuid.UUID) -> SubSection | None:
    statement = select(SubSection).where(SubSection.id == sub_section_id)
    return session.exec(statement).first()


def get_sub_sections(*, session: Session, skip: int = 0, limit: int = 100) -> list[SubSection]:
    statement = select(SubSection).offset(skip).limit(limit)
    return list(session.exec(statement))


def get_sub_sections_by_section(
    *, session: Session, section_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[SubSection]:
    statement = select(SubSection).where(SubSection.section_id == section_id).offset(skip).limit(limit)
    return list(session.exec(statement))
