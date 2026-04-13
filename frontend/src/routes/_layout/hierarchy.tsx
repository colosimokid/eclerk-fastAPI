import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense } from "react"

import { CategoriesService } from "@/client"
import HierarchyManager from "@/components/Hierarchy/HierarchyManager"

function getCategoriesQueryOptions() {
  return {
    queryFn: () => CategoriesService.readCategories({ skip: 0, limit: 100 }),
    queryKey: ["categories"],
  }
}

function HierarchyContent() {
  // Esta query asegura que los datos estén disponibles antes de renderizar
  useSuspenseQuery(getCategoriesQueryOptions())
  return <HierarchyManager />
}

function Hierarchy() {
  return (
    <Suspense fallback={<div>Cargando jerarquía...</div>}>
      <HierarchyContent />
    </Suspense>
  )
}

export const Route = createFileRoute("/_layout/hierarchy")({
  component: Hierarchy,
  head: () => ({
    meta: [
      {
        title: "Jerarquía - FastAPI Cloud",
      },
    ],
  }),
})