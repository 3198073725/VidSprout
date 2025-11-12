import http from '../services/http'
import type { Paginated, MediaItem, ManageCommentItem } from './types'
import type { UserProfile } from './users'

const BASE = '/v1'

// ==================== 数据统计 ====================

export interface StatsData {
  userGrowth: Array<{ date: string; count: number }>
  mediaUpload: Array<{ date: string; count: number }>
  activity: Array<{ label: string; count: number }>
  mediaType: Array<{ type: string; count: number }>
  overview: {
    totalUsers: number
    totalMedia: number
    totalComments: number
    activeUsers: number
    userGrowth: number
    mediaGrowth: number
    commentGrowth: number
    activityGrowth: number
  }
}

export interface StatsParams {
  date_range?: '7d' | '30d' | '90d' | '1y'
  start_date?: string
  end_date?: string
}

export function getAdminStats(params?: StatsParams): Promise<StatsData> {
  return http.get(`${BASE}/admin/stats`, { params })
}

// ==================== 批量操作 ====================

export interface BatchOperationParams {
  ids: string[]
  operation: string
  [key: string]: any
}

export interface BatchOperationResult {
  success: boolean
  processed: number
  failed: number
  errors?: string[]
}

export function executeBatchOperation(params: BatchOperationParams): Promise<BatchOperationResult> {
  return http.post(`${BASE}/admin/batch`, params)
}

// ==================== 数据导出 ====================

export interface ExportParams {
  type: 'users' | 'media' | 'comments'
  format: 'csv' | 'excel' | 'json'
  date_range?: '7d' | '30d' | '90d' | '1y'
  start_date?: string
  end_date?: string
  filters?: Record<string, any>
}

export function exportData(params: ExportParams): Promise<{ download_url: string; filename: string }> {
  return http.post(`${BASE}/admin/export`, params)
}

// ==================== 媒体管理 ====================

export interface ManageMediaParams {
  page?: number
  sort_by?: 'title' | 'add_date' | 'edit_date' | 'views' | 'likes' | 'reported_times'
  ordering?: 'asc' | 'desc'
  state?: 'private' | 'public' | 'unlisted'
  search?: string
}

export function getManageMedia(params?: ManageMediaParams): Promise<Paginated<MediaItem>> {
  return http.get(`${BASE}/manage_media`, { params })
}

// 批量删除媒体
export function batchDeleteMedia(ids: string[]): Promise<BatchOperationResult> {
  return executeBatchOperation({
    ids,
    operation: 'delete',
    type: 'media'
  })
}

// 批量修改媒体状态
export function batchUpdateMediaState(ids: string[], state: string): Promise<BatchOperationResult> {
  return executeBatchOperation({
    ids,
    operation: 'update_state',
    type: 'media',
    state
  })
}

// 批量推荐媒体
export function batchFeatureMedia(ids: string[], featured: boolean): Promise<BatchOperationResult> {
  return executeBatchOperation({
    ids,
    operation: featured ? 'feature' : 'unfeature',
    type: 'media'
  })
}

// ==================== 评论管理 ====================

export interface ManageCommentsParams {
  page?: number
  sort_by?: string
  ordering?: 'asc' | 'desc'
}

export function getManageComments(params?: ManageCommentsParams): Promise<Paginated<ManageCommentItem>> {
  return http.get(`${BASE}/manage_comments`, { params })
}

export function deleteComments(commentIds: string[]): Promise<void> {
  return http.delete(`${BASE}/manage_comments`, {
    params: { comment_ids: commentIds.join(',') }
  })
}

// ==================== 用户管理 ====================

export interface ManageUsersParams {
  page?: number
  sort_by?: 'username' | 'name' | 'date_joined' | 'last_login'
  ordering?: 'asc' | 'desc'
  role?: 'all' | 'user' | 'editor' | 'manager' | 'admin'
}

export function getManageUsers(params?: ManageUsersParams): Promise<Paginated<UserProfile>> {
  return http.get(`${BASE}/manage_users`, { params })
}

// ==================== 任务管理 ====================

export interface TaskInfo {
  'profile name'?: string
  'media title'?: string
  'encoding progress'?: number
}

export interface Task {
  worker: string
  task_id: string
  args: string
  name: string
  time_start?: number
  info?: TaskInfo
}

export interface TasksResponse {
  active: {
    tasks: Task[]
  }
  reserved: {
    tasks: Task[]
  }
  scheduled: {
    tasks: Task[]
  }
  task_ids: string[]
  media_profile_pairs: [string, number][]
}

