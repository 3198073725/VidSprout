/**
 * 性能工具函数单元测试
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { debounce, throttle, formatFileSize, processBatch } from '@/utils/performance'

describe('Performance Utils', () => {
  describe('debounce', () => {
    beforeEach(() => {
      vi.useFakeTimers()
    })

    it('应该延迟执行函数', () => {
      const fn = vi.fn()
      const debouncedFn = debounce(fn, 100)

      debouncedFn()
      expect(fn).not.toHaveBeenCalled()

      vi.advanceTimersByTime(100)
      expect(fn).toHaveBeenCalledTimes(1)
    })

    it('连续调用应该重置计时器', () => {
      const fn = vi.fn()
      const debouncedFn = debounce(fn, 100)

      debouncedFn()
      vi.advanceTimersByTime(50)
      debouncedFn()
      vi.advanceTimersByTime(50)

      // 此时还不应该执行
      expect(fn).not.toHaveBeenCalled()

      vi.advanceTimersByTime(50)
      expect(fn).toHaveBeenCalledTimes(1)
    })
  })

  describe('throttle', () => {
    beforeEach(() => {
      vi.useFakeTimers()
    })

    it('应该在指定时间内只执行一次', () => {
      const fn = vi.fn()
      const throttledFn = throttle(fn, 100)

      throttledFn()
      expect(fn).toHaveBeenCalledTimes(1)

      throttledFn()
      throttledFn()
      expect(fn).toHaveBeenCalledTimes(1)

      vi.advanceTimersByTime(100)
      throttledFn()
      expect(fn).toHaveBeenCalledTimes(2)
    })
  })

  describe('formatFileSize', () => {
    it('应该正确格式化字节数', () => {
      expect(formatFileSize(0)).toBe('0 B')
      expect(formatFileSize(1024)).toBe('1 KB')
      expect(formatFileSize(1024 * 1024)).toBe('1 MB')
      expect(formatFileSize(1024 * 1024 * 1024)).toBe('1 GB')
      expect(formatFileSize(1536)).toBe('1.5 KB')
    })
  })

  describe('processBatch', () => {
    it('应该按批次处理数组', async () => {
      const array = Array.from({ length: 10 }, (_, i) => i)
      const processor = vi.fn()

      await processBatch(array, 3, processor)

      // 应该调用 4 次（10 / 3 = 3...1）
      expect(processor).toHaveBeenCalledTimes(4)

      // 检查每批的大小
      expect(processor.mock.calls[0][0]).toHaveLength(3)
      expect(processor.mock.calls[1][0]).toHaveLength(3)
      expect(processor.mock.calls[2][0]).toHaveLength(3)
      expect(processor.mock.calls[3][0]).toHaveLength(1)
    })
  })
})

