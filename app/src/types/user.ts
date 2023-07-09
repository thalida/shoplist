export interface IUser {
  uid: string,
  username: string,
  email: string,
  first_name: string,
  last_name: string,
}

export interface IGoogleAuthRes {
  access_token: string,
  refresh_token: string,
  expires_in: number,
  token_type: string,
  scope: string,
}
