import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    id_rol: uuid.UUID | None = Field(default=None, foreign_key="role.id")

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    role: Optional["Role"] = Relationship(back_populates="users")


class Role(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=30)
    is_active: bool = True
    users: list["User"] = Relationship(back_populates="role")


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    is_active: bool = True
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    sections: list["Section"] = Relationship(back_populates="category")


class Section(SQLModel, table=True):
    __tablename__ = "sections"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    category_id: uuid.UUID = Field(foreign_key="categories.id")
    is_active: bool = True
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    category: Optional["Category"] = Relationship(back_populates="sections")
    sub_sections: list["SubSection"] = Relationship(back_populates="section")


class SubSection(SQLModel, table=True):
    __tablename__ = "sub_sections"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=150)
    section_id: uuid.UUID = Field(foreign_key="sections.id")
    is_active: bool = True
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    section: Optional["Section"] = Relationship(back_populates="sub_sections")


class Brand(SQLModel, table=True):
    __tablename__ = "brands"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    nombre: str = Field(max_length=100)
    is_active: bool = True
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Category models
class CategoryBase(SQLModel):
    nombre: str = Field(max_length=100)
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    nombre: str | None = Field(default=None, max_length=100)
    is_active: bool | None = Field(default=None)


class CategoryPublic(CategoryBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int


# Section models
class SectionBase(SQLModel):
    nombre: str = Field(max_length=100)
    category_id: uuid.UUID
    is_active: bool = True


class SectionCreate(SectionBase):
    pass


class SectionUpdate(SectionBase):
    nombre: str | None = Field(default=None, max_length=100)
    category_id: uuid.UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class SectionPublic(SectionBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SectionsPublic(SQLModel):
    data: list[SectionPublic]
    count: int


# SubSection models
class SubSectionBase(SQLModel):
    nombre: str = Field(max_length=150)
    section_id: uuid.UUID
    is_active: bool = True


class SubSectionCreate(SubSectionBase):
    pass


class SubSectionUpdate(SubSectionBase):
    nombre: str | None = Field(default=None, max_length=150)
    section_id: uuid.UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class SubSectionPublic(SubSectionBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SubSectionsPublic(SQLModel):
    data: list[SubSectionPublic]
    count: int


# Brand models
class BrandBase(SQLModel):
    nombre: str = Field(max_length=100)
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BrandBase):
    nombre: str | None = Field(default=None, max_length=100)
    is_active: bool | None = Field(default=None)


class BrandPublic(BrandBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BrandsPublic(SQLModel):
    data: list[BrandPublic]
    count: int


# Warehouse models
class WarehouseBase(SQLModel):
    nombre: str = Field(max_length=100)
    estado: str = Field(max_length=50)
    direccion: str = Field(max_length=255)
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(WarehouseBase):
    nombre: str | None = Field(default=None, max_length=100)
    estado: str | None = Field(default=None, max_length=50)
    direccion: str | None = Field(default=None, max_length=255)
    is_active: bool | None = Field(default=None)


class Warehouse(WarehouseBase, table=True):
    __tablename__ = "warehouses"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    bins: list["Bin"] = Relationship(back_populates="warehouse")


class WarehousePublic(WarehouseBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class WarehousesPublic(SQLModel):
    data: list[WarehousePublic]
    count: int


# Bin models
class BinBase(SQLModel):
    nombre: str = Field(max_length=100)
    x: str = Field(max_length=15, default="0")
    y: str = Field(max_length=15, default="0")
    z: str = Field(max_length=15, default="0")
    warehouse_id: uuid.UUID
    is_active: bool = True


class BinCreate(BinBase):
    pass


class BinUpdate(BinBase):
    nombre: str | None = Field(default=None, max_length=100)
    x: str | None = Field(default=None, max_length=15)
    y: str | None = Field(default=None, max_length=15)
    z: str | None = Field(default=None, max_length=15)
    warehouse_id: uuid.UUID | None = Field(default=None)
    is_active: bool | None = Field(default=None)


class Bin(BinBase, table=True):
    __tablename__ = "bins"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    warehouse_id: uuid.UUID = Field(foreign_key="warehouses.id")
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    warehouse: Optional["Warehouse"] = Relationship(back_populates="bins")


class BinPublic(BinBase):
    id: uuid.UUID
    created_at: datetime | None = None
    updated_at: datetime | None = None


class BinsPublic(SQLModel):
    data: list[BinPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)
