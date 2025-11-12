/**
 * 性能优化工具函数
 */

/**
 * 防抖函数
 * @param fn 要防抖的函数
 * @param delay 延迟时间（毫秒）
 * @returns 防抖后的函数
 */
export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null

  return function (this: any, ...args: Parameters<T>) {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }

    timeoutId = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * 节流函数
 * @param fn 要节流的函数
 * @param delay 延迟时间（毫秒）
 * @returns 节流后的函数
 */
export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let lastCall = 0

  return function (this: any, ...args: Parameters<T>) {
    const now = Date.now()

    if (now - lastCall >= delay) {
      lastCall = now
      fn.apply(this, args)
    }
  }
}

/**
 * 请求空闲回调
 * 使用 requestIdleCallback 或 setTimeout 作为降级方案
 * @param callback 回调函数
 * @param options 选项
 */
export function requestIdleCallback(
  callback: () => void,
  options?: { timeout?: number }
): number {
  if (typeof window.requestIdleCallback === 'function') {
    return window.requestIdleCallback(callback, options)
  }

  // 降级为 setTimeout
  return window.setTimeout(callback, options?.timeout || 1)
}

/**
 * 取消空闲回调
 * @param id 回调 ID
 */
export function cancelIdleCallback(id: number): void {
  if (typeof window.cancelIdleCallback === 'function') {
    window.cancelIdleCallback(id)
  } else {
    clearTimeout(id)
  }
}

/**
 * 图片预加载
 * @param urls 图片 URL 列表
 * @returns Promise，当所有图片加载完成时 resolve
 */
export function preloadImages(urls: string[]): Promise<void> {
  const promises = urls.map(url => {
    return new Promise<void>((resolve, reject) => {
      const img = new Image()
      img.onload = () => resolve()
      img.onerror = () => reject(new Error(`Failed to load image: ${url}`))
      img.src = url
    })
  })

  return Promise.all(promises).then(() => {})
}

/**
 * 懒加载观察器
 * 用于懒加载图片、组件等
 */
export class LazyLoader {
  private observer: IntersectionObserver
  private elements: Map<Element, () => void> = new Map()

  constructor(options?: IntersectionObserverInit) {
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const callback = this.elements.get(entry.target)
            if (callback) {
              callback()
              this.unobserve(entry.target)
            }
          }
        })
      },
      {
        rootMargin: '50px',
        ...options
      }
    )
  }

  /**
   * 观察元素
   * @param element 要观察的元素
   * @param callback 进入视口时的回调
   */
  observe(element: Element, callback: () => void): void {
    this.elements.set(element, callback)
    this.observer.observe(element)
  }

  /**
   * 停止观察元素
   * @param element 要停止观察的元素
   */
  unobserve(element: Element): void {
    this.elements.delete(element)
    this.observer.unobserve(element)
  }

  /**
   * 断开所有观察
   */
  disconnect(): void {
    this.observer.disconnect()
    this.elements.clear()
  }
}

/**
 * 内存优化：大数组分批处理
 * @param array 要处理的数组
 * @param batchSize 每批处理的数量
 * @param processor 处理函数
 * @returns Promise
 */
export async function processBatch<T>(
  array: T[],
  batchSize: number,
  processor: (batch: T[]) => Promise<void> | void
): Promise<void> {
  for (let i = 0; i < array.length; i += batchSize) {
    const batch = array.slice(i, i + batchSize)
    await processor(batch)
    
    // 让出控制权，避免阻塞主线程
    await new Promise(resolve => setTimeout(resolve, 0))
  }
}

/**
 * 格式化文件大小
 * @param bytes 字节数
 * @returns 格式化后的字符串
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

/**
 * 获取性能指标
 */
export function getPerformanceMetrics() {
  if (typeof window.performance === 'undefined') {
    return null
  }

  const perf = window.performance
  const timing = perf.timing

  return {
    // DNS 查询耗时
    dns: timing.domainLookupEnd - timing.domainLookupStart,
    // TCP 连接耗时
    tcp: timing.connectEnd - timing.connectStart,
    // 请求耗时
    request: timing.responseEnd - timing.requestStart,
    // 响应耗时
    response: timing.responseEnd - timing.responseStart,
    // DOM 解析耗时
    domParse: timing.domInteractive - timing.domLoading,
    // DOM 就绪耗时
    domReady: timing.domContentLoadedEventEnd - timing.navigationStart,
    // 页面加载耗时
    load: timing.loadEventEnd - timing.navigationStart,
    // 首次渲染时间
    firstPaint: perf.getEntriesByType('paint')[0]?.startTime || 0,
    // 首次内容绘制时间
    firstContentfulPaint: perf.getEntriesByType('paint')[1]?.startTime || 0
  }
}

