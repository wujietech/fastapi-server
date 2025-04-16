/*
 * @Author: 李明(liming@inmyshow.com)
 * @Date: 2025-04-15 16:22:13
 * @LastEditors: 李明(liming@inmyshow.com)
 * @LastEditTime: 2025-04-16 18:38:00
 * @FilePath: /fastapi-server/frontend/src/components/Common/SidebarItems.tsx
 * @Description: 
 * 
 * Copyright (c) 2025 by 五街科技, All Rights Reserved. 
 */
import { Box, Flex, Icon, Text } from "@chakra-ui/react"
import { useQueryClient } from "@tanstack/react-query"
import { Link as RouterLink } from "@tanstack/react-router"
import { FiBriefcase, FiHome, FiSettings, FiUsers, FiBookmark, FiSend, FiLayers } from "react-icons/fi"
import type { IconType } from "react-icons/lib"

import type { UserPublic } from "@/client"
// react-icons/fi
const items = [
  { icon: FiHome, title: "Dashboard", path: "/" },
  { icon: FiBookmark, title: "分类", path: "/categories" },
  { icon: FiSend, title: "工作流", path: "/workflows" },
  { icon: FiLayers, title: "工作流日志", path: "/workflows-logs" },
  { icon: FiSettings, title: "User Settings", path: "/settings" },
  { icon: FiBriefcase, title: "Items", path: "/items" },
]

interface SidebarItemsProps {
  onClose?: () => void
}

interface Item {
  icon: IconType
  title: string
  path: string
}

const SidebarItems = ({ onClose }: SidebarItemsProps) => {
  const queryClient = useQueryClient()
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"])

  const finalItems: Item[] = currentUser?.is_superuser
    ? [...items, { icon: FiUsers, title: "Admin", path: "/admin" }]
    : items

  const listItems = finalItems.map(({ icon, title, path }) => (
    <RouterLink key={title} to={path} onClick={onClose}>
      <Flex
        gap={4}
        px={4}
        py={2}
        _hover={{
          background: "gray.subtle",
        }}
        alignItems="center"
        fontSize="sm"
      >
        <Icon as={icon} alignSelf="center" />
        <Text ml={2}>{title}</Text>
      </Flex>
    </RouterLink>
  ))

  return (
    <>
      <Text fontSize="xs" px={4} py={2} fontWeight="bold">
        Menu
      </Text>
      <Box>{listItems}</Box>
    </>
  )
}

export default SidebarItems
