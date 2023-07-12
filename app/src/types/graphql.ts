import type { PageInfo } from "@/api/gql/graphql";
import type { CombinedError } from "villus";

export interface IPageInfo extends PageInfo {
  totalCount: number;
}

export interface IFilterBy {
  [key: string]: any,
}

export interface IOrderBy {
  [key: string]: boolean | null,
}

export interface IError extends CombinedError {}
