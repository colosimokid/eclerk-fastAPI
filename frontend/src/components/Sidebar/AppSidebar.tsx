import { Home, Layers, ShoppingCart, Truck, Users } from "lucide-react"

import { SidebarAppearance } from "@/components/Common/Appearance"
import { Logo } from "@/components/Common/Logo"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import useAuth from "@/hooks/useAuth"
import { type Item, Main } from "./Main"
import { User } from "./User"

const baseItems: Item[] = [{ icon: Home, title: "Dashboard", path: "/" }]

const sidebarItems: Item[] = [
  {
    icon: Layers,
    title: "General",
    path: "/general",
    subItems: [
      { title: "Tasa conversión", path: "/general/tasa-conversion" },
      { title: "Marcas", path: "/general/marcas" },
      { title: "Productos", path: "/general/productos" },
      { title: "Depositos", path: "/general/depositos" },
      { title: "Categorias", path: "/general/categorias" },
    ],
  },
  {
    icon: ShoppingCart,
    title: "Compras",
    path: "/compras",
    subItems: [
      { title: "Orden de compra", path: "/compras/orden-de-compra" },
      { title: "Factura (Proveedor)", path: "/compras/factura-proveedor" },
      { title: "Devolucion (Proveedor)", path: "/compras/devolucion-proveedor" },
    ],
  },
  {
    icon: Truck,
    title: "Ventas",
    path: "/ventas",
    subItems: [
      { title: "Guia de despacho", path: "/ventas/guia-de-despacho" },
      { title: "Orden de compra", path: "/ventas/orden-de-compra" },
      { title: "Factura (cliente)", path: "/ventas/factura-cliente" },
      { title: "Devolucion (Cliente)", path: "/ventas/devolucion-cliente" },
    ],
  },
]

export function AppSidebar() {
  const { user: currentUser } = useAuth()

  const items = currentUser?.is_superuser
    ? [...baseItems, ...sidebarItems, { icon: Users, title: "Admin", path: "/admin" }]
    : [...baseItems, ...sidebarItems]

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <Logo variant="responsive" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
