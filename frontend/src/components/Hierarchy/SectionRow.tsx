import { useState } from "react"

import type { SectionPublic, SubSectionPublic } from "@/client"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { TableCell, TableRow } from "@/components/ui/table"
import { ChevronDown, ChevronRight } from "lucide-react"
import AddSubSection from "./AddSubSection"
import SubSectionRow from "./SubSectionRow"

interface SectionRowProps {
  section: SectionPublic
  subSections: SubSectionPublic[]
}

export default function SectionRow({ section, subSections }: SectionRowProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const toggleExpanded = () => setIsExpanded(!isExpanded)

  return (
    <>
      <TableRow className="bg-muted/50">
        <TableCell className="pl-8">
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
        <TableCell className="font-medium pl-4">{section.nombre}</TableCell>
        <TableCell>
          <Badge variant="outline">Sección</Badge>
        </TableCell>
        <TableCell>
          <Badge variant={section.is_active ? "default" : "secondary"}>
            {section.is_active ? "Activo" : "Inactivo"}
          </Badge>
        </TableCell>
        <TableCell>
          {section.created_at ? new Date(section.created_at).toLocaleDateString() : "-"}
        </TableCell>
        <TableCell>
          <div className="flex items-center gap-2">
            <AddSubSection sectionId={section.id} />
            {/* Aquí irían los botones de editar y eliminar */}
          </div>
        </TableCell>
      </TableRow>
      {isExpanded && subSections.map((subSection) => (
        <SubSectionRow key={subSection.id} subSection={subSection} />
      ))}
    </>
  )
}