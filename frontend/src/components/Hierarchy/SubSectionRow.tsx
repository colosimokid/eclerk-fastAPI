import type { SubSectionPublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { TableCell, TableRow } from "@/components/ui/table"

interface SubSectionRowProps {
  subSection: SubSectionPublic
}

export default function SubSectionRow({ subSection }: SubSectionRowProps) {
  return (
    <TableRow className="bg-muted/25">
      <TableCell className="pl-16"></TableCell>
      <TableCell className="font-medium pl-8">{subSection.nombre}</TableCell>
      <TableCell>
        <Badge variant="outline" className="text-xs">Sub-sección</Badge>
      </TableCell>
      <TableCell>
        <Badge variant={subSection.is_active ? "default" : "secondary"}>
          {subSection.is_active ? "Activo" : "Inactivo"}
        </Badge>
      </TableCell>
      <TableCell>
        {subSection.created_at ? new Date(subSection.created_at).toLocaleDateString() : "-"}
      </TableCell>
      <TableCell>
        {/* Aquí irían los botones de editar y eliminar */}
      </TableCell>
    </TableRow>
  )
}