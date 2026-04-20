import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { ProductsService } from "@/lib/products"
import { DataTable } from "@/components/Common/DataTable"
import AddProduct from "@/components/General/AddProduct"
import { columnsProducts } from "@/components/General/columnsProducts"

function getProductsQueryOptions() {
  return {
    queryFn: () => ProductsService.readProducts({ skip: 0, limit: 100 }),
    queryKey: ["products"],
  }
}

function ProductsTableContent() {
  const { data: products } = useSuspenseQuery(getProductsQueryOptions())

  if (products.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">No hay productos todavía</h3>
        <p className="text-muted-foreground">
          Agrega un producto para comenzar a administrarlos.
        </p>
      </div>
    )
  }

  return <DataTable columns={columnsProducts} data={products} />
}

function Products() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Productos</h1>
          <p className="text-muted-foreground">Crea, edita y elimina productos.</p>
        </div>
        <AddProduct />
      </div>
      <Suspense
        fallback={
          <div className="rounded-xl border p-8 text-center text-muted-foreground">
            Cargando productos...
          </div>
        }
      >
        <ProductsTableContent />
      </Suspense>
    </div>
  )
}

export const Route = createFileRoute("/_layout/general/productos")({
  component: Products,
  head: () => ({
    meta: [
      {
        title: "Productos - FastAPI Cloud",
      },
    ],
  }),
})