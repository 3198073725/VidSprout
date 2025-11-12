import http from '../services/http'
import type { 
  SearchSuggestionItem, 
  SearchHistoryItem, 
  SearchStats, 
  AdvancedSearchParams,
  Paginated,
  MediaItem 
} from './types'

const BASE = '/v1'

// 获取搜索建议
export function getSearchSuggestions(
  query: string, 
  limit: number = 10, 
  type: string = 'popular'
): Promise<SearchSuggestionItem[]> {
  return http.get(`${BASE}/search/suggestions/`, {
    params: { q: query, limit, type }
  })
}

// 获取搜索历史
export function getSearchHistory(): Promise<SearchHistoryItem[]> {
  return http.get(`${BASE}/search/history/`)
}

// 保存搜索历史（使用localStorage）
export function saveSearchHistory(query: string): Promise<{ status: string }> {
  try {
    if (!query.trim()) {
      return Promise.resolve({ status: 'empty' })
    }
    
    // 从 localStorage 获取现有历史
    const historyStr = localStorage.getItem('mediacms_search_history')
    let history: SearchHistoryItem[] = historyStr ? JSON.parse(historyStr) : []
    
    // 查找是否已存在
    const existingIndex = history.findIndex(item => item.query.toLowerCase() === query.toLowerCase())
    
    if (existingIndex > -1) {
      // 更新现有记录
      const existingItem = history[existingIndex]
      if (existingItem) {
        existingItem.search_count++
        existingItem.last_searched = new Date().toISOString()
      }
    } else {
      // 添加新记录
      const newItem: SearchHistoryItem = {
        id: Date.now(),
        query: query.trim(),
        search_count: 1,
        last_searched: new Date().toISOString(),
        created_at: new Date().toISOString()
      }
      history.unshift(newItem)
    }
    
    // 只保留最近30条
    history = history.slice(0, 30)
    
    // 保存回 localStorage
    localStorage.setItem('mediacms_search_history', JSON.stringify(history))
    
    return Promise.resolve({ status: 'success' })
  } catch (error) {
    console.error('保存搜索历史失败:', error)
    return Promise.resolve({ status: 'error' })
  }
}

// 清空搜索历史
export function clearSearchHistory(): Promise<void> {
  return http.delete(`${BASE}/search/history/`)
}

// 获取搜索统计
export function getSearchStats(): Promise<SearchStats> {
  return http.get(`${BASE}/search/stats/`)
}

// 增强版搜索（使用标准搜索端点）
export function enhancedSearch(params: AdvancedSearchParams): Promise<Paginated<MediaItem>> {
  // 转换参数名以匹配后端 API（后端使用 c/t 而不是 category/tag）
  const backendParams: Record<string, unknown> = {
    q: params.q,
    media_type: params.media_type,
    c: params.category,  // category -> c
    t: params.tag,       // tag -> t
    author: params.author,
    duration_min: params.duration_min,
    duration_max: params.duration_max,
    upload_date: params.upload_date,
    sort_by: params.sort_by,
    ordering: params.ordering,
    highlight: params.highlight,
    page: params.page
  }
  
  // 移除 undefined 值
  Object.keys(backendParams).forEach(key => {
    if (backendParams[key] === undefined) {
      delete backendParams[key]
    }
  })
  
  return http.get(`${BASE}/search`, { params: backendParams })
}

// 点击搜索建议（用于统计）
export function clickSuggestion(keyword: string): Promise<void> {
  // 这里可以调用后端API记录点击行为
  console.log(`点击搜索建议: ${keyword}`)
  return Promise.resolve()
}