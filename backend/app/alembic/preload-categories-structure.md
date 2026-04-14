# Script SQL Completo - Estructura de Categorías (3 tablas)

**Base de datos:** PostgreSQL

**Tablas:** `categories`, `sections`, `sub_sections`

**ID:** UUID con valor por defecto

**Relaciones:** Claves foráneas correctas

**Campos extra:** `is_active`, `created_at`, `updated_at`

> Este script describe la estructura y la precarga inicial de datos para el inicio del proyecto. Es especialmente útil antes de poner el sistema en producción.

---

## 1. Crear extensión UUID (ejecutar una sola vez)

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## 2. Estructura de tablas

```sql
-- =============================================
-- TABLA 1: CATEGORIES (antes Seccion)
-- =============================================
CREATE TABLE IF NOT EXISTS public.categories (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre      VARCHAR(100) NOT NULL UNIQUE,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- TABLA 2: SECTIONS (antes Familia)
-- =============================================
CREATE TABLE IF NOT EXISTS public.sections (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre       VARCHAR(100) NOT NULL,
    category_id  UUID         NOT NULL,
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sections_category 
        FOREIGN KEY (category_id) REFERENCES public.categories(id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,

    CONSTRAINT uq_section_category UNIQUE (nombre, category_id)
);

-- =============================================
-- TABLA 3: SUB_SECTIONS (antes SubFamilia)
-- =============================================
CREATE TABLE IF NOT EXISTS public.sub_sections (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre      VARCHAR(150) NOT NULL,
    section_id  UUID         NOT NULL,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_sub_sections_section 
        FOREIGN KEY (section_id) REFERENCES public.sections(id) 
        ON DELETE RESTRICT ON UPDATE CASCADE,

    CONSTRAINT uq_sub_section_section UNIQUE (nombre, section_id)
);

-- Índices recomendados
CREATE INDEX IF NOT EXISTS idx_sections_category_id   ON public.sections(category_id);
CREATE INDEX IF NOT EXISTS idx_sub_sections_section_id ON public.sub_sections(section_id);
```

---

## 3. Precarga inicial de datos

```sql
INSERT INTO public.categories (nombre) VALUES
('ACABADOS'),
('ARTICULOS PARA EL HOGAR'),
('AUTOMOTRIZ'),
('ELECTRICIDAD'),
('FERRETERIA GENERAL'),
('FERRETERIA MARINA'),
('HERRAMIENTAS'),
('HERRERIA'),
('HOGAR'),
('PINTURAS'),
('PLOMERIA'),
('TORNILLERIA')
ON CONFLICT (nombre) DO NOTHING;
```

```sql
INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'CERRADURAS Y CERROJOS', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'ACABADOS' AND s.nombre = 'PUERTAS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'BARNIZ', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'PINTURAS' AND s.nombre = 'PINTURAS PARA MADERA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'REPUESTOS PARA RODILLO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'PINTURAS' AND s.nombre = 'BROCHAS-RODILLOS-ACCESORI' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'HERRERIA', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'PINTURAS' AND s.nombre = 'FONDOS ANTICORROSIVOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'ESMALTE', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'PINTURAS' AND s.nombre = 'PINTURAS MARINAS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT '40X', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'MOTORES FUERA DE BORDA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT '40G', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'MOTORES FUERA DE BORDA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'DT40', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'MOTORES FUERA DE BORDA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'REPUESTOS', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ACCESORIOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'REZON', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ANCLA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'MONOFILAMENTO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'REDES DE PESCA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'MULTIFILAMENTO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'REDES DE PESCA' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'SEÑUELOS TIPO POTERA', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ANZUELOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'SEÑUELOS DE SEGUIMIENTO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ANZUELOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'SEÑUELOS TIPO TRASTES', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ANZUELOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'ANZUELOS JINGWEI', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ANZUELOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'SALVAVIDAS', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'FLOTADORES' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'BOYAS TIPO DEFENSA', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'FLOTADORES' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'NYLON MONOFIL PESCA', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'HILOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'NYLON MONOFIL REMENDAR', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'HILOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'MECATE DE POLIPROPILENO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'HILOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'MECATE DE POLIETILENO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'HILOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'TENSORES', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ACCESORIOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'POLEAS', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ACCESORIOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'GANCHOS', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ACCESORIOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'PLOMOS', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ACCESORIOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'EQUIPOS DE BUCEO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'ACCESORIOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'RADIO MARINO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'EQUIPOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;

INSERT INTO public.sub_sections (nombre, section_id)
SELECT 'ALMACENAMIENTO', s.id FROM sections s JOIN categories c ON s.category_id = c.id WHERE c.nombre = 'FERRETERIA MARINA' AND s.nombre = 'EQUIPOS' LIMIT 1
ON CONFLICT (nombre, section_id) DO NOTHING;
```

> Luego se van a agregar más inserts de precarga para que lo tengas en cuenta.

---

## 4. Consideraciones importantes

- Este script es para datos precargados al inicio del proyecto y no debería usarse directamente como la única fuente de datos en producción sin validación adicional.
- `updated_at` con `DEFAULT CURRENT_TIMESTAMP` se aplica solo en la inserción. Si se desea actualizar automáticamente en cada modificación, se necesita un trigger o manejo desde la aplicación.
- Asegúrate de ejecutar la extensión `uuid-ossp` antes de crear las tablas si vas a usar `uuid_generate_v4()`.
- Para un entorno de producción sólido, lo ideal es convertir este script en migraciones de Alembic y mantener los datos de carga inicial como seed scripts controlados.
