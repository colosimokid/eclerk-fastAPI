import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { Pencil } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import type { ProductPublic } from "@/lib/products"
import { ProductsService } from "@/lib/products"
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
import { Textarea } from "@/components/ui/textarea"
import { LoadingButton } from "@/components/ui/loading-button"
import { Checkbox } from "@/components/ui/checkbox"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const formSchema = z.object({
  codigo: z.string().min(1, { message: "El código es requerido" }),
  referencia: z.string().optional(),
  descripcion: z.string().min(1, { message: "La descripción es requerida" }),
  descripcion_adicional: z.string().optional(),
  cod_barras_1: z.string().optional(),
  cod_barras_2: z.string().optional(),
  cod_barras_3: z.string().optional(),
  ultimo_coste: z.number().min(0).optional(),
  peso: z.number().min(0).optional(),
  impuesto_compra: z.number().min(0).max(100),
  impuesto_venta: z.number().min(0).max(100),
  is_active: z.boolean(),
})

type FormData = z.infer<typeof formSchema>

interface EditProductProps {
  product: ProductPublic
  onSuccess: () => void
}

const EditProduct = ({ product, onSuccess }: EditProductProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      codigo: product.codigo,
      referencia: product.referencia || "",
      descripcion: product.descripcion,
      descripcion_adicional: product.descripcion_adicional || "",
      cod_barras_1: product.cod_barras_1 || "",
      cod_barras_2: product.cod_barras_2 || "",
      cod_barras_3: product.cod_barras_3 || "",
      ultimo_coste: product.ultimo_coste || undefined,
      peso: product.peso || undefined,
      impuesto_compra: product.impuesto_compra,
      impuesto_venta: product.impuesto_venta,
      is_active: product.is_active,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FormData) => ProductsService.updateProduct(product.id, data),
    onSuccess: () => {
      showSuccessToast("Producto actualizado correctamente")
      setIsOpen(false)
      onSuccess()
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
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
        Editar Producto
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <DialogHeader>
              <DialogTitle>Editar Producto</DialogTitle>
              <DialogDescription>
                Actualiza los datos del producto.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="codigo"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Código <span className="text-destructive">*</span>
                      </FormLabel>
                      <FormControl>
                        <Input placeholder="Código" type="text" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="referencia"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Referencia</FormLabel>
                      <FormControl>
                        <Input placeholder="Referencia" type="text" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormField
                control={form.control}
                name="descripcion"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      Descripción <span className="text-destructive">*</span>
                    </FormLabel>
                    <FormControl>
                      <Input placeholder="Descripción" type="text" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="descripcion_adicional"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Descripción Adicional</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Descripción adicional" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="grid grid-cols-3 gap-4">
                <FormField
                  control={form.control}
                  name="cod_barras_1"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Código de Barras 1</FormLabel>
                      <FormControl>
                        <Input placeholder="Código 1" type="text" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="cod_barras_2"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Código de Barras 2</FormLabel>
                      <FormControl>
                        <Input placeholder="Código 2" type="text" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="cod_barras_3"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Código de Barras 3</FormLabel>
                      <FormControl>
                        <Input placeholder="Código 3" type="text" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="ultimo_coste"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Último Coste</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0.00"
                          type="number"
                          step="0.01"
                          {...field}
                          onChange={(e) => field.onChange(e.target.value ? parseFloat(e.target.value) : undefined)}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="peso"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Peso (kg)</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0.00"
                          type="number"
                          step="0.01"
                          {...field}
                          onChange={(e) => field.onChange(e.target.value ? parseFloat(e.target.value) : undefined)}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="impuesto_compra"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Impuesto Compra (%)</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0"
                          type="number"
                          step="0.01"
                          min="0"
                          max="100"
                          {...field}
                          onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="impuesto_venta"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Impuesto Venta (%)</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0"
                          type="number"
                          step="0.01"
                          min="0"
                          max="100"
                          {...field}
                          onChange={(e) => field.onChange(parseFloat(e.target.value) || 0)}
                        />
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
                  <FormItem className="flex items-center gap-3 space-y-0">
                    <FormControl>
                      <Checkbox
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                    <FormLabel className="font-normal">Activo</FormLabel>
                  </FormItem>
                )}
              />
            </div>

            <DialogFooter>
              <DialogClose asChild>
                <Button variant="outline" disabled={mutation.isPending}>
                  Cancelar
                </Button>
              </DialogClose>
              <LoadingButton type="submit" loading={mutation.isPending}>
                Guardar
              </LoadingButton>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default EditProduct