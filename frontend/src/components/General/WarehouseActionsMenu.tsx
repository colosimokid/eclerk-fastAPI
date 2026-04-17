import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { WarehousePublic } from "@/lib/warehouses"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteWarehouse from "./DeleteWarehouse"
import EditWarehouse from "./EditWarehouse"

interface WarehouseActionsMenuProps {
  warehouse: WarehousePublic
}

export const WarehouseActionsMenu = ({ warehouse }: WarehouseActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditWarehouse warehouse={warehouse} onSuccess={() => setOpen(false)} />
        <DeleteWarehouse id={warehouse.id} onSuccess={() => setOpen(false)} />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}