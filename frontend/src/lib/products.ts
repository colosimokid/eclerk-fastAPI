import axios from "axios"
import { OpenAPI } from "@/client"

const apiBase = OpenAPI.BASE.replace(/\/$/, "")

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export type ProductPublic = {
  id: string
  category_id: string
  section_id: string
  sub_section_id?: string | null
  codigo: string
  referencia?: string | null
  descripcion: string
  descripcion_adicional?: string | null
  cod_barras_1?: string | null
  cod_barras_2?: string | null
  cod_barras_3?: string | null
  brand_id?: string | null
  ultimo_coste?: number | null
  peso?: number | null
  impuesto_compra: number
  impuesto_venta: number
  is_active: boolean
  created_at?: string | null
  updated_at?: string | null
}

export type ProductCreate = {
  category_id: string
  section_id: string
  sub_section_id?: string | null
  codigo: string
  referencia?: string | null
  descripcion: string
  descripcion_adicional?: string | null
  cod_barras_1?: string | null
  cod_barras_2?: string | null
  cod_barras_3?: string | null
  brand_id?: string | null
  ultimo_coste?: number | null
  peso?: number | null
  impuesto_compra?: number
  impuesto_venta?: number
  is_active?: boolean
}

export type ProductUpdate = {
  category_id?: string
  section_id?: string
  sub_section_id?: string | null
  codigo?: string
  referencia?: string | null
  descripcion?: string
  descripcion_adicional?: string | null
  cod_barras_1?: string | null
  cod_barras_2?: string | null
  cod_barras_3?: string | null
  brand_id?: string | null
  ultimo_coste?: number | null
  peso?: number | null
  impuesto_compra?: number
  impuesto_venta?: number
  is_active?: boolean
}

export const ProductsService = {
  readProducts: async ({ skip = 0 } = {}) => {
    const response = await axios.get<ProductPublic[]>(`${apiBase}/api/v1/products`, {
      headers: getAuthHeaders(),
      params: { skip },
    })
    return response.data
  },

  createProduct: async (data: ProductCreate) => {
    const response = await axios.post<ProductPublic>(`${apiBase}/api/v1/products`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  updateProduct: async (id: string, data: ProductUpdate) => {
    const response = await axios.patch<ProductPublic>(`${apiBase}/api/v1/products/${id}`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  deleteProduct: async (id: string) => {
    const response = await axios.delete<{ message: string }>(`${apiBase}/api/v1/products/${id}`, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  getProductById: async (id: string) => {
    const response = await axios.get<ProductPublic>(`${apiBase}/api/v1/products/${id}`, {
      headers: getAuthHeaders(),
    })
    return response.data
  },
}