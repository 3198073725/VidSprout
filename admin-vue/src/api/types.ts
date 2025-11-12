// 用户相关类型
export interface UserProfile {
  id: number
  username: string
  email: string
  name: string
  is_staff: boolean
  is_superuser: boolean
  is_manager?: boolean
  is_editor?: boolean
  logo?: string
  date_joined?: string
  last_login?: string
}

// 分页响应
export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// 媒体类型
export interface MediaItem {
  friendly_token: string
  title: string
  description?: string
  thumbnail_url?: string
  poster_url?: string
  media_type: 'video' | 'image' | 'audio' | 'pdf'
  state: 'public' | 'private' | 'unlisted'
  featured: boolean
  user_featured: boolean
  is_reviewed: boolean
  encoding_status: 'pending' | 'running' | 'success' | 'fail'
  listable: boolean
  views: number
  likes: number
  dislikes: number
  duration?: number
  add_date: string
  edit_date: string
  user: string
  author_name?: string
  categories_info?: Array<{ title: string; url: string }>
  tags_info?: Array<{ title: string; url: string }>
}

// 统计数据
export interface StatsData {
  overview: {
    totalMedia: number
    totalUsers: number
    totalComments: number
    activeUsers: number
    todayViews: number
    pendingReview: number
    mediaGrowth: number
    userGrowth: number
  }
  uploadTrend: Array<{ date: string; count: number }>
  mediaType: Array<{ type: string; count: number }>
  recentMedia: Array<{
    id: string
    title: string
    type: string
    author: string
    time: string
  }>
  systemStatus: {
    cpu: number
    memory: number
    disk: number
    tasks: number
    tasksCount: number
  }
}

// 批量操作
export interface BatchOperationParams {
  ids: string[]
  operation: string
  type: 'media' | 'users' | 'comments'
  [key: string]: any
}

export interface BatchOperationResult {
  success: boolean
  processed: number
  failed: number
  errors?: string[]
}

