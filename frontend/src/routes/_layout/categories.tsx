import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
  Button,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { FiEdit, FiTrash2, FiSearch } from "react-icons/fi"
import { z } from "zod"

import { CategoryPublic, CategoryService } from "@/client"
import PendingItems from "@/components/Pending/PendingItems"
import {
  PaginationItems,
  PaginationNextTrigger,
  PaginationPrevTrigger,
  PaginationRoot,
} from "@/components/ui/pagination.tsx"

const itemsSearchSchema = z.object({
  page: z.number().catch(1),
})

const PER_PAGE = 20

function getItemsQueryOptions({ pageNumber }: { pageNumber: number }) {
  return {
    queryFn: () =>
      CategoryService.readCategories({ pageNumber, pageSize: PER_PAGE }),
    queryKey: ["categories", { pageNumber }],
  }
}

export const Route = createFileRoute("/_layout/categories")({
  component: Items,
  validateSearch: (search) => itemsSearchSchema.parse(search),
})

function CategoryActionsMenu({ category }: { category: CategoryPublic }) {
  return (
    <Flex gap={2}>
      <Button
        leftIcon={<FiEdit />}
        variant="ghost"
        size="sm"
        onClick={() => console.log('编辑', category.id)}
      >
        编辑
      </Button>
      <Button
        leftIcon={<FiTrash2 />}
        variant="ghost"
        size="sm"
        onClick={() => console.log('删除', category.id)}
      >
        删除
      </Button>
    </Flex>
  )
}

function ItemsTable() {
  const navigate = useNavigate({ from: Route.fullPath })
  const { page } = Route.useSearch()

  const { data, isLoading, isPlaceholderData } = useQuery({
    ...getItemsQueryOptions({ pageNumber: page }),
    placeholderData: (prevData) => prevData,
  })

  const setPage = (page: number) =>
    navigate({
      search: (prev: { [key: string]: string }) => ({ ...prev, page }),
    })

  const categories = data?.data?.items ?? []
  const total = data?.data?.total ?? 0

  if (isLoading) {
    return <PendingItems />
  }

  if (categories.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>暂无分类数据</EmptyState.Title>
            <EmptyState.Description>
              添加一个新的分类开始使用
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  return (
    <>
      <Table.Root size={{ base: "sm", md: "md" }}>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader w="sm">ID</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Name</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Description</Table.ColumnHeader>
            <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {categories.map((category: CategoryPublic) => (
            <Table.Row key={category.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell truncate maxW="sm">
                {category.id}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {category.name}
              </Table.Cell>
              <Table.Cell
                color={!category.description ? "gray" : "inherit"}
                truncate
                maxW="30%"
              >
                {category.description || "N/A"}
              </Table.Cell>
              <Table.Cell>
                <CategoryActionsMenu category={category} />
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
      <Flex justifyContent="flex-end" mt={4}>
        <PaginationRoot
          count={total}
          pageSize={PER_PAGE}
          onPageChange={({ page }) => setPage(page)}
        >
          <Flex>
            <PaginationPrevTrigger />
            <PaginationItems />
            <PaginationNextTrigger />
          </Flex>
        </PaginationRoot>
      </Flex>
    </>
  )
}

function Items() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        分类管理
      </Heading>
      <ItemsTable />
    </Container>
  )
}
