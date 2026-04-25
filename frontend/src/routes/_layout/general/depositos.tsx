import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { ChevronDown, ChevronRight, Search } from "lucide-react"
import { Suspense, useMemo, useState } from "react"

import { BinsService, type BinPublic } from "@/lib/bins"
import { WarehousesService, type WarehousePublic } from "@/lib/warehouses"
import { DataTable } from "@/components/Common/DataTable"
import AddBin from "@/components/General/AddBin"
import AddWarehouse from "@/components/General/AddWarehouse"
import { BinActionsMenu } from "@/components/General/BinActionsMenu"
import { columnsWarehouses } from "@/components/General/columnsWarehouses"
import { Button } from "@/components/ui/button"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard"

function getWarehousesQueryOptions() {
  return {
    queryFn: () => WarehousesService.readWarehouses({ skip: 0 }),
    queryKey: ["warehouses"],
  }
}

function getBinsQueryOptions() {
  return {
    queryFn: () => BinsService.readBins({ skip: 0 }),
    queryKey: ["bins"],
  }
}

function CopyId({ id }: { id: string }) {
  const [copiedText, copy] = useCopyToClipboard()
  const isCopied = copiedText === id
  const shortId = id.slice(0, 8) + "..."

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center gap-1.5 group">
            <span className="font-mono text-xs text-muted-foreground">{shortId}</span>
            <Button
              variant="ghost"
              size="icon"
              className="size-6 opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={() => copy(id)}
            >
              {isCopied ? (
                <span className="text-emerald-500">✓</span>
              ) : (
                <span className="text-slate-500">📋</span>
              )}
              <span className="sr-only">Copiar ID</span>
            </Button>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>{id}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

function WarehousesTableContent() {
  const { data: warehouses } = useSuspenseQuery(getWarehousesQueryOptions())
  const { data: bins } = useSuspenseQuery(getBinsQueryOptions())
  const [expandedWarehouseId, setExpandedWarehouseId] = useState<string | null>(null)

  const binsByWarehouse = useMemo(() => {
    return bins.reduce<Record<string, BinPublic[]>>((acc, bin) => {
      if (!acc[bin.warehouse_id]) {
        acc[bin.warehouse_id] = []
      }
      acc[bin.warehouse_id].push(bin)
      return acc
    }, {})
  }, [bins])

  const toggleExpand = (warehouseId: string) => {
    setExpandedWarehouseId((current) =>
      current === warehouseId ? null : warehouseId,
    )
  }

  const warehouseColumns = useMemo(() => {
    return [
      {
        id: "expand",
        header: "",
        cell: ({ row }: { row: { original: WarehousePublic } }) => {
          const expanded = row.original.id === expandedWarehouseId
          return (
            <Button
              variant="ghost"
              size="icon"
              className="p-0"
              onClick={() => toggleExpand(row.original.id)}
            >
              {expanded ? (
                <ChevronDown className="h-4 w-4" />
              ) : (
                <ChevronRight className="h-4 w-4" />
              )}
              <span className="sr-only">
                {expanded ? "Cerrar ubicaciones" : "Ver ubicaciones"}
              </span>
            </Button>
          )
        },
      },
      ...columnsWarehouses,
    ]
  }, [expandedWarehouseId])

  const renderRowDetail = (row: { original: WarehousePublic }) => {
    const warehouseBins = binsByWarehouse[row.original.id] ?? []
    if (expandedWarehouseId !== row.original.id) {
      return null
    }

    return (
      <TableRow>
        <TableCell colSpan={warehouseColumns.length} className="bg-slate-50 dark:bg-slate-800 p-0">
          <div className="rounded-b-lg border border-t-0 border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800">
            <div className="px-4 py-3 text-sm font-semibold text-slate-700 dark:text-slate-300">
              Ubicaciones ({warehouseBins.length})
            </div>
            {warehouseBins.length === 0 ? (
              <div className="px-4 pb-4 text-sm text-muted-foreground">
                No hay ubicaciones para este depósito.
              </div>
            ) : (
              <Table className="mb-0">
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Nombre</TableHead>
                    <TableHead>X</TableHead>
                    <TableHead>Y</TableHead>
                    <TableHead>Z</TableHead>
                    <TableHead>Activo</TableHead>
                    <TableHead className="text-right">Acciones</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {warehouseBins.map((bin) => (
                    <TableRow key={bin.id} className="border-t border-slate-200 dark:border-slate-700">
                      <TableCell>
                        <CopyId id={bin.id} />
                      </TableCell>
                      <TableCell>{bin.nombre}</TableCell>
                      <TableCell>{bin.x}</TableCell>
                      <TableCell>{bin.y}</TableCell>
                      <TableCell>{bin.z}</TableCell>
                      <TableCell>
                        <span
                          className={
                            bin.is_active
                              ? "rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-900"
                              : "rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-700"
                          }
                        >
                          {bin.is_active ? "Yes" : "No"}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        <BinActionsMenu bin={bin} />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </div>
        </TableCell>
      </TableRow>
    )
  }

  if (warehouses.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">No hay depósitos todavía</h3>
        <p className="text-muted-foreground">
          Agrega un depósito para comenzar a administrarlos.
        </p>
      </div>
    )
  }

  return (
    <DataTable
      columns={warehouseColumns}
      data={warehouses}
      renderRowDetail={renderRowDetail}
    />
  )
}

function Depositos() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Depósitos y Ubicaciones</h1>
        <p className="text-muted-foreground">
          Gestiona tus depósitos y explora sus ubicaciones.
        </p>
      </div>
      <div className="space-y-4">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold">Depósitos</h2>
            <p className="text-muted-foreground">
              Expande un depósito para ver sus ubicaciones directamente en la fila.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <AddBin />
            <AddWarehouse />
          </div>
        </div>
        <Suspense
          fallback={
            <div className="rounded-xl border p-8 text-center text-muted-foreground">
              Cargando depósitos...
            </div>
          }
        >
          <WarehousesTableContent />
        </Suspense>
      </div>
    </div>
  )
}

export const Route = createFileRoute("/_layout/general/depositos")({
  component: Depositos,
})
