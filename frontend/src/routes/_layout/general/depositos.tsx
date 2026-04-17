import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { BinsService } from "@/lib/bins"
import { WarehousesService } from "@/lib/warehouses"
import { DataTable } from "@/components/Common/DataTable"
import AddBin from "@/components/General/AddBin"
import AddWarehouse from "@/components/General/AddWarehouse"
import { columnsBins } from "@/components/General/columnsBins"
import { columnsWarehouses } from "@/components/General/columnsWarehouses"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

function getWarehousesQueryOptions() {
  return {
    queryFn: () => WarehousesService.readWarehouses({ skip: 0, limit: 100 }),
    queryKey: ["warehouses"],
  }
}

function getBinsQueryOptions() {
  return {
    queryFn: () => BinsService.readBins({ skip: 0, limit: 100 }),
    queryKey: ["bins"],
  }
}

function WarehousesTableContent() {
  const { data: warehouses } = useSuspenseQuery(getWarehousesQueryOptions())

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

  return <DataTable columns={columnsWarehouses} data={warehouses} />
}

function BinsTableContent() {
  const { data: bins } = useSuspenseQuery(getBinsQueryOptions())

  if (bins.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">No hay ubicaciones todavía</h3>
        <p className="text-muted-foreground">
          Agrega una ubicación para comenzar a administrarlas.
        </p>
      </div>
    )
  }

  return <DataTable columns={columnsBins} data={bins} />
}

function Depositos() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Depósitos y Ubicaciones</h1>
        <p className="text-muted-foreground">
          Crea, edita y elimina depósitos y sus ubicaciones.
        </p>
      </div>
      <Tabs defaultValue="warehouses" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="warehouses">Depósitos</TabsTrigger>
          <TabsTrigger value="bins">Ubicaciones</TabsTrigger>
        </TabsList>
        <TabsContent value="warehouses" className="space-y-4">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold">Depósitos</h2>
              <p className="text-muted-foreground">
                Gestiona los depósitos de tu inventario.
              </p>
            </div>
            <AddWarehouse />
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
        </TabsContent>
        <TabsContent value="bins" className="space-y-4">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold">Ubicaciones</h2>
              <p className="text-muted-foreground">
                Gestiona las ubicaciones dentro de los depósitos.
              </p>
            </div>
            <AddBin />
          </div>
          <Suspense
            fallback={
              <div className="rounded-xl border p-8 text-center text-muted-foreground">
                Cargando ubicaciones...
              </div>
            }
          >
            <BinsTableContent />
          </Suspense>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export const Route = createFileRoute("/_layout/general/depositos")({
  component: Depositos,
})