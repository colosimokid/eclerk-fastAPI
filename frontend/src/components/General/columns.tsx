import type { ColumnDef } from "@tanstack/react-table"
import { Check, Copy } from "lucide-react"

import type { BrandPublic } from "@/lib/brands"
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard"
import { cn } from "@/lib/utils"
import { BrandActionsMenu } from "./BrandActionsMenu"

function CopyId({ id }: { id: string }) {
  const [copiedText, copy] = useCopyToClipboard()
  const isCopied = copiedText === id
  const shortId = id.slice(0, 8) + "..."

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center gap-1.5 group">
            <span className="font-mono text-xs text-muted-foreground">{shortId}</span>
            <Button
              variant="ghost"
              size="icon"
              className="size-6 opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={() => copy(id)}
            >
              {isCopied ? (
                <Check className="size-3 text-green-500" />
              ) : (
                <Copy className="size-3" />
              )}
              <span className="sr-only">Copy ID</span>
            </Button>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>{id}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

export const columns: ColumnDef<BrandPublic>[] = [
  {
    accessorKey: "id",
    header: "ID",
    cell: ({ row }) => <CopyId id={row.original.id} />,
  },
  {
    accessorKey: "nombre",
    header: "Nombre",
    cell: ({ row }) => <span className="font-medium">{row.original.nombre}</span>,
  },
  {
    accessorKey: "is_active",
    header: "Activo",
    cell: ({ row }) => (
      <span
        className={cn(
          "rounded-full px-2 py-1 text-xs font-semibold",
          row.original.is_active
            ? "bg-emerald-100 text-emerald-900"
            : "bg-slate-100 text-slate-700",
        )}
      >
        {row.original.is_active ? "Yes" : "No"}
      </span>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <BrandActionsMenu brand={row.original} />
      </div>
    ),
  },
]
