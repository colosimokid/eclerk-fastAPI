import logging
from sqlmodel import Session, select

from app.core.db import engine
from app import crud
from app.models import (
    Category,
    CategoryCreate,
    Section,
    SectionCreate,
    SubSection,
    SubSectionCreate,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CATEGORIES = [
    "ACABADOS",
    "ARTICULOS PARA EL HOGAR",
    "AUTOMOTRIZ",
    "ELECTRICIDAD",
    "FERRETERIA GENERAL",
    "FERRETERIA MARINA",
    "HERRAMIENTAS",
    "HERRERIA",
    "HOGAR",
    "PINTURAS",
    "PLOMERIA",
    "TORNILLERIA",
]

SECTIONS_BY_CATEGORY = {
    "ACABADOS": ["PUERTAS"],
    "PINTURAS": [
        "PINTURAS PARA MADERA",
        "BROCHAS-RODILLOS-ACCESORI",
        "FONDOS ANTICORROSIVOS",
        "PINTURAS MARINAS",
    ],
    "FERRETERIA MARINA": [
        "MOTORES FUERA DE BORDA",
        "ACCESORIOS",
        "ANCLA",
        "REDES DE PESCA",
        "ANZUELOS",
        "FLOTADORES",
        "HILOS",
        "EQUIPOS",
    ],
}

SUB_SECTIONS_BY_SECTION = {
    ("ACABADOS", "PUERTAS"): ["CERRADURAS Y CERROJOS"],
    ("PINTURAS", "PINTURAS PARA MADERA"): ["BARNIZ"],
    ("PINTURAS", "BROCHAS-RODILLOS-ACCESORI"): ["REPUESTOS PARA RODILLO"],
    ("PINTURAS", "FONDOS ANTICORROSIVOS"): ["HERRERIA"],
    ("PINTURAS", "PINTURAS MARINAS"): ["ESMALTE"],
    ("FERRETERIA MARINA", "MOTORES FUERA DE BORDA"): ["40X", "40G", "DT40"],
    ("FERRETERIA MARINA", "ACCESORIOS"): [
        "REPUESTOS",
        "TENSORES",
        "POLEAS",
        "GANCHOS",
        "PLOMOS",
        "EQUIPOS DE BUCEO",
    ],
    ("FERRETERIA MARINA", "ANCLA"): ["REZON"],
    ("FERRETERIA MARINA", "REDES DE PESCA"): ["MONOFILAMENTO", "MULTIFILAMENTO"],
    ("FERRETERIA MARINA", "ANZUELOS"): [
        "SEÑUELOS TIPO POTERA",
        "SEÑUELOS DE SEGUIMIENTO",
        "SEÑUELOS TIPO TRASTES",
        "ANZUELOS JINGWEI",
    ],
    ("FERRETERIA MARINA", "FLOTADORES"): ["SALVAVIDAS", "BOYAS TIPO DEFENSA"],
    ("FERRETERIA MARINA", "HILOS"): [
        "NYLON MONOFIL PESCA",
        "NYLON MONOFIL REMENDAR",
        "MECATE DE POLIPROPILENO",
        "MECATE DE POLIETILENO",
    ],
    ("FERRETERIA MARINA", "EQUIPOS"): ["RADIO MARINO", "ALMACENAMIENTO"],
}


def get_or_create_category(session: Session, nombre: str):
    statement = select(Category).where(Category.nombre == nombre)
    category = session.exec(statement).first()
    if category:
        return category
    return crud.create_category(
        session=session, category_create=CategoryCreate(nombre=nombre)
    )


def get_or_create_section(session: Session, category_id, nombre: str):
    statement = select(Section).where(
        Section.nombre == nombre, Section.category_id == category_id
    )
    section = session.exec(statement).first()
    if section:
        return section
    return crud.create_section(
        session=session,
        section_create=SectionCreate(nombre=nombre, category_id=category_id),
    )


def get_or_create_sub_section(session: Session, section_id, nombre: str):
    statement = select(SubSection).where(
        SubSection.nombre == nombre, SubSection.section_id == section_id
    )
    sub_section = session.exec(statement).first()
    if sub_section:
        return sub_section
    return crud.create_sub_section(
        session=session,
        sub_section_create=SubSectionCreate(nombre=nombre, section_id=section_id),
    )


def preload_categories_sections_sub_sections(session: Session) -> None:
    logger.info("Preloading categories, sections and sub_sections")
    
    # Create categories
    for category_name in CATEGORIES:
        get_or_create_category(session=session, nombre=category_name)

    # Create sections
    for category_name, sections in SECTIONS_BY_CATEGORY.items():
        category = get_or_create_category(session=session, nombre=category_name)
        for section_name in sections:
            get_or_create_section(
                session=session, category_id=category.id, nombre=section_name
            )

    # Create sub_sections
    for (category_name, section_name), sub_names in SUB_SECTIONS_BY_SECTION.items():
        category = get_or_create_category(session=session, nombre=category_name)
        section = session.exec(
            select(Section).where(
                Section.nombre == section_name,
                Section.category_id == category.id,
            )
        ).first()
        if not section:
            logger.warning(
                "No se encontró section %s para category %s",
                section_name,
                category_name,
            )
            continue

        for sub_name in sub_names:
            get_or_create_sub_section(
                session=session, section_id=section.id, nombre=sub_name
            )


def main() -> None:
    logger.info("Seeding categories, sections y sub_sections")
    with Session(engine) as session:
        preload_categories_sections_sub_sections(session)
    logger.info("Seed de categorías completado")


if __name__ == "__main__":
    main()