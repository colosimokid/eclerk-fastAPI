# Script SQL Completo - Estructura de Warehouses y Bins

**Base de datos:** PostgreSQL

**Tablas:** `warehouses`, `bins`

**ID:** UUID con valor por defecto

**Relaciones:** Claves foráneas correctas

**Campos extra:** `is_active`, `created_at`, `updated_at`

> Este script describe la estructura y la precarga inicial de datos para warehouses y bins. Es especialmente útil antes de poner el sistema en producción.

---

## 1. Crear extensión UUID (ejecutar una sola vez)

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## 2. Estructura de tablas

```sql
-- =============================================
-- TABLA 1: WAREHOUSES
-- =============================================
CREATE TABLE IF NOT EXISTS public.warehouses (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre      VARCHAR(100) NOT NULL,
    estado      VARCHAR(50) NOT NULL,
    direccion   VARCHAR(255) NOT NULL,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- TABLA 2: BINS
-- =============================================
CREATE TABLE IF NOT EXISTS public.bins (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre       VARCHAR(100) NOT NULL,
    x            VARCHAR(15)  NOT NULL DEFAULT '0',
    y            VARCHAR(15)  NOT NULL DEFAULT '0',
    z            VARCHAR(15)  NOT NULL DEFAULT '0',
    warehouse_id UUID         NOT NULL,
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bins_warehouse
        FOREIGN KEY (warehouse_id) REFERENCES public.warehouses(id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Índices recomendados
CREATE INDEX IF NOT EXISTS idx_warehouses_nombre   ON public.warehouses(nombre);
CREATE INDEX IF NOT EXISTS idx_bins_warehouse_id   ON public.bins(warehouse_id);
```

---

## 3. Precarga inicial de datos

```sql
INSERT INTO public.warehouses (nombre, estado, direccion) VALUES
('General', 'Activo', 'Av, Juan Bautista Arismendi')
ON CONFLICT (nombre) DO NOTHING;
```

```sql
-- Insertar bin para el warehouse General
INSERT INTO public.bins (nombre, x, y, z, warehouse_id)
SELECT 'general', '0', '0', '0', w.id
FROM public.warehouses w
WHERE w.nombre = 'General'
ON CONFLICT DO NOTHING;
```