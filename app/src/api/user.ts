import axios, { type AxiosResponse } from "axios";
import { API_URL, getConfig } from "@/api/index";
import type { IUser, IGoogleAuthRes } from "@/types/user";


export async function getMe() {
  const url = `${API_URL}/users/me/`;
  const config = getConfig()

  const res = await axios.get<never, AxiosResponse<IUser>>(url, config)

  return res.data
}

export async function updateMe(data: Partial<IUser>) {
  const url = `${API_URL}/users/me/`;
  const config = getConfig()

  const res = await axios.patch<Partial<IUser>, AxiosResponse<IUser>>(url, data, config)

  return res.data
}

export async function loginWithGoogle(googleToken: string) {
  const url = `${API_URL}/auth/convert-token/`;

  const res = await axios.post<{ access_token: string }, AxiosResponse<IGoogleAuthRes>>(url, {
    token: googleToken,
    grant_type: 'convert_token',
    backend: 'google-oauth2',
    client_id: import.meta.env.VITE_API_AUTH_CLIENT_ID,
    client_secret: import.meta.env.VITE_API_AUTH_CLIENT_SECRET,
  })

  return res.data
}

export async function logout() {
  const url = `${API_URL}/auth/invalidate-sessions/`;
  const config = getConfig()

  const res = await axios.post(url, {
    client_id: import.meta.env.VITE_API_AUTH_CLIENT_ID,
  }, config)

  return res.data
}
