import http from '../services/http'
import type { Category, Tag, Paginated, MediaItem } from './types'

const BASE = '/v1'

export function listCategories(): Promise<Category[]> {
  return http.get(`${BASE}/categories`)
}

export function listTags(params?: { page?: number }): Promise<Paginated<Tag>> {
  return http.get(`${BASE}/tags`, { params })
}

export function search(params?: Record<string, any>): Promise<Paginated<MediaItem>> {
  return http.get(`${BASE}/search`, { params })
}

// 联系表单接口
export interface ContactFormPayload {
  name: string
  email: string
  subject: string
  message: string
}

export function submitContactForm(payload: ContactFormPayload): Promise<{ detail: string }> {
  return http.post(`${BASE}/contact`, payload)
}
