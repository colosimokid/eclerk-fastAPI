import axios from "axios"
import { OpenAPI } from "@/client"

const apiBase = OpenAPI.BASE.replace(/\/$/, "")

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export type WarehousePublic = {
  id: string
  nombre: string
  estado: string
  direccion: string
  is_active: boolean
  created_at?: string | null
  updated_at?: string | null
}

export type WarehouseCreate = {
  nombre: string
  estado: string
  direccion: string
  is_active?: boolean
}

export type WarehouseUpdate = {
  nombre?: string
  estado?: string
  direccion?: string
  is_active?: boolean
}

export const WarehousesService = {
  readWarehouses: async ({ skip = 0 } = {}) => {
    const response = await axios.get<WarehousePublic[]>(`${apiBase}/api/v1/warehouses`, {
      headers: getAuthHeaders(),
      params: { skip },
    })
    return response.data
  },

  createWarehouse: async (data: WarehouseCreate) => {
    const response = await axios.post<WarehousePublic>(`${apiBase}/api/v1/warehouses`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  updateWarehouse: async (id: string, data: WarehouseUpdate) => {
    const response = await axios.patch<WarehousePublic>(`${apiBase}/api/v1/warehouses/${id}`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  deleteWarehouse: async (id: string) => {
    const response = await axios.delete(`${apiBase}/api/v1/warehouses/${id}`, {
      headers: getAuthHeaders(),
    })
    return response.data
  },
}