import {
  type UserNode,
} from "@/api/gql/graphql";

export interface IUser extends UserNode {}

export interface IUsers {
  [key: string]: IUser
}
