/**
 * 评分相关API
 */
import http from '../services/http'

const BASE = '/v1'

// 评分分类接口
export interface RatingCategory {
  id: number
  title: string
  description: string
  enabled: boolean
}

// 媒体评分统计接口
export interface MediaRatingStats {
  category_id: number
  category_title: string
  average_score: number | null
  count: number
  user_score: number | null
}

export interface MediaRatingsResponse {
  ratings: MediaRatingStats[]
}

/**
 * 获取所有启用的评分分类
 */
export function getRatingCategories(): Promise<RatingCategory[]> {
  return http.get(`${BASE}/rating-categories`)
}

/**
 * 获取媒体的评分统计
 */
export function getMediaRatings(friendlyToken: string): Promise<MediaRatingsResponse> {
  return http.get(`${BASE}/media/${friendlyToken}/ratings`)
}

/**
 * 给媒体评分
 */
export function rateMedia(
  friendlyToken: string,
  categoryId: number,
  score: number
): Promise<{ detail: string; action_type: string }> {
  return http.post(`${BASE}/media/${friendlyToken}/actions`, {
    type: 'rate',
    extra_info: JSON.stringify({
      category_id: categoryId,
      score: score
    })
  })
}

