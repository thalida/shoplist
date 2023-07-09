export interface IUser {
  uid: string,
  email: string,
  first_name: string,
  last_name: string,
  avatar: string,
}

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
