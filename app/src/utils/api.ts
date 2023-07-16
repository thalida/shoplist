import type { IOrderBy } from '@/types/api'
import { isObject } from '@/utils/general'
import { findIndex } from 'lodash'

export function humanizeGraphQLResponse(input: any) {
  if (!input) return null
  const output: Record<string, any> = {}

  Object.keys(input).forEach(key => {
    if (input[key] && input[key].edges) {
      output[key] = input[key].edges.map((edge: Record<string, any>) => humanizeGraphQLResponse(edge.node))
    } else if (isObject(input[key])) {
      output[key] = humanizeGraphQLResponse(input[key])
    } else {
      output[key] = input[key]
    }
  })

  return output
}

export function formatOrderByArgs(orderBy: IOrderBy[] | null | undefined, keyMap: Record<string, string> = {}) {
    if (typeof orderBy === "undefined" || orderBy === null) {
      return "";
    }

    const orderByStr = orderBy.map((order) => {
      const queryKey = keyMap[order.field] || order.field

      if (order.value === null) {
        return '';
      }

      return `${order.value ? "" : "-"}${queryKey}`;
    }).join(",");

    return orderByStr;
  }

export function toggleOrderByField(orderBy: IOrderBy[], field: string) {
    const index = findIndex(orderBy, { field })
    const currOrder = orderBy[index]
    const newOrder: IOrderBy = {
      field,
      value: null
    }

    if (typeof currOrder === 'undefined' || currOrder.value === null) {
      newOrder.value = true
    } else if (currOrder.value === true) {
      newOrder.value = false
    } else if (currOrder.value === false) {
      newOrder.value = null
    }

    orderBy = orderBy.filter((order) => order.field !== field)
    orderBy.unshift(newOrder)

    return orderBy
  }
