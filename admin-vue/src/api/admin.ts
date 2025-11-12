import http from './http'
import type { Paginated, MediaItem, UserProfile, StatsData, BatchOperationParams, BatchOperationResult } from './types'

const BASE = '/v1'

// ==================== 数据统计 ====================

export function getDashboardStats(): Promise<any> {
  return http.get(`${BASE}/admin/dashboard/stats`)
}

// ==================== 批量操作 ====================

/**
 * 批量操作媒体
 */
export function batchMediaAction(mediaIds: string[], action: string, extra?: any): Promise<any> {
  return http.post(`${BASE}/admin/media/batch`, {
    media_ids: mediaIds,
    action,
    ...extra
  })
}

/**
 * 批量操作用户
 */
export function batchUserAction(userIds: string[], action: string): Promise<any> {
  return http.post('/v1/admin/users/batch', {
    user_ids: userIds,
    action
  })
}

// ==================== 媒体管理 ====================

export interface ManageMediaParams {
  page?: number
  sort_by?: 'title' | 'add_date' | 'edit_date' | 'views' | 'likes' | 'reported_times'
  ordering?: 'asc' | 'desc'
  state?: 'private' | 'public' | 'unlisted'
  search?: string
  encoding_status?: 'pending' | 'running' | 'success' | 'fail'
  featured?: 'true' | 'false' | 'all'
  is_reviewed?: 'true' | 'false' | 'all'
  category?: string
  media_type?: 'video' | 'image' | 'audio' | 'pdf'
}

export function getManageMedia(params?: ManageMediaParams): Promise<Paginated<MediaItem>> {
  return http.get(`${BASE}/manage_media`, { params })
}

export function batchDeleteMedia(ids: string[]): Promise<any> {
  return batchMediaAction(ids, 'delete')
}

export function batchUpdateMediaState(ids: string[], state: string): Promise<any> {
  const actionMap: Record<string, string> = {
    'public': 'set_public',
    'private': 'set_private',
    'unlisted': 'set_unlisted'
  }
  return batchMediaAction(ids, actionMap[state] || state)
}

export function batchFeatureMedia(ids: string[], featured: boolean): Promise<any> {
  return batchMediaAction(ids, featured ? 'feature' : 'unfeature')
}

export function batchApproveMedia(ids: string[]): Promise<any> {
  return batchMediaAction(ids, 'approve')
}

export function batchRejectMedia(ids: string[]): Promise<any> {
  return batchMediaAction(ids, 'reject')
}

export function batchSetCategory(ids: string[], category: string): Promise<any> {
  return batchMediaAction(ids, 'set_category', { category })
}

// ==================== 用户管理 ====================

export interface ManageUsersParams {
  page?: number
  sort_by?: 'name' | 'date_added'
  ordering?: 'asc' | 'desc'
  role?: 'all' | 'manager' | 'editor'
  is_approved?: 'true' | 'false'
}

export function getManageUsers(params?: ManageUsersParams): Promise<Paginated<UserProfile>> {
  return http.get(`${BASE}/manage_users`, { params })
}

export function batchDeleteUsers(ids: string[]): Promise<any> {
  return batchUserAction(ids, 'delete')
}

export function batchBlockUsers(ids: string[]): Promise<any> {
  return batchUserAction(ids, 'block')
}

export function batchUnblockUsers(ids: string[]): Promise<any> {
  return batchUserAction(ids, 'unblock')
}

export function batchSetEditor(ids: string[]): Promise<any> {
  return batchUserAction(ids, 'set_editor')
}

export function batchSetManager(ids: string[]): Promise<any> {
  return batchUserAction(ids, 'set_manager')
}

export function batchRemoveRole(ids: string[]): Promise<any> {
  return batchUserAction(ids, 'remove_role')
}

/**
 * 单个用户操作
 */
export function blockUser(userId: number): Promise<any> {
  return http.post(`${BASE}/admin/users/${userId}/actions`, {
    action: 'block'
  })
}

export function unblockUser(userId: number): Promise<any> {
  return http.post(`${BASE}/admin/users/${userId}/actions`, {
    action: 'unblock'
  })
}

// ==================== 评论管理 ====================

export interface ManageCommentsParams {
  page?: number
  sort_by?: 'text' | 'add_date'
  ordering?: 'asc' | 'desc'
}

export function getManageComments(params?: ManageCommentsParams): Promise<Paginated<any>> {
  return http.get(`${BASE}/manage_comments`, { params })
}

export function deleteComments(commentIds: string[]): Promise<void> {
  return http.delete(`${BASE}/manage_comments?comment_ids=${commentIds.join(',')}`)
}

// ==================== 系统监控 ====================

export function getSystemMonitoring(): Promise<any> {
  return http.get(`${BASE}/admin/system/monitoring`)
}

// ==================== 其他 ====================

export function getPopularCategories(): Promise<any[]> {
  return http.get(`${BASE}/admin/categories/popular`)
}

export function getActiveUsers(): Promise<UserProfile[]> {
  return http.get(`${BASE}/admin/users/active`)
}

export function exportData(params: {
  type: 'users' | 'media' | 'comments'
  format: 'csv' | 'excel' | 'json'
}): Promise<{ download_url: string; filename: string }> {
  return http.post(`${BASE}/admin/export`, params)
}

// ==================== 举报管理 ====================

export interface ManageReportsParams {
  page?: number
  page_size?: number
  status?: 'pending' | 'resolved' | 'ignored'
  search?: string
}

export interface ReportItem {
  id: number
  type: 'media' | 'comment' | 'user'
  target_id: string
  target_title: string
  target_url?: string
  reason: string
  description?: string
  status: 'pending' | 'resolved' | 'ignored'
  reporter_id: string
  reporter_name: string
  created_at: string
  handled_at?: string
  handler_name?: string
  media?: {
    friendly_token: string
    title: string
    thumbnail_url: string
    author: string
    views: number
    reported_times: number
  }
}

export function getManageReports(params?: ManageReportsParams): Promise<Paginated<ReportItem>> {
  return http.get(`${BASE}/admin/reports`, { params })
}

export function handleReport(reportId: number, action: 'resolve' | 'ignore' | 'delete_media', note?: string): Promise<any> {
  return http.post(`${BASE}/admin/reports/${reportId}`, { action, note })
}

export function getReportStats(): Promise<{
  total: number
  pending: number
  resolved: number
  ignored: number
  today: number
  most_reported_media: Array<{
    friendly_token: string
    title: string
    reported_times: number
    thumbnail_url: string
  }>
}> {
  return http.get(`${BASE}/admin/reports/stats`)
}

// 兼容性导出（保持向后兼容）
export const AdminAPI = {
  getDashboardStats,
  getManageMedia,
  getManageUsers,
  getManageComments,
  deleteComments,
  batchDeleteMedia,
  batchUpdateMediaState,
  batchFeatureMedia,
  batchApproveMedia,
  batchRejectMedia,
  batchSetCategory,
  batchDeleteUsers,
  batchBlockUsers,
  batchUnblockUsers,
  batchSetEditor,
  batchSetManager,
  batchRemoveRole,
  blockUser,
  unblockUser,
  getSystemMonitoring,
  getPopularCategories,
  getActiveUsers,
  exportData,
  getManageReports,
  handleReport,
  getReportStats
}
