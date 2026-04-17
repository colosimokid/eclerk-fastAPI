import logging

from sqlmodel import Session

from app.core.db import engine, init_db
from app import crud
from app.models import WarehouseCreate, BinCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)
        # Preload warehouses and bins
        preload_warehouses_and_bins(session)


def preload_warehouses_and_bins(session: Session) -> None:
    # Check if General warehouse exists
    warehouse = crud.get_warehouses(session=session, limit=1)
    if not warehouse:
        logger.info("Creating initial warehouse: General")
        warehouse_in = WarehouseCreate(
            nombre="General",
            estado="Activo",
            direccion="Av, Juan Bautista Arismendi"
        )
        crud.create_warehouse(session=session, warehouse_create=warehouse_in)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
