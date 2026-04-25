# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**eclerk** is a billing and inventory management system. Backend in FastAPI, frontend in React + TypeScript. Currently implemented: products, inventory, warehouses/bins, categories hierarchy, brands, users/roles. Pending: invoicing, accounts receivable, chart of accounts, dispatch guides, configurable taxes/rates.

## Commands

### Backend (run from `backend/`)

```bash
# Install dependencies
uv sync

# Run dev server
fastapi dev app/main.py

# Linting / formatting
ruff check .
ruff format .

# Type checking
mypy app

# Run all tests
pytest

# Run a single test file
pytest tests/crud/test_product.py

# Run a single test function
pytest tests/crud/test_product.py::test_create_product

# DB migrations
alembic upgrade head
alembic revision --autogenerate -m "description"
```

### Frontend (run from `frontend/`)

```bash
# Install dependencies
bun install

# Dev server (http://localhost:5173)
bun dev

# Build
bun build

# Lint + format (Biome)
bun lint

# Regenerate API client from OpenAPI schema
bun generate-client

# E2E tests
bun test
bun test:ui   # with Playwright UI
```

### Full stack (root)

```bash
docker compose up      # starts backend + frontend + postgres + mailcatcher
docker compose down
```

## Architecture

### Backend

All backend code lives in `backend/app/`.

**Data flow:** `models.py` → `crud.py` → `api/routes/<entity>.py` → registered in `api/main.py`

- **`models.py`** — Single file with all SQLModel table definitions and Pydantic schemas. Each entity has: `EntityBase`, `EntityCreate`, `EntityUpdate`, `EntityPublic` (response shape), and `Entity` (table=True).
- **`crud.py`** — Single file with all DB operations. Functions use `Session` from SQLModel and follow the pattern `get_<entity>`, `create_<entity>`, `update_<entity>`, `delete_<entity>`.
- **`api/routes/<entity>.py`** — One file per entity. All routes currently require `get_current_active_superuser` via `Depends`. `SessionDep` and `CurrentUser` are type aliases in `api/deps.py`.
- **`api/main.py`** — Aggregates all routers. `private.py` router is only included when `ENVIRONMENT=local`.
- **`core/config.py`** — `Settings` reads from root `.env` (one level above `backend/`). All config accessed via `settings` singleton.

**IDs:** All primary keys are `uuid.UUID` with `default_factory=uuid.uuid4`.

**Timestamps:** Use `get_datetime_utc()` helper and `sa_type=DateTime(timezone=True)` for timezone-aware columns.

**Migrations:** One Alembic revision per new table/change, in `backend/app/alembic/versions/`.

### Frontend

All frontend code lives in `frontend/src/`.

**Data flow:** `client/` (generated) → `lib/<entity>.ts` (axios wrappers + types) → `components/<Domain>/` → `routes/<page>.tsx`

- **`client/`** — Auto-generated from `openapi.json` via `@hey-api/openapi-ts`. **Never edit manually.** Regenerate with `bun generate-client` after backend changes.
- **`lib/<entity>.ts`** — Hand-written axios helpers with manual TypeScript types (duplicates what the generated client has, but more ergonomic). Auth token read from `localStorage.getItem("access_token")`.
- **`routes/`** — File-based routing via TanStack Router. Each route file exports a `Route` created with `createFileRoute`.
- **`components/<Domain>/`** — Components grouped by domain (Admin, General, Hierarchy, Items, Pending, Sidebar, UserSettings). Each entity typically has: `Add<Entity>`, `Edit<Entity>`, `Delete<Entity>`, `<Entity>ActionsMenu`, and a `columns.tsx` for the data table.
- **`hooks/useAuth.ts`** — Auth state and login/logout logic. Token stored in `localStorage`.
- **`components/Common/DataTable.tsx`** — Shared table component used across all entity pages with TanStack Table.

**Forms:** react-hook-form + Zod for validation. Zod schemas defined inline in the component file.

**API calls:** TanStack Query (`useQuery`, `useMutation`) wraps calls from `lib/` helpers. Toasts via `sonner` / `useCustomToast` hook.

**UI:** shadcn/ui components in `components/ui/` (Radix UI primitives + Tailwind). Theme via `next-themes`.

## Project Skills

These rules apply at all times when working in this repository.

### FastAPI Expert Pattern-Follower (backend)

- Follow CRUD patterns in `backend/app/crud.py`. Do not invent new architectural patterns unless explicitly requested.
- Follow the Alembic migration pattern in `backend/app/alembic/versions/`.
- **Foreign keys must use the actual table name**, not the Python class name. Example: `Field(foreign_key="warehouses.id")`, never `Field(foreign_key="Warehouse.id")`. This avoids `NoForeignKeysError`.
- For seed/preload data, follow the SQL style in `backend/app/alembic/preload-categories-structure.md` and `preload-warehouses-structure.md`.
- Docker is run by the user in their terminal — do not generate or run docker commands.

### React Expert Pattern-Follower (frontend)

- Follow existing UI patterns in `frontend/src/components/` — table layouts and create/edit/delete forms.
- Use `frontend/src/routes/` as the source of page structure.
- Do not use the `Jerarquia` sidebar item as a design example unless explicitly asked.
- Validate data contracts against `http://localhost:8000/docs`.
- All backend endpoints are prefixed with `/api/v1` (e.g., `/api/v1/brands`).
- In data tables, display UUIDs as first 8 characters + "..." with a tooltip showing the full UUID.
- In API queries, do not set a default limit — allow unlimited results.
- Docker is run by the user in their terminal — do not generate or run docker commands.

---

### Adding a New Module (pattern to follow)

1. Add models to `backend/app/models.py` (Base, Create, Update, Public, table class)
2. Add CRUD functions to `backend/app/crud.py`
3. Create `backend/app/api/routes/<entity>.py` with APIRouter
4. Register router in `backend/app/api/main.py`
5. Run `alembic revision --autogenerate -m "add <entity> table"` and `alembic upgrade head`
6. Export OpenAPI schema and run `bun generate-client` in frontend
7. Create `frontend/src/lib/<entity>.ts` with axios helpers and TypeScript types
8. Create `frontend/src/components/<Domain>/` with Add/Edit/Delete/ActionsMenu/columns
9. Add route file in `frontend/src/routes/`
