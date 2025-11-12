import http from '../services/http'
import type { Paginated, MediaItem, MediaDetail, MediaActionResponse, UserMediaActionData, UserActionStatus } from './types'

const BASE = '/v1'

export interface MediaListParams {
  page?: number
  show?: 'recommended' | 'featured' | 'shared_by_me' | 'shared_with_me'
  author?: string
}

export function listMedia(params?: MediaListParams): Promise<Paginated<MediaItem>> {
  return http.get(`${BASE}/media`, { params })
}

export function getMediaDetail(friendlyToken: string): Promise<MediaDetail> {
  return http.get(`${BASE}/media/${friendlyToken}`)
}

export interface CreateMediaPayload {
  media_file: File | Blob
  title?: string
  description?: string
}

export function createMedia(payload: CreateMediaPayload): Promise<MediaDetail> {
  const form = new FormData()
  form.append('media_file', payload.media_file)
  if (payload.title) form.append('title', payload.title)
  if (payload.description) form.append('description', payload.description)
  return http.post(`${BASE}/media`, form)
}

export interface UpdateMediaPayload {
  title?: string
  description?: string
  media_file?: File | Blob
  uploaded_poster?: File | Blob
  state?: 'public' | 'private' | 'unlisted'
  tags?: string[]
  categories?: string[]
}

export function updateMedia(friendlyToken: string, payload: UpdateMediaPayload): Promise<MediaDetail> {
  const form = new FormData()
  if (payload.title) form.append('title', payload.title)
  if (payload.description) form.append('description', payload.description)
  if (payload.media_file) form.append('media_file', payload.media_file)
  if (payload.uploaded_poster) form.append('uploaded_poster', payload.uploaded_poster)
  if (payload.state) form.append('state', payload.state)
  if (payload.tags && payload.tags.length > 0) {
    payload.tags.forEach(tag => form.append('tags', tag))
    console.log(`📌 添加了 ${payload.tags.length} 个标签:`, payload.tags)
  }
  if (payload.categories && payload.categories.length > 0) {
    payload.categories.forEach(cat => form.append('category', cat))
    console.log(`📂 添加了 ${payload.categories.length} 个分类:`, payload.categories)
  }
  
  console.log('📤 发送更新请求到:', `${BASE}/media/${friendlyToken}`)
  return http.put(`${BASE}/media/${friendlyToken}`, form)
}

export function deleteMedia(friendlyToken: string): Promise<void> {
  return http.delete(`${BASE}/media/${friendlyToken}`)
}

export interface MediaManageActionPayload {
  type: 'encode' | 'review'
  encoding_profiles?: number[]
  result?: boolean
}

export function manageMedia(friendlyToken: string, payload: MediaManageActionPayload): Promise<{ detail: string }>{
  const form = new FormData()
  form.append('type', payload.type)
  if (payload.encoding_profiles) {
    payload.encoding_profiles.forEach((id) => form.append('encoding_profiles', String(id)))
  }
  if (typeof payload.result === 'boolean') form.append('result', String(payload.result))
  return http.post(`${BASE}/media/${friendlyToken}`, form)
}

export function getMediaActions(friendlyToken: string): Promise<UserActionStatus> {
  return http.get(`${BASE}/media/${friendlyToken}/actions`)
}

export function createMediaAction(friendlyToken: string, body: Record<string, string | number | boolean>): Promise<MediaActionResponse> {
  return http.post(`${BASE}/media/${friendlyToken}/actions`, body)
}

export function deleteMediaActions(friendlyToken: string): Promise<void> {
  return http.delete(`${BASE}/media/${friendlyToken}/actions`)
}

export interface BulkMediaActionsPayload {
  media_ids: string[]
  action:
    | 'enable_comments'
    | 'disable_comments'
    | 'delete_media'
    | 'enable_download'
    | 'disable_download'
    | 'add_to_playlist'
    | 'remove_from_playlist'
    | 'set_state'
    | 'change_owner'
    | 'copy_media'
  playlist_ids?: number[]
  state?: 'private' | 'public' | 'unlisted'
  owner?: string
}

export function bulkMediaActions(payload: BulkMediaActionsPayload): Promise<{ detail: string }>{
  return http.post(`${BASE}/media/user/bulk_actions`, payload)
}

// 用户对媒体的操作（点赞、不喜欢、观看、举报）
export interface UserMediaAction {
  action: 'like' | 'dislike' | 'watch' | 'report'
}

// 创建用户媒体操作（点赞、不喜欢、举报、观看）
export function createUserMediaAction(
  friendlyToken: string, 
  action: string, 
  extraInfo?: { reason?: string; description?: string; details?: string }
): Promise<MediaActionResponse> {
  // 后端API期望的参数名是 'type' 而不是 'action'
  const payload: any = { type: action }
  
  // 如果是举报操作，添加额外信息
  if (action === 'report' && extraInfo) {
    payload.extra_info = JSON.stringify({
      reason: extraInfo.reason || 'other',
      description: extraInfo.description || extraInfo.details || '',
      status: 'pending'
    })
  }
  
  console.log('📤 提交用户媒体操作:', { action, extraInfo, payload })
  
  return http.post(`${BASE}/media/${friendlyToken}/actions`, payload)
}

// 删除用户媒体操作（取消点赞/不喜欢等）
export function deleteUserMediaAction(friendlyToken: string, action: string): Promise<void> {
  // 后端API期望的参数名是 'type'
  return http.delete(`${BASE}/media/${friendlyToken}/actions`, { data: { type: action } })
}

// 获取用户的历史记录、喜欢的媒体等
export function getUserActionMedia(action: 'like' | 'dislike' | 'watch' | 'report' | 'rate', params?: { page?: number }): Promise<Paginated<MediaItem>> {
  return http.get(`${BASE}/user/action/${action}`, { params })
}

// 共享媒体相关API

// 获取我分享给别人的媒体
export function getSharedByMeMedia(params?: { page?: number }): Promise<Paginated<MediaItem>> {
  return listMedia({ ...params, show: 'shared_by_me' })
}

// 获取别人分享给我的媒体
export function getSharedWithMeMedia(params?: { page?: number }): Promise<Paginated<MediaItem>> {
  return listMedia({ ...params, show: 'shared_with_me' })
}
