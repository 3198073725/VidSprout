import http from '../services/http'
import type { Paginated, CommentItem } from './types'

const BASE = '/v1'

export interface CommentsListParams {
  page?: number
  author?: string
}

export interface EnhancedCommentsListParams {
  page?: number
  page_size?: number
  sort?: 'newest' | 'hottest' | 'most_liked'
  parent?: string
}

export interface CommentLikeResponse {
  detail: string
}

export function listAllComments(params?: CommentsListParams): Promise<Paginated<CommentItem>> {
  return http.get(`${BASE}/comments`, { params })
}

// 增强的评论列表API
export function listMediaCommentsEnhanced(
  friendlyToken: string,
  params?: EnhancedCommentsListParams
): Promise<Paginated<CommentItem>> {
  return http.get(`${BASE}/media/${friendlyToken}/comments/enhanced`, { params })
}

// 原有的评论列表API（添加排序支持）
export function listMediaComments(
  friendlyToken: string, 
  params?: { 
    page?: number
    sort?: 'newest' | 'hottest' | 'most_liked'
  }
): Promise<Paginated<CommentItem>> {
  return http.get(`${BASE}/media/${friendlyToken}/comments`, { params })
}

export interface CreateCommentPayload {
  text: string
  parent?: string | null
}

export function createMediaComment(friendlyToken: string, payload: CreateCommentPayload): Promise<CommentItem> {
  return http.post(`${BASE}/media/${friendlyToken}/comments`, payload)
}

export function getCommentDetail(friendlyToken: string, uid: string): Promise<CommentItem> {
  return http.get(`${BASE}/media/${friendlyToken}/comments/${uid}`)
}

export function updateComment(friendlyToken: string, uid: string, payload: Partial<CreateCommentPayload>): Promise<CommentItem> {
  // docs show POST for update
  return http.post(`${BASE}/media/${friendlyToken}/comments/${uid}`, payload)
}

export function deleteComment(friendlyToken: string, uid: string): Promise<void> {
  return http.delete(`${BASE}/media/${friendlyToken}/comments/${uid}`)
}

// 评论点赞功能
export function likeComment(uid: string): Promise<CommentLikeResponse> {
  return http.post(`${BASE}/comments/${uid}/like`)
}

export function unlikeComment(uid: string): Promise<CommentLikeResponse> {
  return http.delete(`${BASE}/comments/${uid}/like`)
}
