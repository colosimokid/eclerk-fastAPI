-- =============================================
-- CREAR REGISTROS EN storage_details para todos los productos
-- =============================================

INSERT INTO public.storage_details (
    id,
    is_active,
    created_at,
    updated_at,
    product_id,
    bin_id,
    qty_on_hand,
    qty_order_on_hand,
    date_last_inventory
)
SELECT
    uuid_generate_v4() AS id,
    true AS is_active,
    CURRENT_TIMESTAMP AS created_at,
    CURRENT_TIMESTAMP AS updated_at,
    p.id AS product_id,
    b.id AS bin_id,
    floor(random() * 16 + 5)::numeric AS qty_on_hand,   -- Número aleatorio entre 5 y 20
    0 AS qty_order_on_hand,
    CURRENT_TIMESTAMP AS date_last_inventory
FROM public.products p
CROSS JOIN (
    SELECT id
    FROM public.bins
    WHERE nombre = 'Principal'

    LIMIT 1
) b
WHERE b.id IS NOT NULL
  AND NOT EXISTS (
        SELECT 1
        FROM public.storage_details sd
        WHERE sd.product_id = p.id
          AND sd.bin_id = b.id
      )
ON CONFLICT (product_id, bin_id) DO NOTHING;   -- Evita duplicados por la UNIQUE constraint
