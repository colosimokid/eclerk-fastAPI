import type { ColumnDef } from "@tanstack/react-table"
import { Check, Copy } from "lucide-react"

import type { ProductPublic } from "@/lib/products"
import { Button } from "@/components/ui/button"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"
import { useCopyToClipboard } from "@/hooks/useCopyToClipboard"
import { cn } from "@/lib/utils"
import { ProductActionsMenu } from "./ProductActionsMenu"

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

export const columnsProducts: ColumnDef<ProductPublic>[] = [
  {
    accessorKey: "id",
    header: "ID",
    cell: ({ row }) => <CopyId id={row.original.id} />,
  },
  {
    accessorKey: "codigo",
    header: "Código",
    cell: ({ row }) => <span className="font-medium">{row.original.codigo}</span>,
  },
  {
    accessorKey: "descripcion",
    header: "Descripción",
    cell: ({ row }) => <span className="font-medium">{row.original.descripcion}</span>,
  },
  {
    accessorKey: "referencia",
    header: "Referencia",
    cell: ({ row }) => <span>{row.original.referencia || "-"}</span>,
  },
  {
    accessorKey: "ultimo_coste",
    header: "Último Coste",
    cell: ({ row }) => (
      <span>
        {row.original.ultimo_coste !== null && row.original.ultimo_coste !== undefined
          ? `$${row.original.ultimo_coste.toFixed(2)}`
          : "-"}
      </span>
    ),
  },
  {
    accessorKey: "peso",
    header: "Peso",
    cell: ({ row }) => (
      <span>
        {row.original.peso !== null && row.original.peso !== undefined
          ? `${row.original.peso.toFixed(2)} kg`
          : "-"}
      </span>
    ),
  },
  {
    accessorKey: "is_active",
    header: "Activo",
    cell: ({ row }) => (
      <span
        className={cn(
          "rounded-full px-2 py-1 text-xs font-semibold",
          row.original.is_active
            ? "bg-emerald-100 text-emerald-900 dark:bg-emerald-900 dark:text-emerald-100"
            : "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
        )}
      >
        {row.original.is_active ? "Sí" : "No"}
      </span>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Acciones</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <ProductActionsMenu product={row.original} />
      </div>
    ),
  },
]