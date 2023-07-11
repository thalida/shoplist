import { isObject } from '@/utils/general'

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
