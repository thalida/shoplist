import {
  useQuery as vUseQuery,
  useMutation as vUseMutation,
  type QueryCompositeOptions,
  type QueryVariables,
  type Operation,
  type QueryExecutionContext,
  type MaybeRef,
} from "villus";
import merge from "lodash/merge";
import { useUserStore } from '@/stores/user';

interface MutationExecutionOptions {
  context: MaybeRef<QueryExecutionContext>;
}

export function useQuery<TData, TVars = QueryVariables>(opts: QueryCompositeOptions<TData, TVars>) {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isAuthenticated;

  const context = {
    headers: null as Record<string, string> | null,
  };

  if (isAuthenticated && userStore.accessToken !== null) {
    context.headers = {
      Authorization: `JWT ${userStore.accessToken}`,
    };
  }

  return vUseQuery(merge(opts, { context }));
}

export function useMutation<TData, TVars = QueryVariables>(
  query: Operation<TData, TVars>["query"],
  opts?: MutationExecutionOptions
) {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isAuthenticated;

  const context = {
    headers: null as Record<string, string> | null,
  };

  if (isAuthenticated && userStore.accessToken !== null) {
    context.headers = {
      Authorization: `JWT ${userStore.accessToken}`,
    };
  }

  return vUseMutation(query, merge(opts, { context }));
}
