import http from '../services/http'
import type { UserSummary, Paginated } from './types'

const BASE = '/v1'

// 扩展用户资料接口
export interface UserProfile extends UserSummary {
  id: number
  email?: string
  date_joined?: string
  last_login?: string
  is_active?: boolean
  is_staff?: boolean
  is_manager?: boolean
  is_editor?: boolean
}

// 邮箱地址接口
export interface EmailAddress {
  id: number
  email: string
  verified: boolean
  primary: boolean
}

export interface CreateUserPayload {
  username: string
  password: string
  email?: string
  name?: string
}

export async function createUser(payload: CreateUserPayload) {
  // MediaCMS 现在提供了专门的注册 API：/api/v1/register
  // 支持 JSON 和 FormData 格式，无需 CSRF token
  return http.post(`${BASE}/register`, {
    username: payload.username,
    password: payload.password,
    email: payload.email || '',
    name: payload.name || payload.username
  })
}

export interface UpdateUserPayload {
  name?: string
  description?: string
  logo?: File | Blob | null
}

export async function updateUser(username: string, payload: UpdateUserPayload) {
  const form = new FormData()
  if (payload.name) form.append('name', payload.name)
  if (payload.description) form.append('description', payload.description)
  if (payload.logo) form.append('logo', payload.logo)
  return http.post(`${BASE}/users/${encodeURIComponent(username)}`, form)
}

// 获取用户资料
export async function getUserProfile(username: string): Promise<UserProfile> {
  return http.get(`${BASE}/users/${encodeURIComponent(username)}`)
}

// 获取成员列表
export interface GetMembersParams {
  page?: number
  search?: string
  ordering?: string
}

export async function getMembers(params?: GetMembersParams): Promise<Paginated<UserProfile>> {
  return http.get(`${BASE}/users`, { params })
}

// 邮箱管理相关API
export async function getEmailAddresses(): Promise<EmailAddress[]> {
  return http.get(`${BASE}/user/emails`)
}

export async function setPrimaryEmail(email: string): Promise<void> {
  return http.post(`${BASE}/user/emails/set-primary`, { email })
}

export async function resendVerificationEmail(email: string): Promise<void> {
  return http.post(`${BASE}/user/emails/resend-verification`, { email })
}

export async function removeEmail(email: string): Promise<void> {
  return http.delete(`${BASE}/user/emails`, { data: { email } })
}

export async function addEmail(email: string): Promise<EmailAddress> {
  return http.post(`${BASE}/user/emails`, { email })
}
