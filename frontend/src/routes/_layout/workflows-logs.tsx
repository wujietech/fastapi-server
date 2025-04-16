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

import { WorkflowLogPublic, WorkflowLogService } from "@/client"
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
      WorkflowLogService.readWorkflowLogs({ pageNumber, pageSize: PER_PAGE }),
    queryKey: ["workflows", { pageNumber }],
  }
}

export const Route = createFileRoute("/_layout/workflows-logs")({
  component: Items,
  validateSearch: (search) => itemsSearchSchema.parse(search),
})

function WorkflowActionsMenu({ log }: { log: WorkflowLogPublic }) {
  return (
    <Flex gap={2}>
      <Button
        leftIcon={<FiEdit />}
        variant="ghost"
        size="sm"
        onClick={() => console.log('编辑', log.id)}
      >
        编辑
      </Button>
      <Button
        leftIcon={<FiTrash2 />}
        variant="ghost"
        size="sm"
        onClick={() => console.log('删除', log.id)}
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

  const workflows = data?.data?.items ?? []
  const total = data?.data?.total ?? 0

  if (isLoading) {
    return <PendingItems />
  }

  if (workflows.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>暂无工作流数据</EmptyState.Title>
            <EmptyState.Description>
              添加一个新的工作流开始使用
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
          {workflows.map((workflow: WorkflowPublic) => (
            <Table.Row key={workflow.id} opacity={isPlaceholderData ? 0.5 : 1}>
              <Table.Cell truncate maxW="sm">
                {workflow.id}
              </Table.Cell>
              <Table.Cell truncate maxW="sm">
                {workflow.name}
              </Table.Cell>
              <Table.Cell
                color={!workflow.description ? "gray" : "inherit"}
                truncate
                maxW="30%"
              >
                {workflow.description || "N/A"}
              </Table.Cell>
              <Table.Cell>
                {/* <CategoryActionsMenu category={category} /> */}
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
      {/* <Heading size="lg" pt={12}>
        工作流日志
      </Heading> */}
      <ItemsTable />
    </Container>
  )
}
