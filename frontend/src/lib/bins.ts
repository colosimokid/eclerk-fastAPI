import axios from "axios"
import { OpenAPI } from "@/client"

const apiBase = OpenAPI.BASE.replace(/\/$/, "")

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export type BinPublic = {
  id: string
  nombre: string
  x: string
  y: string
  z: string
  warehouse_id: string
  is_active: boolean
  created_at?: string | null
  updated_at?: string | null
}

export type BinCreate = {
  nombre: string
  x: string
  y: string
  z: string
  warehouse_id: string
  is_active?: boolean
}

export type BinUpdate = {
  nombre?: string
  x?: string
  y?: string
  z?: string
  warehouse_id?: string
  is_active?: boolean
}

export const BinsService = {
  readBins: async ({ skip = 0 } = {}) => {
    const response = await axios.get<BinPublic[]>(`${apiBase}/api/v1/bins`, {
      headers: getAuthHeaders(),
      params: { skip },
    })
    return response.data
  },

  createBin: async (data: BinCreate) => {
    const response = await axios.post<BinPublic>(`${apiBase}/api/v1/bins`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  updateBin: async (id: string, data: BinUpdate) => {
    const response = await axios.patch<BinPublic>(`${apiBase}/api/v1/bins/${id}`, data, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  deleteBin: async (id: string) => {
    const response = await axios.delete(`${apiBase}/api/v1/bins/${id}`, {
      headers: getAuthHeaders(),
    })
    return response.data
  },

  readBinsByWarehouse: async (warehouseId: string, { skip = 0 } = {}) => {
    const response = await axios.get<BinPublic[]>(`${apiBase}/api/v1/bins/warehouse/${warehouseId}`, {
      headers: getAuthHeaders(),
      params: { skip },
    })
    return response.data
  },
}