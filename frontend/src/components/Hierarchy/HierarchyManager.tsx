import { useSuspenseQuery } from "@tanstack/react-query"
import { Plus } from "lucide-react"

import { CategoriesService, SectionsService, SubSectionsService } from "@/client"
import {
  Table,
  TableBody,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import AddCategory from "./AddCategory"
import CategoryRow from "./CategoryRow"

function getCategoriesQueryOptions() {
  return {
    queryFn: () => CategoriesService.readCategories({ skip: 0, limit: 100 }),
    queryKey: ["categories"],
  }
}

function getSectionsQueryOptions() {
  return {
    queryFn: () => SectionsService.readSections({ skip: 0, limit: 100 }),
    queryKey: ["sections"],
  }
}

function getSubSectionsQueryOptions() {
  return {
    queryFn: () => SubSectionsService.readSubSections({ skip: 0, limit: 100 }),
    queryKey: ["sub-sections"],
  }
}

function HierarchyTableContent() {
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions())
  const { data: sections } = useSuspenseQuery(getSectionsQueryOptions())
  const { data: subSections } = useSuspenseQuery(getSubSectionsQueryOptions())

  if (categories.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Plus className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">No hay categorías aún</h3>
        <p className="text-muted-foreground">Crea tu primera categoría para comenzar</p>
      </div>
    )
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-8"></TableHead>
          <TableHead>Nombre</TableHead>
          <TableHead>Tipo</TableHead>
          <TableHead>Estado</TableHead>
          <TableHead>Creado</TableHead>
          <TableHead className="w-32">Acciones</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {categories.map((category) => (
          <CategoryRow
            key={category.id}
            category={category}
            sections={sections.filter(s => s.category_id === category.id)}
            subSections={subSections}
          />
        ))}
      </TableBody>
    </Table>
  )
}

function HierarchyTable() {
  return (
    <div className="space-y-4">
      <HierarchyTableContent />
    </div>
  )
}

export default function HierarchyManager() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Jerarquía</h1>
          <p className="text-muted-foreground">
            Gestiona categorías, secciones y sub-secciones
          </p>
        </div>
        <AddCategory />
      </div>
      <HierarchyTable />
    </div>
  )
}