import { useState } from "react"

import type { CategoryPublic, SectionPublic, SubSectionPublic } from "@/client"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { TableCell, TableRow } from "@/components/ui/table"
import { ChevronDown, ChevronRight } from "lucide-react"
import AddSection from "./AddSection"
import SectionRow from "./SectionRow"

interface CategoryRowProps {
  category: CategoryPublic
  sections: SectionPublic[]
  subSections: SubSectionPublic[]
}

export default function CategoryRow({ category, sections, subSections }: CategoryRowProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const toggleExpanded = () => setIsExpanded(!isExpanded)

  return (
    <>
      <TableRow>
        <TableCell>
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleExpanded}
            className="h-6 w-6 p-0"
          >
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </Button>
        </TableCell>
        <TableCell className="font-medium">{category.nombre}</TableCell>
        <TableCell>
          <Badge variant="secondary">Categoría</Badge>
        </TableCell>
        <TableCell>
          <Badge variant={category.is_active ? "default" : "secondary"}>
            {category.is_active ? "Activo" : "Inactivo"}
          </Badge>
        </TableCell>
        <TableCell>
          {category.created_at ? new Date(category.created_at).toLocaleDateString() : "-"}
        </TableCell>
        <TableCell>
          <div className="flex items-center gap-2">
            <AddSection categoryId={category.id} />
            {/* Aquí irían los botones de editar y eliminar */}
          </div>
        </TableCell>
      </TableRow>
      {isExpanded && sections.map((section) => (
        <SectionRow
          key={section.id}
          section={section}
          subSections={subSections.filter(s => s.section_id === section.id)}
        />
      ))}
    </>
  )
}