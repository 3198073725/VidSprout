/**
 * 缓存管理器单元测试
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { cacheManager } from '@/utils/cache'

describe('CacheManager', () => {
  beforeEach(() => {
    // 每个测试前清空缓存
    cacheManager.clear()
  })

  it('应该能够设置和获取缓存', () => {
    const key = 'test-key'
    const data = { foo: 'bar' }

    cacheManager.set(key, data)
    const cached = cacheManager.get(key)

    expect(cached).toEqual(data)
  })

  it('缓存过期后应该返回 null', async () => {
    const key = 'test-key'
    const data = { foo: 'bar' }

    // 设置 100ms 过期
    cacheManager.set(key, data, 100)

    // 立即获取应该有值
    expect(cacheManager.get(key)).toEqual(data)

    // 等待 150ms 后应该过期
    await new Promise(resolve => setTimeout(resolve, 150))
    expect(cacheManager.get(key)).toBeNull()
  })

  it('应该能够删除指定缓存', () => {
    const key = 'test-key'
    const data = { foo: 'bar' }

    cacheManager.set(key, data)
    expect(cacheManager.get(key)).toEqual(data)

    cacheManager.delete(key)
    expect(cacheManager.get(key)).toBeNull()
  })

  it('应该能够清空所有缓存', () => {
    cacheManager.set('key1', 'value1')
    cacheManager.set('key2', 'value2')

    expect(cacheManager.get('key1')).toBe('value1')
    expect(cacheManager.get('key2')).toBe('value2')

    cacheManager.clear()

    expect(cacheManager.get('key1')).toBeNull()
    expect(cacheManager.get('key2')).toBeNull()
  })

  it('wrap 方法应该能够缓存函数结果', async () => {
    const key = 'test-wrap'
    const mockFetcher = vi.fn().mockResolvedValue({ data: 'test' })

    // 第一次调用
    const result1 = await cacheManager.wrap(key, mockFetcher)
    expect(result1).toEqual({ data: 'test' })
    expect(mockFetcher).toHaveBeenCalledTimes(1)

    // 第二次调用应该使用缓存
    const result2 = await cacheManager.wrap(key, mockFetcher)
    expect(result2).toEqual({ data: 'test' })
    expect(mockFetcher).toHaveBeenCalledTimes(1) // 仍然是 1 次

    // 强制刷新
    const result3 = await cacheManager.wrap(key, mockFetcher, undefined, true)
    expect(result3).toEqual({ data: 'test' })
    expect(mockFetcher).toHaveBeenCalledTimes(2) // 增加到 2 次
  })

  it('clearExpired 应该只清除过期的缓存', async () => {
    // 设置一个长期缓存和一个短期缓存
    cacheManager.set('long', 'value1', 5000)
    cacheManager.set('short', 'value2', 100)

    // 等待短期缓存过期
    await new Promise(resolve => setTimeout(resolve, 150))

    cacheManager.clearExpired()

    // 长期缓存应该还在
    expect(cacheManager.get('long')).toBe('value1')
    // 短期缓存应该被清除
    expect(cacheManager.get('short')).toBeNull()
  })
})

