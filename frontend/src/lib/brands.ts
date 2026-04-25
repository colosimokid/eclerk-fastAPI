import axios from "axios"
import { OpenAPI } from "@/client"

const apiBase = OpenAPI.BASE.replace(/\/$/, "")

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export type BrandPublic = {
  id: string
  nombre: string
  is_active: boolean
  created_at?: string | null
  updated_at?: string | null
}

export type BrandCreate = {
  nombre: string
  is_active?: boolean
}

export type BrandUpdate = {
  nombre?: string
  is_active?: boolean
}

export const BrandsService = {
  readBrands: async ({ skip = 0 } = {}) => {
    const response = await axios.get<BrandPublic[]>(`${apiBase}/api/v1/brands`, {
      headers: getAuthHeaders(),
      params: { skip },
    })
    return response.data
  },

  createBrand: async (data: BrandCreate) => {
    const response = await axios.post<BrandPublic>(`${apiBase}/api/v1/brands`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  updateBrand: async (id: string, data: BrandUpdate) => {
    const response = await axios.patch<BrandPublic>(`${apiBase}/api/v1/brands/${id}`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  deleteBrand: async (id: string) => {
    const response = await axios.delete<{ message: string }>(`${apiBase}/api/v1/brands/${id}`, {
      headers: getAuthHeaders(),
    })
    return response.data
  },
}
