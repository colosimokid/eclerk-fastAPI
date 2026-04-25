import axios from "axios"
import { OpenAPI } from "@/client"

const apiBase = OpenAPI.BASE.replace(/\/$/, "")

const getAuthHeaders = () => {
  const token = localStorage.getItem("access_token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export type StorageDetailPublic = {
  id: string
  product_id: string
  bin_id: string
  qty_on_hand: number
  qty_order_on_hand: number
  date_last_inventory?: string | null
  is_active: boolean
  created_at?: string | null
  updated_at?: string | null
}

export type StorageDetailSearchParams = {
  warehouse_id?: string | null
  bin_id?: string | null
  product_query?: string | null
  skip?: number
}

export const StorageDetailsService = {
  searchStorageDetails: async (params: StorageDetailSearchParams = {}) => {
    const query: Record<string, string | number> = {}
    if (params.warehouse_id) query.warehouse_id = params.warehouse_id
    if (params.bin_id) query.bin_id = params.bin_id
    if (params.product_query) query.product_query = params.product_query
    if (params.skip !== undefined) query.skip = params.skip

    const response = await axios.get<StorageDetailPublic[]>(
      `${apiBase}/api/v1/storage_details/search`,
      { headers: getAuthHeaders(), params: query },
    )
    return response.data
  },
}
