import http from '../services/http'
import type { Paginated, MediaItem } from './types'

export type UserAction = 'like' | 'dislike' | 'watch' | 'report' | 'rate'

export const getUserAction = async (action: UserAction, params?: { page?: number }): Promise<Paginated<MediaItem>> => {
  return http.get(`/v1/user/action/${action}`, { params })
}

export const clearUserAction = async (action: UserAction): Promise<{ detail: string; count: number; action: string }> => {
  return http.delete(`/v1/user/action/${action}`)
}
