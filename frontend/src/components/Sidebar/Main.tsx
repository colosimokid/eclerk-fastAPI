import { Link as RouterLink, useRouterState } from "@tanstack/react-router"
import { ChevronDown } from "lucide-react"
import type { LucideIcon } from "lucide-react"
import * as React from "react"

import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  useSidebar,
} from "@/components/ui/sidebar"

export type SubItem = {
  title: string
  path: string
  icon?: LucideIcon
}

export type Item = {
  icon: LucideIcon
  title: string
  path: string
  subItems?: SubItem[]
}

interface MainProps {
  items: Item[]
}

export function Main({ items }: MainProps) {
  const { isMobile, setOpenMobile } = useSidebar()
  const [openSections, setOpenSections] = React.useState<Record<string, boolean>>({})
  const router = useRouterState()
  const currentPath = router.location.pathname

  const handleMenuClick = () => {
    if (isMobile) {
      setOpenMobile(false)
    }
  }

  const toggleSection = (title: string) => {
    setOpenSections((prev) => ({ ...prev, [title]: !prev[title] }))
  }

  return (
    <SidebarGroup>
      <SidebarGroupContent>
        <SidebarMenu>
          {items.map((item) => {
            const isActive =
              currentPath === item.path ||
              item.subItems?.some((subItem) => currentPath === subItem.path)

            const isOpen = openSections[item.title] ?? false

            return (
              <React.Fragment key={item.title}>
                <SidebarMenuItem>
                  <SidebarMenuButton
                    tooltip={item.title}
                    isActive={isActive}
                    onClick={() =>
                      item.subItems ? toggleSection(item.title) : undefined
                    }
                    asChild
                  >
                    {item.subItems ? (
                      <button type="button" className="flex w-full items-center gap-2">
                        <item.icon />
                        <span>{item.title}</span>
                        <ChevronDown
                          className={`ml-auto transition-transform duration-150 ${
                            isOpen ? "rotate-180" : ""
                          }`}
                        />
                      </button>
                    ) : (
                      <RouterLink to={item.path} onClick={handleMenuClick}>
                        <item.icon />
                        <span>{item.title}</span>
                      </RouterLink>
                    )}
                  </SidebarMenuButton>
                </SidebarMenuItem>
                {item.subItems && isOpen && (
                  <SidebarMenuSub>
                    {item.subItems.map((subItem) => {
                      const isSubActive = currentPath === subItem.path

                      return (
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton
                            asChild
                            isActive={isSubActive}
                          >
                            <RouterLink
                              to={subItem.path}
                              onClick={handleMenuClick}
                            >
                              <span>{subItem.title}</span>
                            </RouterLink>
                          </SidebarMenuSubButton>
                        </SidebarMenuSubItem>
                      )
                    })}
                  </SidebarMenuSub>
                )}
              </React.Fragment>
            )
          })}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}
