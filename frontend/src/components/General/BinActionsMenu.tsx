import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { BinPublic } from "@/lib/bins"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeleteBin from "./DeleteBin"
import EditBin from "./EditBin"

interface BinActionsMenuProps {
  bin: BinPublic
}

export const BinActionsMenu = ({ bin }: BinActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditBin bin={bin} onSuccess={() => setOpen(false)} />
        <DeleteBin id={bin.id} onSuccess={() => setOpen(false)} />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}