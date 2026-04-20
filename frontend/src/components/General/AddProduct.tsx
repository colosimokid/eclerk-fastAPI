import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Plus } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { CategoriesService, SectionsService, SubSectionsService } from "@/client"
import { type ProductCreate, ProductsService } from "@/lib/products"
import { BrandsService } from "@/lib/brands"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
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
  category_id: z.string().min(1, { message: "La categoría es requerida" }),
  section_id: z.string().min(1, { message: "La sección es requerida" }),
  sub_section_id: z.string().optional(),
  codigo: z.string().min(1, { message: "El código es requerido" }),
  referencia: z.string().optional(),
  descripcion: z.string().min(1, { message: "La descripción es requerida" }),
  descripcion_adicional: z.string().optional(),
  cod_barras_1: z.string().optional(),
  cod_barras_2: z.string().optional(),
  cod_barras_3: z.string().optional(),
  brand_id: z.string().optional(),
  ultimo_coste: z.number().min(0).optional(),
  peso: z.number().min(0).optional(),
  impuesto_compra: z.number().min(0).max(100),
  impuesto_venta: z.number().min(0).max(100),
  is_active: z.boolean(),
})

type FormData = z.infer<typeof formSchema>

const AddProduct = () => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const { data: categories = [] } = useQuery({
    queryKey: ["categories"],
    queryFn: () => CategoriesService.readCategories(),
  })

  const { data: brands = [] } = useQuery({
    queryKey: ["brands"],
    queryFn: () => BrandsService.readBrands(),
  })

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      category_id: "",
      section_id: "",
      sub_section_id: "",
      codigo: "",
      referencia: "",
      descripcion: "",
      descripcion_adicional: "",
      cod_barras_1: "",
      cod_barras_2: "",
      cod_barras_3: "",
      brand_id: "",
      ultimo_coste: undefined,
      peso: undefined,
      impuesto_compra: 0,
      impuesto_venta: 0,
      is_active: true,
    },
  })

  const selectedCategoryId = form.watch("category_id")
  const selectedSectionId = form.watch("section_id")

  const { data: sections = [] } = useQuery({
    queryKey: ["sections"],
    queryFn: () => SectionsService.readSections({ skip: 0, limit: 100 }),
  })

  const { data: subSections = [] } = useQuery({
    queryKey: ["sub_sections"],
    queryFn: () => SubSectionsService.readSubSections({ skip: 0, limit: 100 }),
  })

  const filteredSections = sections.filter(
    (section) => section.category_id === selectedCategoryId,
  )

  const filteredSubSections = subSections.filter(
    (subSection) => subSection.section_id === selectedSectionId,
  )

  const mutation = useMutation({
    mutationFn: (data: ProductCreate) => ProductsService.createProduct(data),
    onSuccess: () => {
      showSuccessToast("Producto creado correctamente")
      form.reset()
      setIsOpen(false)
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
    },
  })

  const onSubmit = (data: FormData) => {
    const productData: ProductCreate = {
      ...data,
      sub_section_id: data.sub_section_id || undefined,
      brand_id: data.brand_id || undefined,
      ultimo_coste: data.ultimo_coste || undefined,
      peso: data.peso || undefined,
    }
    mutation.mutate(productData)
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button className="my-4">
          <Plus className="mr-2" />
          Agregar Producto
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Agregar Producto</DialogTitle>
          <DialogDescription>
            Completa los datos para crear un nuevo producto.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-3 gap-4">
                <FormField
                  control={form.control}
                  name="category_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Categoría <span className="text-destructive">*</span>
                      </FormLabel>
                      <Select onValueChange={field.onChange} value={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Seleccionar categoría" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {categories.map((category) => (
                            <SelectItem key={category.id} value={category.id}>
                              {category.nombre}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="section_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Sección <span className="text-destructive">*</span>
                      </FormLabel>
                      <Select
                        onValueChange={(value) => {
                          field.onChange(value)
                          form.setValue("sub_section_id", "")
                        }}
                        value={field.value}
                        disabled={!selectedCategoryId}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Seleccionar sección" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {filteredSections.map((section) => (
                            <SelectItem key={section.id} value={section.id}>
                              {section.nombre}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="sub_section_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Sub Sección</FormLabel>
                      <Select onValueChange={field.onChange} value={field.value} disabled={!selectedSectionId}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Seleccionar sub sección" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {filteredSubSections.map((subSection) => (
                            <SelectItem key={subSection.id} value={subSection.id}>
                              {subSection.nombre}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

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
                        <Input placeholder="Código del producto" type="text" {...field} />
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
                      <Input placeholder="Descripción del producto" type="text" {...field} />
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

              <FormField
                control={form.control}
                name="brand_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Marca</FormLabel>
                    <Select onValueChange={field.onChange} value={field.value}>
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Seleccionar marca" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {brands.map((brand) => (
                          <SelectItem key={brand.id} value={brand.id}>
                            {brand.nombre}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

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

export default AddProduct