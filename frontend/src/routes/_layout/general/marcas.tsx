import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { BrandsService } from "@/lib/brands"
import { DataTable } from "@/components/Common/DataTable"
import AddBrand from "@/components/General/AddBrand"
import { columns } from "@/components/General/columns"

function getBrandsQueryOptions() {
  return {
    queryFn: () => BrandsService.readBrands({ skip: 0, limit: 100 }),
    queryKey: ["brands"],
  }
}

function BrandsTableContent() {
  const { data: brands } = useSuspenseQuery(getBrandsQueryOptions())

  if (brands.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">No hay marcas todavía</h3>
        <p className="text-muted-foreground">
          Agrega una marca para comenzar a administrarlas.
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={brands} />
}

function Brands() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Marcas</h1>
          <p className="text-muted-foreground">Crea, edita y elimina marcas.</p>
        </div>
        <AddBrand />
      </div>
      <Suspense
        fallback={
          <div className="rounded-xl border p-8 text-center text-muted-foreground">
            Cargando marcas...
          </div>
        }
      >
        <BrandsTableContent />
      </Suspense>
    </div>
  )
}

export const Route = createFileRoute("/_layout/general/marcas")({
  component: Brands,
  head: () => ({
    meta: [
      {
        title: "Marcas - FastAPI Cloud",
      },
    ],
  }),
})
