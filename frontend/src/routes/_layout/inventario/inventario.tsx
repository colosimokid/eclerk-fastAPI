import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import type { ColumnDef } from "@tanstack/react-table"
import { Search } from "lucide-react"
import { useMemo, useState } from "react"

import { BinsService, type BinPublic } from "@/lib/bins"
import { StorageDetailsService, type StorageDetailPublic } from "@/lib/storage_details"
import { WarehousesService, type WarehousePublic } from "@/lib/warehouses"
import { DataTable } from "@/components/Common/DataTable"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

const ALL = "__all__"

function ShortId({ id }: { id: string }) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <span className="font-mono text-xs text-muted-foreground cursor-default">
            {id.slice(0, 8)}...
          </span>
        </TooltipTrigger>
        <TooltipContent>
          <p className="font-mono text-xs">{id}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

type AppliedFilters = {
  warehouseId: string
  binId: string
  productQuery: string
}

function InventarioContent() {
  const [warehouseId, setWarehouseId] = useState<string>(ALL)
  const [binId, setBinId] = useState<string>(ALL)
  const [productQuery, setProductQuery] = useState<string>("")
  const [appliedFilters, setAppliedFilters] = useState<AppliedFilters | null>(null)

  const { data: warehouses = [] } = useQuery<WarehousePublic[]>({
    queryKey: ["warehouses"],
    queryFn: () => WarehousesService.readWarehouses(),
  })

  const { data: allBins = [] } = useQuery<BinPublic[]>({
    queryKey: ["bins"],
    queryFn: () => BinsService.readBins(),
  })

  const filteredBins = useMemo(
    () => (warehouseId === ALL ? allBins : allBins.filter((b) => b.warehouse_id === warehouseId)),
    [allBins, warehouseId],
  )

  const { data: results = [], isFetching, isSuccess } = useQuery<StorageDetailPublic[]>({
    queryKey: ["storage_details_search", appliedFilters],
    queryFn: () =>
      StorageDetailsService.searchStorageDetails({
        warehouse_id: appliedFilters?.warehouseId === ALL ? null : appliedFilters?.warehouseId,
        bin_id: appliedFilters?.binId === ALL ? null : appliedFilters?.binId,
        product_query: appliedFilters?.productQuery || null,
      }),
    enabled: appliedFilters !== null,
  })

  const binMap = useMemo(
    () => Object.fromEntries(allBins.map((b) => [b.id, b])),
    [allBins],
  )
  const warehouseMap = useMemo(
    () => Object.fromEntries(warehouses.map((w) => [w.id, w])),
    [warehouses],
  )

  const columns = useMemo<ColumnDef<StorageDetailPublic>[]>(
    () => [
      {
        accessorKey: "product_id",
        header: "Producto",
        cell: ({ getValue }) => <ShortId id={getValue<string>()} />,
      },
      {
        id: "bin",
        header: "Ubicación",
        cell: ({ row }) => {
          const bin = binMap[row.original.bin_id]
          return bin ? (
            <span className="font-medium">{bin.nombre}</span>
          ) : (
            <ShortId id={row.original.bin_id} />
          )
        },
      },
      {
        id: "warehouse",
        header: "Depósito",
        cell: ({ row }) => {
          const bin = binMap[row.original.bin_id]
          if (!bin) return <span className="text-muted-foreground">—</span>
          const warehouse = warehouseMap[bin.warehouse_id]
          return warehouse ? (
            <span>{warehouse.nombre}</span>
          ) : (
            <ShortId id={bin.warehouse_id} />
          )
        },
      },
      {
        accessorKey: "qty_on_hand",
        header: "Stock",
        cell: ({ getValue }) => (
          <span className="font-semibold tabular-nums">{getValue<number>()}</span>
        ),
      },
      {
        accessorKey: "qty_order_on_hand",
        header: "En pedido",
        cell: ({ getValue }) => (
          <span className="tabular-nums text-muted-foreground">{getValue<number>()}</span>
        ),
      },
      {
        accessorKey: "date_last_inventory",
        header: "Último inventario",
        cell: ({ getValue }) => {
          const val = getValue<string | null>()
          if (!val) return <span className="text-muted-foreground">—</span>
          return new Date(val).toLocaleDateString("es-VE")
        },
      },
      {
        accessorKey: "is_active",
        header: "Activo",
        cell: ({ getValue }) => (
          <span
            className={
              getValue<boolean>()
                ? "rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-900"
                : "rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700"
            }
          >
            {getValue<boolean>() ? "Sí" : "No"}
          </span>
        ),
      },
    ],
    [binMap, warehouseMap],
  )

  const handleWarehouseChange = (value: string) => {
    setWarehouseId(value)
    setBinId(ALL)
  }

  const handleSearch = () => {
    setAppliedFilters({ warehouseId, binId, productQuery })
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Inventario</h1>
        <p className="text-muted-foreground">
          Consulta el stock disponible por depósito, ubicación o producto.
        </p>
      </div>

      <div className="rounded-xl border bg-card p-6">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4 items-end">
          <div className="flex flex-col gap-1.5">
            <Label htmlFor="warehouse-select">Depósito</Label>
            <Select value={warehouseId} onValueChange={handleWarehouseChange}>
              <SelectTrigger id="warehouse-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ALL}>Todos</SelectItem>
                {warehouses.map((w) => (
                  <SelectItem key={w.id} value={w.id}>
                    {w.nombre}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="bin-select">Ubicación</Label>
            <Select
              value={binId}
              onValueChange={setBinId}
              disabled={filteredBins.length === 0}
            >
              <SelectTrigger id="bin-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value={ALL}>Todas</SelectItem>
                {filteredBins.map((b) => (
                  <SelectItem key={b.id} value={b.id}>
                    {b.nombre}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="flex flex-col gap-1.5">
            <Label htmlFor="product-input">Producto (opcional)</Label>
            <Input
              id="product-input"
              placeholder="Código, descripción, barcode..."
              value={productQuery}
              onChange={(e) => setProductQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
          </div>

          <Button onClick={handleSearch} disabled={isFetching} className="w-full">
            <Search className="mr-2 h-4 w-4" />
            {isFetching ? "Buscando..." : "Buscar"}
          </Button>
        </div>
      </div>

      {appliedFilters === null ? (
        <div className="flex flex-col items-center justify-center text-center py-16 text-muted-foreground">
          <Search className="h-10 w-10 mb-3 opacity-30" />
          <p>Aplica los filtros y presiona Buscar para ver el inventario.</p>
        </div>
      ) : isFetching ? (
        <div className="rounded-xl border p-8 text-center text-muted-foreground">
          Buscando...
        </div>
      ) : isSuccess && results.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-16">
          <div className="rounded-full bg-muted p-4 mb-4">
            <Search className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold">Sin resultados</h3>
          <p className="text-muted-foreground">
            No hay registros de inventario para los filtros seleccionados.
          </p>
        </div>
      ) : (
        <DataTable columns={columns} data={results} />
      )}
    </div>
  )
}

export const Route = createFileRoute("/_layout/inventario/inventario")({
  component: InventarioContent,
})
