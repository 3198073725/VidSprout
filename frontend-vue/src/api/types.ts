export interface Paginated<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface LoginResponse {
  email?: string
  username?: string
  token: string
}

export interface UserSummary {
  description?: string
  date_added?: string
  name?: string
  is_featured?: boolean
  thumbnail_url?: string | null
  url?: string
  api_url?: string
  username: string
  advancedUser?: boolean
  is_editor?: boolean
  is_manager?: boolean
  email_is_verified?: boolean
  notification_on_comments?: boolean
}

export interface MediaItem {
  id: number
  friendly_token: string
  url: string
  api_url: string
  user: string
  title: string
  description?: string
  add_date?: string
  edit_date?: string
  views?: number
  media_type?: string
  state?: string
  duration?: number
  thumbnail_url?: string | null
  poster_url?: string | null
  preview_url?: string | null
  author_name?: string
  author_profile?: string
  author_thumbnail?: string | null
  encoding_status?: string
  likes?: number
  dislikes?: number
  reported_times?: number
  featured?: boolean
  user_featured?: boolean
  size?: number
  // 标签和分类信息（从后端同步）
  categories_info?: Array<{ title: string; description?: string }>
  tags_info?: Array<{ title: string }>
}

export interface MediaDetail extends MediaItem {
  encodings_info?: Array<{ id: number; profile: string; url: string; size: number }>
  original_media_url?: string
  video_height?: number
  enable_comments?: boolean
  // categories_info 和 tags_info 已在 MediaItem 中定义
  hls_info?: { playlist_url: string; segments?: number }
  subtitles_info?: Array<{ language: string; label: string; url: string }>
  chapter_data?: Array<{ title: string; start_time: number; end_time: number }>
  ratings_info?: { average: number; count: number }
  // MediaPublish 需要的字段
  is_public?: boolean
  categories?: Category[]
  tags?: Tag[]
  allow_comments?: boolean
}

export interface CommentItem {
  add_date: string
  text: string
  parent: string | null
  author_thumbnail_url?: string | null
  author_profile?: string
  author_name: string
  media_url: string
  uid: string
  likes?: number
  reply_count?: number
  hot_score?: number
  user_liked?: boolean
  children?: CommentItem[]
}

// 管理后台评论数据（扩展字段）
export interface ManageCommentItem extends CommentItem {
  user?: {
    username: string
    name?: string
    avatar_url?: string
  }
  media?: {
    friendly_token: string
    title: string
    thumbnail_url?: string
  }
  likes?: number
  reported_times?: number
  publish_date?: string
}

export interface PlaylistItemSummary {
  friendly_token: string
  url: string
  api_url: string
  user: string
  title: string
  description?: string
  add_date?: string
  views?: number
  media_type?: string
  state?: string
  duration?: number
  thumbnail_url?: string | null
  is_reviewed?: boolean
  preview_url?: string | null
  author_name?: string
  author_profile?: string
  author_thumbnail?: string | null
  encoding_status?: string
  likes?: number
  dislikes?: number
  reported_times?: number
  featured?: boolean
  user_featured?: boolean
  size?: number
}

export interface PlaylistDetail {
  title: string
  add_date?: string
  user_thumbnail_url?: string | null
  description?: string
  user: string
  media_count: number
  url: string
  thumbnail_url?: string | null
  playlist_media: PlaylistItemSummary[]
}

export interface Category {
  id: number
  title: string
  description?: string
  is_global?: boolean
  media_count?: number
  user?: string
  thumbnail_url?: string | null
}

export interface Tag {
  id: number
  title: string
  media_count?: number
  thumbnail_url?: string | null
}

// 媒体操作响应
export interface MediaActionResponse {
  detail: string
  action?: string
  media?: string
  action_type?: string // 新增：操作类型（like/unlike/dislike/undislike）
}

// 用户媒体操作数据
export interface UserMediaActionData {
  action: 'like' | 'dislike' | 'watch' | 'report' | 'rate'
  timestamp?: string
}

// 用户操作状态响应
export interface UserActionStatus {
  user_liked: boolean
  user_disliked: boolean
  likes: number
  dislikes: number
  reported?: Array<{ reported_date: string; reason: string }>
  filter?: <T>(predicate: (item: T) => boolean) => UserActionStatus[]
}

// 搜索相关类型
export interface SearchSuggestionItem {
  id: number
  keyword: string
  suggestion_type: 'popular' | 'related' | 'corrected' | 'trending'
  weight: number
  search_count: number
  click_count: number
}

export interface SearchHistoryItem {
  id: number
  query: string
  search_count: number
  last_searched: string
  created_at: string
}

export interface SearchStats {
  total_searches: number
  popular_queries: string[]
  trending_queries: string[]
  user_history: string[]
}

// 高级搜索参数
export interface AdvancedSearchParams {
  q: string
  media_type?: 'video' | 'audio' | 'image'
  category?: string
  tag?: string
  author?: string
  duration_min?: number
  duration_max?: number
  upload_date?: 'today' | 'this_week' | 'this_month' | 'this_year'
  sort_by?: 'relevance' | 'add_date' | 'views' | 'likes' | 'duration'
  ordering?: 'asc' | 'desc'
  highlight?: boolean
  page?: number
}

// 设备管理相关类型
export interface Device {
  id: string
  device_type: 'desktop' | 'mobile' | 'tablet'
  login_time: string
  ip_address: string
  user_agent?: string
}

// 重新导出用户相关类型
export type { UserProfile, EmailAddress } from './users'
