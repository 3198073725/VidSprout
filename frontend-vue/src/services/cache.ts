import type { AxiosResponse } from 'axios'

interface CacheEntry {
  data: any
  timestamp: number
  expires: number
}

interface CacheConfig {
  maxAge?: number // 缓存最大存活时间 (ms)
  maxSize?: number // 缓存最大条目数
  keyGenerator?: (url: string, params?: any) => string // 缓存键生成器
}

class RequestCache {
  private cache: Map<string, CacheEntry>
  private config: Required<CacheConfig>

  constructor(config: CacheConfig = {}) {
    this.cache = new Map()
    this.config = {
      maxAge: config.maxAge || 5 * 60 * 1000, // 默认5分钟
      maxSize: config.maxSize || 100, // 默认100条
      keyGenerator: config.keyGenerator || this.defaultKeyGenerator
    }
  }

  private defaultKeyGenerator(url: string, params?: any): string {
    const paramsStr = params ? JSON.stringify(params) : ''
    return `${url}:${paramsStr}`
  }

  private isExpired(entry: CacheEntry): boolean {
    return Date.now() > entry.expires
  }

  private cleanup(): void {
    if (this.cache.size <= this.config.maxSize) return

    // 删除最旧的条目
    const entries = Array.from(this.cache.entries())
    entries.sort((a, b) => a[1].timestamp - b[1].timestamp)
    
    const toDelete = entries.slice(0, entries.length - this.config.maxSize)
    toDelete.forEach(([key]) => this.cache.delete(key))
  }

  get(url: string, params?: any): any | null {
    const key = this.config.keyGenerator(url, params)
    const entry = this.cache.get(key)

    if (!entry) return null
    if (this.isExpired(entry)) {
      this.cache.delete(key)
      return null
    }

    return entry.data
  }

  set(url: string, data: any, params?: any): void {
    const key = this.config.keyGenerator(url, params)
    const entry: CacheEntry = {
      data,
      timestamp: Date.now(),
      expires: Date.now() + this.config.maxAge
    }

    this.cache.set(key, entry)
    this.cleanup()
  }

  clear(): void {
    this.cache.clear()
  }

  delete(url: string, params?: any): void {
    const key = this.config.keyGenerator(url, params)
    this.cache.delete(key)
  }

  has(url: string, params?: any): boolean {
    return this.get(url, params) !== null
  }

  size(): number {
    return this.cache.size
  }

  // 获取缓存统计信息
  getStats(): {
    size: number
    maxSize: number
    hitRate: number
    missRate: number
    oldestEntry: number | null
    newestEntry: number | null
  } {
    const entries = Array.from(this.cache.values())
    const now = Date.now()
    
    const oldestEntry = entries.length > 0 
      ? Math.min(...entries.map(e => now - e.timestamp))
      : null
    
    const newestEntry = entries.length > 0
      ? Math.max(...entries.map(e => now - e.timestamp))
      : null

    return {
      size: this.cache.size,
      maxSize: this.config.maxSize,
      hitRate: 0, // 需要在外部统计
      missRate: 0,
      oldestEntry,
      newestEntry
    }
  }
}

// 创建默认实例
export const requestCache = new RequestCache()

export default RequestCache