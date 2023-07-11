import {
  type UserNode,
} from "@/api/gql/graphql";

export interface IUser extends UserNode {}

export interface IUsers {
  [key: string]: IUser
}

export interface IGoogleAuthRes {
  access_token: string,
  refresh_token: string,
  expires_in: number,
  token_type: string,
  scope: string,
}
