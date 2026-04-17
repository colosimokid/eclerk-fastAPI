---
name: FastAPI Expert Pattern-Follower
description: |
  Use when working on backend FastAPI features for this project. The assistant should follow installed FastAPI version patterns, existing Alembic migration structure, CRUD logic patterns in backend/app/crud.py, and preload data patterns like backend/app/alembic/preload-categories-structure.md.
---

# FastAPI Expert Pattern-Follower

This skill defines the expected behavior for backend work in this repository.

## What it means

- The project uses `fastapi[standard]` at version `>=0.114.2,<1.0.0`.
- Prefer existing backend patterns in `backend/app/crud.py` for create/read/update/delete behavior.
- Follow the Alembic migration pattern under `backend/app/alembic/versions/` for schema changes.
- Use preload data scripts like `backend/app/alembic/preload-categories-structure.md` when the user asks for initial data seeding.
- Keep initial data preparation ready for production deployment with seed/preload scripts.
- Always use the table name in `Field(foreign_key="table.column")`, not the class name. For example, use `"warehouses.id"` for the `Warehouse` table (where `__tablename__ = "warehouses"`), not `"Warehouse.id"`. This ensures SQLAlchemy can properly resolve foreign key relationships and avoid `NoForeignKeysError`.
- Do not invent new backend patterns or architectural approaches unless explicitly requested.

## Suggested prompts

- "Usa la skill FastAPI Expert Pattern-Follower para agregar una nueva migración y preload de datos siguiendo los patrones actuales."
- "Crea la lógica CRUD de backend según el patrón existente en backend/app/crud.py." 
- "Agrega datos iniciales de preload como en backend/app/alembic/preload-categories-structure.md." 
