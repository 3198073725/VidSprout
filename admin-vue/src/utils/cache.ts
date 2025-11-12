/**
 * API 缓存管理器
 * 用于缓存 API 响应，减少不必要的网络请求
 */

interface CacheItem {
  data: any
  expireTime: number
}

class CacheManager {
  private cache: Map<string, CacheItem> = new Map()
  private defaultTTL = 5 * 60 * 1000 // 默认缓存 5 分钟

  /**
   * 设置缓存
   * @param key 缓存键
   * @param data 缓存数据
   * @param ttl 过期时间（毫秒），默认 5 分钟
   */
  set(key: string, data: any, ttl?: number): void {
    const expireTime = Date.now() + (ttl || this.defaultTTL)
    this.cache.set(key, { data, expireTime })
  }

  /**
   * 获取缓存
   * @param key 缓存键
   * @returns 缓存数据，如果不存在或已过期则返回 null
   */
  get(key: string): any {
    const item = this.cache.get(key)
    
    if (!item) {
      return null
    }

    // 检查是否过期
    if (Date.now() > item.expireTime) {
      this.cache.delete(key)
      return null
    }

    return item.data
  }

  /**
   * 删除缓存
   * @param key 缓存键
   */
  delete(key: string): void {
    this.cache.delete(key)
  }

  /**
   * 清空所有缓存
   */
  clear(): void {
    this.cache.clear()
  }

  /**
   * 清空过期缓存
   */
  clearExpired(): void {
    const now = Date.now()
    for (const [key, item] of this.cache.entries()) {
      if (now > item.expireTime) {
        this.cache.delete(key)
      }
    }
  }

  /**
   * 包装 API 请求，自动处理缓存
   * @param key 缓存键
   * @param fetcher API 请求函数
   * @param ttl 缓存时间（毫秒）
   * @param forceRefresh 是否强制刷新
   */
  async wrap<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl?: number,
    forceRefresh = false
  ): Promise<T> {
    // 如果不强制刷新，先尝试从缓存获取
    if (!forceRefresh) {
      const cached = this.get(key)
      if (cached !== null) {
        return cached as T
      }
    }

    // 执行请求
    const data = await fetcher()

    // 缓存结果
    this.set(key, data, ttl)

    return data
  }
}

// 导出单例
export const cacheManager = new CacheManager()

// 定期清理过期缓存（每 10 分钟）
setInterval(() => {
  cacheManager.clearExpired()
}, 10 * 60 * 1000)

