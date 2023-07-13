/* eslint-disable */
import * as types from './graphql';
import type { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 */
const documents = {
    "query AllProducts($first: Int, $after: String, $last: Int, $before: String, $orderBy: String, $name: String, $name_Icontains: String, $category: [ID], $store: [ID], $list: [ID]) {\n  allProducts(\n    first: $first\n    after: $after\n    last: $last\n    before: $before\n    orderBy: $orderBy\n    name: $name\n    name_Icontains: $name_Icontains\n    category: $category\n    stores: $store\n    lists: $list\n  ) {\n    totalCount\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n    edges {\n      node {\n        uid\n        name\n        category {\n          uid\n          name\n          color\n        }\n        stores {\n          edges {\n            node {\n              uid\n              name\n            }\n          }\n        }\n        lists {\n          edges {\n            node {\n              uid\n              name\n            }\n          }\n        }\n      }\n    }\n  }\n}": types.AllProductsDocument,
    "mutation RegisterSocial($socialAccessToken: String!, $socialBackend: String!) {\n  registerSocial(\n    input: {accessToken: $socialAccessToken, socialBackend: $socialBackend}\n  ) {\n    token\n  }\n}": types.RegisterSocialDocument,
    "mutation TokenAuth($username: String!, $password: String!) {\n  tokenAuth(input: {username: $username, password: $password}) {\n    token\n  }\n}": types.TokenAuthDocument,
    "mutation VerifyToken($token: String!) {\n  verifyToken(input: {token: $token}) {\n    payload\n  }\n}": types.VerifyTokenDocument,
    "query Me {\n  me {\n    id\n    uid\n    username\n    email\n    firstName\n    lastName\n    avatar\n  }\n}": types.MeDocument,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 *
 *
 * @example
 * ```ts
 * const query = graphql(`query GetUser($id: ID!) { user(id: $id) { name } }`);
 * ```
 *
 * The query argument is unknown!
 * Please regenerate the types.
 */
export function graphql(source: string): unknown;

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "query AllProducts($first: Int, $after: String, $last: Int, $before: String, $orderBy: String, $name: String, $name_Icontains: String, $category: [ID], $store: [ID], $list: [ID]) {\n  allProducts(\n    first: $first\n    after: $after\n    last: $last\n    before: $before\n    orderBy: $orderBy\n    name: $name\n    name_Icontains: $name_Icontains\n    category: $category\n    stores: $store\n    lists: $list\n  ) {\n    totalCount\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n    edges {\n      node {\n        uid\n        name\n        category {\n          uid\n          name\n          color\n        }\n        stores {\n          edges {\n            node {\n              uid\n              name\n            }\n          }\n        }\n        lists {\n          edges {\n            node {\n              uid\n              name\n            }\n          }\n        }\n      }\n    }\n  }\n}"): (typeof documents)["query AllProducts($first: Int, $after: String, $last: Int, $before: String, $orderBy: String, $name: String, $name_Icontains: String, $category: [ID], $store: [ID], $list: [ID]) {\n  allProducts(\n    first: $first\n    after: $after\n    last: $last\n    before: $before\n    orderBy: $orderBy\n    name: $name\n    name_Icontains: $name_Icontains\n    category: $category\n    stores: $store\n    lists: $list\n  ) {\n    totalCount\n    pageInfo {\n      hasNextPage\n      hasPreviousPage\n      startCursor\n      endCursor\n    }\n    edges {\n      node {\n        uid\n        name\n        category {\n          uid\n          name\n          color\n        }\n        stores {\n          edges {\n            node {\n              uid\n              name\n            }\n          }\n        }\n        lists {\n          edges {\n            node {\n              uid\n              name\n            }\n          }\n        }\n      }\n    }\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "mutation RegisterSocial($socialAccessToken: String!, $socialBackend: String!) {\n  registerSocial(\n    input: {accessToken: $socialAccessToken, socialBackend: $socialBackend}\n  ) {\n    token\n  }\n}"): (typeof documents)["mutation RegisterSocial($socialAccessToken: String!, $socialBackend: String!) {\n  registerSocial(\n    input: {accessToken: $socialAccessToken, socialBackend: $socialBackend}\n  ) {\n    token\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "mutation TokenAuth($username: String!, $password: String!) {\n  tokenAuth(input: {username: $username, password: $password}) {\n    token\n  }\n}"): (typeof documents)["mutation TokenAuth($username: String!, $password: String!) {\n  tokenAuth(input: {username: $username, password: $password}) {\n    token\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "mutation VerifyToken($token: String!) {\n  verifyToken(input: {token: $token}) {\n    payload\n  }\n}"): (typeof documents)["mutation VerifyToken($token: String!) {\n  verifyToken(input: {token: $token}) {\n    payload\n  }\n}"];
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "query Me {\n  me {\n    id\n    uid\n    username\n    email\n    firstName\n    lastName\n    avatar\n  }\n}"): (typeof documents)["query Me {\n  me {\n    id\n    uid\n    username\n    email\n    firstName\n    lastName\n    avatar\n  }\n}"];

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}

export type DocumentType<TDocumentNode extends DocumentNode<any, any>> = TDocumentNode extends DocumentNode<  infer TType,  any>  ? TType  : never;