import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient, useSuspenseQuery } from "@tanstack/react-query"
import { Pencil } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import type { BinPublic } from "@/lib/bins"
import { BinsService } from "@/lib/bins"
import { WarehousesService } from "@/lib/warehouses"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { DropdownMenuItem } from "@/components/ui/dropdown-menu"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { LoadingButton } from "@/components/ui/loading-button"
import { Checkbox } from "@/components/ui/checkbox"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const formSchema = z.object({
  nombre: z.string().min(1, { message: "El nombre es requerido" }),
  x: z.string().max(15, { message: "Máximo 15 caracteres" }),
  y: z.string().max(15, { message: "Máximo 15 caracteres" }),
  z: z.string().max(15, { message: "Máximo 15 caracteres" }),
  warehouse_id: z.string().min(1, { message: "Selecciona un depósito" }),
  is_active: z.boolean(),
})

type FormData = z.infer<typeof formSchema>

interface EditBinProps {
  bin: BinPublic
  onSuccess: () => void
}

const EditBin = ({ bin, onSuccess }: EditBinProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const { data: warehouses } = useSuspenseQuery({
    queryFn: () => WarehousesService.readWarehouses(),
    queryKey: ["warehouses"],
  })

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      nombre: bin.nombre,
      x: bin.x,
      y: bin.y,
      z: bin.z,
      warehouse_id: bin.warehouse_id,
      is_active: bin.is_active,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FormData) => BinsService.updateBin(bin.id, data),
    onSuccess: () => {
      showSuccessToast("Ubicación actualizada correctamente")
      setIsOpen(false)
      onSuccess()
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["bins"] })
    },
  })

  const onSubmit = (data: FormData) => {
    mutation.mutate(data)
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuItem
        onSelect={(e) => e.preventDefault()}
        onClick={() => setIsOpen(true)}
      >
        <Pencil />
        Editar Ubicación
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-md">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <DialogHeader>
              <DialogTitle>Editar Ubicación</DialogTitle>
              <DialogDescription>
                Actualiza los datos de la ubicación.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <FormField
                control={form.control}
                name="nombre"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Nombre <span className="text-destructive">*</span>
                    </FormLabel>
                    <FormControl>
                      <Input placeholder="Nombre de la ubicación" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="warehouse_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Depósito <span className="text-destructive">*</span>
                    </FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Selecciona un depósito" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {warehouses.map((warehouse) => (
                          <SelectItem key={warehouse.id} value={warehouse.id}>
                            {warehouse.nombre}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="grid grid-cols-3 gap-4">
                <FormField
                  control={form.control}
                  name="x"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>X</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="y"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Y</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="z"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Z</FormLabel>
                      <FormControl>
                        <Input {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <FormField
                control={form.control}
                name="is_active"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                    <FormControl>
                      <Checkbox
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                    <div className="space-y-1 leading-none">
                      <FormLabel>Activo</FormLabel>
                    </div>
                  </FormItem>
                )}
              />
            </div>
            <DialogFooter>
              <DialogClose asChild>
                <Button type="button" variant="outline">
                  Cancelar
                </Button>
              </DialogClose>
              <LoadingButton
                type="submit"
                loading={mutation.isPending}
                disabled={!form.formState.isValid}
              >
                Actualizar
              </LoadingButton>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default EditBin