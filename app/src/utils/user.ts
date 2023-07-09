import type { IUser } from "@/types/user"

export function getFullName(user: IUser) {
  const firstName = user['first_name']
  const lastName = user['last_name']
  return [firstName, lastName].join(" ")
}


export function getInitials(user: IUser) {
  const firstName = user['first_name'] || ""
  const lastName = user['last_name'] || ""
  return [firstName[0], lastName[0]].join("")
}
