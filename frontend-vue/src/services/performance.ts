interface PerformanceMetrics {
  // 核心Web指标
  fcp?: number // First Contentful Paint
  lcp?: number // Largest Contentful Paint
  fid?: number // First Input Delay
  cls?: number // Cumulative Layout Shift
  ttfb?: number // Time to First Byte
  
  // 自定义指标
  pageLoadTime?: number
  domContentLoaded?: number
  resourceLoadTime?: number
  apiResponseTime?: Record<string, number>
  
  // 运行时指标
  memoryUsage?: number
  cpuUsage?: number
  fps?: number
}

interface PerformanceConfig {
  enableCoreWebVitals?: boolean
  enableResourceTiming?: boolean
  enableUserTiming?: boolean
  enableMemoryMonitoring?: boolean
  samplingRate?: number
  reportThreshold?: number
  onReport?: (metrics: PerformanceMetrics) => void
}

class PerformanceMonitor {
  private config: Required<PerformanceConfig>
  private metrics: PerformanceMetrics = {}
  private observer: PerformanceObserver | null = null
  private memoryMonitor: number | null = null
  private resourceTimings: PerformanceEntry[] = []
  private apiTimings: Record<string, number[]> = {}

  constructor(config: PerformanceConfig = {}) {
    this.config = {
      enableCoreWebVitals: config.enableCoreWebVitals ?? true,
      enableResourceTiming: config.enableResourceTiming ?? true,
      enableUserTiming: config.enableUserTiming ?? true,
      enableMemoryMonitoring: config.enableMemoryMonitoring ?? false,
      samplingRate: config.samplingRate ?? 1,
      reportThreshold: config.reportThreshold ?? 100,
      onReport: config.onReport ?? this.defaultReport
    }

    this.init()
  }

  private init(): void {
    if (this.config.enableCoreWebVitals) {
      this.initCoreWebVitals()
    }

    if (this.config.enableResourceTiming) {
      this.initResourceTiming()
    }

    if (this.config.enableUserTiming) {
      this.initUserTiming()
    }

    if (this.config.enableMemoryMonitoring) {
      this.initMemoryMonitoring()
    }

    // 监听页面生命周期
    this.initLifecycleListeners()
  }

  private initCoreWebVitals(): void {
    // First Contentful Paint
    this.observePaintTiming('first-contentful-paint', (entry) => {
      this.metrics.fcp = entry.startTime
      this.checkAndReport()
    })

    // Largest Contentful Paint
    this.observeLargestContentfulPaint((entry) => {
      this.metrics.lcp = entry.startTime
      this.checkAndReport()
    })

    // First Input Delay
    this.observeFirstInputDelay((entry: any) => {
      this.metrics.fid = entry.processingStart - entry.startTime
      this.checkAndReport()
    })

    // Cumulative Layout Shift
    let clsValue = 0
    this.observeLayoutShift((entry: any) => {
      if (!entry.hadRecentInput) {
        clsValue += entry.value
        this.metrics.cls = clsValue
        this.checkAndReport()
      }
    })

    // Time to First Byte
    this.observeNavigationTiming((entry: any) => {
      this.metrics.ttfb = entry.responseStart - entry.fetchStart
      this.checkAndReport()
    })
  }

  private initResourceTiming(): void {
    this.observer = new PerformanceObserver((list) => {
      const entries = list.getEntries()
      this.resourceTimings.push(...entries)
      
      // 计算资源加载时间
      const totalTime = entries.reduce((sum, entry) => {
        return sum + (entry.duration || 0)
      }, 0)
      
      this.metrics.resourceLoadTime = totalTime
      this.checkAndReport()
    })

    this.observer.observe({ entryTypes: ['resource'] })
  }

  private initUserTiming(): void {
    // 页面加载时间
    window.addEventListener('load', () => {
      this.metrics.pageLoadTime = performance.timing.loadEventEnd - performance.timing.navigationStart
      this.checkAndReport()
    })

    // DOM内容加载时间
    window.addEventListener('DOMContentLoaded', () => {
      this.metrics.domContentLoaded = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart
      this.checkAndReport()
    })
  }

  private initMemoryMonitoring(): void {
    if ('memory' in performance) {
      this.memoryMonitor = window.setInterval(() => {
        const memoryInfo = (performance as any).memory
        if (memoryInfo) {
          this.metrics.memoryUsage = memoryInfo.usedJSHeapSize
          this.checkAndReport()
        }
      }, 5000) // 每5秒检查一次
    }
  }

