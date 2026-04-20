CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. ALTER para todas las tablas

-- ==================== CATEGORIES ====================
ALTER TABLE public.categories
    ALTER COLUMN id SET DEFAULT uuid_generate_v4();

-- ==================== SECTIONS ====================
ALTER TABLE public.sections
    ALTER COLUMN id SET DEFAULT uuid_generate_v4();



-- ==================== SUB_SECTIONS ====================
ALTER TABLE public.sub_sections
    ALTER COLUMN id SET DEFAULT uuid_generate_v4();



-- ==================== BRANDS ====================
ALTER TABLE public.brands
    ALTER COLUMN id SET DEFAULT uuid_generate_v4();

  -- =============================================
-- SET is_active DEFAULT TRUE en TODAS las tablas
-- =============================================

-- 1. CATEGORIES
ALTER TABLE public.categories
    ALTER COLUMN is_active SET DEFAULT TRUE;

-- 2. SECTIONS
ALTER TABLE public.sections
    ALTER COLUMN is_active SET DEFAULT TRUE;

-- 3. SUB_SECTIONS
ALTER TABLE public.sub_sections
    ALTER COLUMN is_active SET DEFAULT TRUE;

-- 4. BRANDS
ALTER TABLE public.brands
    ALTER COLUMN is_active SET DEFAULT TRUE;

-- =============================================
-- SET DEFAULT CURRENT_TIMESTAMP para created_at y updated_at
-- =============================================

-- 1. CATEGORIES
ALTER TABLE public.categories
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

-- 2. SECTIONS
ALTER TABLE public.sections
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

-- 3. SUB_SECTIONS
ALTER TABLE public.sub_sections
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;

-- 4. BRANDS
ALTER TABLE public.brands
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    ALTER COLUMN updated_at SET DEFAULT CURRENT_TIMESTAMP;


    INSERT INTO public.brands (nombre) VALUES
('PINTAQUIM'),
('NTN'),
('KOYO'),
('UGOOD'),
('SUPERMAXTER'),
('ASTIKA'),
('AZUMAR'),
('RIK'),
('WADFOW'),
('INGCO'),
('COVO'),
('REINCO'),
('DYLLU'),
('TRIC'),
('V-TEG'),
('MASAKI'),
('FERCO'),
('UYUSTOOLS'),
('VINKO'),
('ISONIC'),
('TORINGA'),
('BLACK EAGLE'),
('PARSUN'),
('LOBSTER'),
('RUBI TOOLS'),
('MAXI TOOLS'),
('CARBORUNDUM'),
('SONIHOOKS'),
('CHING FA FISHING'),
('BIG LURE'),
('BIG JIG'),
('THREE YACHTS'),
('JINGWEI'),
('MUSTAD')
ON CONFLICT (nombre) DO NOTHING;

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


INSERT INTO public.sections (nombre, category_id)
SELECT 'PUERTAS', id FROM public.categories WHERE nombre = 'ACABADOS' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'CUBRECAMA', id FROM public.categories WHERE nombre = 'ARTICULOS PARA EL HOGAR' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'TOALLAS', id FROM public.categories WHERE nombre = 'ARTICULOS PARA EL HOGAR' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'EQUIPAMIENTO', id FROM public.categories WHERE nombre = 'AUTOMOTRIZ' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'CABLES ELECTRICOS', id FROM public.categories WHERE nombre = 'ELECTRICIDAD' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'FOCOS E ILUMINACIÓN', id FROM public.categories WHERE nombre = 'ELECTRICIDAD' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'INTERRUPTORES - TOMAS', id FROM public.categories WHERE nombre = 'ELECTRICIDAD' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'TEIPES Y AISLANTES', id FROM public.categories WHERE nombre = 'ELECTRICIDAD' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'TUBERIAS Y ACCESORIOS', id FROM public.categories WHERE nombre = 'ELECTRICIDAD' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'ACCESORIOS P/CONSTRUCCION', id FROM public.categories WHERE nombre = 'FERRETERIA GENERAL' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'IMPERMEABILIZANTES', id FROM public.categories WHERE nombre = 'FERRETERIA GENERAL' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'SEGURIDAD INDUSTRIAL', id FROM public.categories WHERE nombre = 'FERRETERIA GENERAL' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'ACCESORIOS', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'ANCLA', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'ANZUELOS', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'EQUIPOS', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'FLOTADORES', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'HILOS', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'MOTORES FUERA DE BORDA', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'PINTURAS MARINAS', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'REDES DE PESCA', id FROM public.categories WHERE nombre = 'FERRETERIA MARINA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'ELECTRICAS E INALAMBRICAS', id FROM public.categories WHERE nombre = 'HERRAMIENTAS' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'MANUALES', id FROM public.categories WHERE nombre = 'HERRAMIENTAS' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'ANGULOS', id FROM public.categories WHERE nombre = 'HERRERIA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'DISCOS', id FROM public.categories WHERE nombre = 'HERRERIA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'BAÑO', id FROM public.categories WHERE nombre = 'HOGAR' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'COCINA', id FROM public.categories WHERE nombre = 'HOGAR' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'JARDINERIA', id FROM public.categories WHERE nombre = 'HOGAR' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'PINTURAS PARA MADERA', id FROM public.categories WHERE nombre = 'PINTURAS' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'BROCHAS-RODILLOS-ACCESORI', id FROM public.categories WHERE nombre = 'PINTURAS' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'FONDOS ANTICORROSIVOS', id FROM public.categories WHERE nombre = 'PINTURAS' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'SELLANTES', id FROM public.categories WHERE nombre = 'PLOMERIA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;

INSERT INTO public.sections (nombre, category_id)
SELECT 'TORNILLOS', id FROM public.categories WHERE nombre = 'TORNILLERIA' LIMIT 1
ON CONFLICT (nombre, category_id) DO NOTHING;
