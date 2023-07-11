import type { IUser } from "@/types/user"

export function getFullName(user: IUser) {
  const firstName = user.firstName
  const lastName = user.lastName
  return [firstName, lastName].join(" ")
}


export function getInitials(user: IUser) {
  const firstName = user.firstName || ""
  const lastName = user.lastName || ""
  return [firstName[0], lastName[0]].join("")
}
