from fastapi import APIRouter

from app.api.routes import bins, brands, categories, items, login, private, sections, sub_sections, users, utils, warehouses
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(categories.router)
api_router.include_router(brands.router)
api_router.include_router(sections.router)
api_router.include_router(sub_sections.router)
api_router.include_router(warehouses.router)
api_router.include_router(bins.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