export function getTasks(): Promise<TasksResponse> {
  return http.get(`${BASE}/tasks`)
}

// ==================== 系统监控 ====================

export interface MonitoringData {
  timestamp: string
  system: {
    cpu_percent: number
    memory_percent: number
    memory_used_gb: number
    memory_total_gb: number
    disk_percent: number
    disk_used_gb: number
    disk_total_gb: number
    boot_time: string
    load_average?: number[]
  }
  network: {
    bytes_sent: number
    bytes_recv: number
    packets_sent: number
    packets_recv: number
  }
  processes: Array<{
    pid: number
    name: string
    cpu_percent: number
    memory_percent: number
  }>
  history: Array<{
    timestamp: string
    cpu: number
    memory: number
    disk: number
  }>
}

export interface AlertRule {
  cpu_threshold: number
  memory_threshold: number
  disk_threshold: number
  network_threshold: number
  enable_notifications: boolean
  notification_email: string
}

export interface PerformanceMetrics {
  timestamp: string
  time_range_hours: number
  application: {
    active_users: number
    active_sessions: number
    recent_media: number
    recent_comments: number
    db_queries: number
    slow_queries: number
  }
  cache: {
    hits: number
    misses: number
    hit_rate: number
  }
  system_load: {
    load_average?: number[]
    cpu_count: number
    load_percentage?: number
  }
}

export interface SystemAlert {
  id: string
  type: string
  title: string
  message: string
  timestamp: string
  severity: 'info' | 'warning' | 'error'
}

export interface MonitoringParams {
  hours?: number
  type?: 'all' | 'info' | 'warning' | 'error'
}

export function getSystemMonitoring(): Promise<MonitoringData> {
  return http.get(`${BASE}/monitoring/system`)
}

export function getAlertRules(): Promise<AlertRule> {
  return http.get(`${BASE}/monitoring/alert-rules`)
}

export function updateAlertRules(rules: AlertRule): Promise<void> {
  return http.post(`${BASE}/monitoring/alert-rules`, { rules })
}

export function getAlertHistory(params?: MonitoringParams): Promise<{
  alerts: SystemAlert[]
  total: number
  days: number
}> {
  return http.get(`${BASE}/monitoring/alert-history`, { params })
}

export function getPerformanceMetrics(hours?: number): Promise<PerformanceMetrics> {
  return http.get(`${BASE}/monitoring/performance`, { params: { hours } })
}

export function sendTestAlert(type: string, message: string): Promise<SystemAlert> {
  return http.post(`${BASE}/monitoring/test-alert`, { type, message })
}

// ==================== 权限管理 ====================

export interface Permission {
  id: number
  name: string
  codename: string
  content_type: string
  app_label: string
  group?: string
}

export interface Role {
  id: number
  name: string
  description: string
  user_count: number
  permissions: Permission[]
}

export interface UserPermission {
  user_id: number
  permissions: number[]
  roles: number[]
}

export interface PermissionAuditLog {
  id: string
  action: string
  user_id: number
  username: string
  target_user_id: number
  details: Record<string, any>
  timestamp: string
  ip_address: string
}

export interface PermissionInfo {
  user_permissions: Permission[]
  all_permissions: Permission[]
  roles: Role[]
}

export function getPermissionInfo(): Promise<PermissionInfo> {
  return http.get(`${BASE}/permissions/manage`)
}

export function updateUserPermissions(userId: number, permissions: number[], roles: number[]): Promise<void> {
  return http.post(`${BASE}/permissions/manage`, {
    user_id: userId,
    permissions,
    roles
  })
}

export function getRoles(): Promise<Role[]> {
  return http.get(`${BASE}/permissions/roles`)
}

export function createOrUpdateRole(role: Partial<Role>): Promise<void> {
  return http.post(`${BASE}/permissions/roles`, role)
}

export function deleteRole(roleId: number): Promise<void> {
  return http.delete(`${BASE}/permissions/roles`, {
    params: { id: roleId }
  })
}

export function getPermissionAuditLogs(params?: {
  user_id?: number
  days?: number
  action?: string
}): Promise<{
  logs: PermissionAuditLog[]
  total: number
  days: number
}> {
  return http.get(`${BASE}/permissions/audit`, { params })
}

export function logPermissionAudit(action: string, targetUserId: number, details: Record<string, any>): Promise<void> {
  return http.post(`${BASE}/permissions/audit`, {
    action,
    target_user_id: targetUserId,
    details
  })
}