  private initLifecycleListeners(): void {
    // 页面可见性变化
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.pauseMonitoring()
      } else {
        this.resumeMonitoring()
      }
    })

    // 页面卸载前发送数据
    window.addEventListener('beforeunload', () => {
      this.sendFinalReport()
    })
  }

  private observePaintTiming(type: string, callback: (entry: PerformanceEntry) => void): void {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name === type) {
          callback(entry)
          observer.disconnect()
          break
        }
      }
    })
    observer.observe({ entryTypes: ['paint'] })
  }

  private observeLargestContentfulPaint(callback: (entry: PerformanceEntry) => void): void {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        callback(entry)
      }
    })
    observer.observe({ entryTypes: ['largest-contentful-paint'] })
  }

  private observeFirstInputDelay(callback: (entry: PerformanceEntry) => void): void {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        callback(entry)
        observer.disconnect()
        break
      }
    })
    observer.observe({ entryTypes: ['first-input'] })
  }

  private observeLayoutShift(callback: (entry: PerformanceEntry) => void): void {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        callback(entry)
      }
    })
    observer.observe({ entryTypes: ['layout-shift'] })
  }

  private observeNavigationTiming(callback: (entry: PerformanceEntry) => void): void {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if ((entry as any).type === 'navigate') {
          callback(entry)
          observer.disconnect()
          break
        }
      }
    })
    observer.observe({ entryTypes: ['navigation'] })
  }

  private checkAndReport(): void {
    // 采样率检查
    if (Math.random() > this.config.samplingRate) {
      return
    }

    // 阈值检查
    const hasSignificantMetrics = Object.values(this.metrics).some(value => 
      value !== undefined && value > this.config.reportThreshold
    )

    if (hasSignificantMetrics) {
      this.report()
    }
  }

  private report(): void {
    const reportData = {
      ...this.metrics,
      timestamp: Date.now(),
      url: window.location.href,
      userAgent: navigator.userAgent,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      }
    }

    this.config.onReport(reportData)
  }

  private sendFinalReport(): void {
    if (Object.keys(this.metrics).length > 0) {
      this.report()
    }
  }

  private defaultReport(metrics: PerformanceMetrics): void {
    // 发送到后端或第三方服务
    if (navigator.sendBeacon) {
      const data = JSON.stringify(metrics)
      navigator.sendBeacon('/api/performance', data)
    } else {
      // 降级方案
      fetch('/api/performance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(metrics),
        keepalive: true
      }).catch(console.error)
    }
  }

  // 手动记录API响应时间
  recordApiTiming(apiName: string, duration: number): void {
    if (!this.apiTimings[apiName]) {
      this.apiTimings[apiName] = []
    }
    this.apiTimings[apiName].push(duration)

    // 计算平均响应时间
    const timings = this.apiTimings[apiName]
    const avgTime = timings.reduce((sum, time) => sum + time, 0) / timings.length
    
    if (!this.metrics.apiResponseTime) {
      this.metrics.apiResponseTime = {}
    }
    this.metrics.apiResponseTime[apiName] = avgTime
    
    this.checkAndReport()
  }

  // 获取当前指标
  getMetrics(): PerformanceMetrics {
    return { ...this.metrics }
  }

  // 获取资源加载统计
  getResourceStats(): {
    totalResources: number
    slowResources: number
    averageLoadTime: number
    resourceTypes: Record<string, { count: number; avgTime: number }>
  } {
    const slowThreshold = 1000 // 1秒
    const slowResources = this.resourceTimings.filter(entry => entry.duration > slowThreshold)
    const totalTime = this.resourceTimings.reduce((sum, entry) => sum + entry.duration, 0)
    
    const resourceTypes: Record<string, { count: number; avgTime: number }> = {}
    this.resourceTimings.forEach(entry => {
      const type = entry.initiatorType || 'other'
      if (!resourceTypes[type]) {
        resourceTypes[type] = { count: 0, avgTime: 0 }
      }
      resourceTypes[type].count++
      resourceTypes[type].avgTime = (resourceTypes[type].avgTime * (resourceTypes[type].count - 1) + entry.duration) / resourceTypes[type].count
    })

    return {
      totalResources: this.resourceTimings.length,
      slowResources: slowResources.length,
      averageLoadTime: this.resourceTimings.length > 0 ? totalTime / this.resourceTimings.length : 0,
      resourceTypes
    }
  }

  // 暂停监控
  pauseMonitoring(): void {
    if (this.observer) {
      this.observer.disconnect()
    }
    if (this.memoryMonitor) {
      clearInterval(this.memoryMonitor)
    }
  }

  // 恢复监控
  resumeMonitoring(): void {
    this.init()
  }

  // 清理资源
  destroy(): void {
    this.pauseMonitoring()
    this.metrics = {}
    this.resourceTimings = []
    this.apiTimings = {}
  }
}

// 创建全局性能监控实例
export const performanceMonitor = new PerformanceMonitor({
  enableCoreWebVitals: true,
  enableResourceTiming: true,
  enableUserTiming: true,
  enableMemoryMonitoring: true,
  samplingRate: 1,
  reportThreshold: 100,
  onReport: (metrics) => {
    console.log('Performance metrics:', metrics)
    // 这里可以发送到后端或第三方监控服务
  }
})

export default PerformanceMonitor