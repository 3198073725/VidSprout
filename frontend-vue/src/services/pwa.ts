interface PWAServiceConfig {
  onUpdate?: (registration: ServiceWorkerRegistration) => void
  onSuccess?: (registration: ServiceWorkerRegistration) => void
  onError?: (error: Error) => void
}

class PWAService {
  private config: PWAServiceConfig
  private registration: ServiceWorkerRegistration | null = null
  private isUpdateAvailable = false

  constructor(config: PWAServiceConfig = {}) {
    this.config = config
  }

  // 注册Service Worker
  async register(): Promise<void> {
    if (!('serviceWorker' in navigator)) {
      console.warn('Service Worker not supported')
      return
    }

    if (!('caches' in window)) {
      console.warn('Cache API not supported')
      return
    }

    try {
      const registration = await navigator.serviceWorker.register('/sw.js')
      this.registration = registration

      console.log('Service Worker registered successfully')

      // 监听更新
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              this.isUpdateAvailable = true
              this.config.onUpdate?.(registration)
            }
          })
        }
      })

      // 监听控制器变化
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        window.location.reload()
      })

      this.config.onSuccess?.(registration)
    } catch (error) {
      console.error('Service Worker registration failed:', error)
      this.config.onError?.(error as Error)
    }
  }

  // 检查更新
  async checkForUpdates(): Promise<void> {
    if (!this.registration) {
      console.warn('Service Worker not registered')
      return
    }

    try {
      await this.registration.update()
    } catch (error) {
      console.error('Failed to check for updates:', error)
    }
  }

  // 激活更新
  async activateUpdate(): Promise<void> {
    if (!this.registration || !this.registration.waiting) {
      console.warn('No update available')
      return
    }

    try {
      this.registration.waiting.postMessage({ type: 'SKIP_WAITING' })
    } catch (error) {
      console.error('Failed to activate update:', error)
    }
  }

  // 获取缓存状态
  async getCacheStatus(): Promise<{
    cacheNames: string[]
    cacheSizes: Record<string, number>
    totalSize: number
  }> {
    if (!('caches' in window)) {
      throw new Error('Cache API not supported')
    }

    const cacheNames = await caches.keys()
    const cacheSizes: Record<string, number> = {}
    let totalSize = 0

    for (const cacheName of cacheNames) {
      const cache = await caches.open(cacheName)
      const requests = await cache.keys()
      const size = requests.length
      cacheSizes[cacheName] = size
      totalSize += size
    }

    return {
      cacheNames,
      cacheSizes,
      totalSize
    }
  }

  // 清除缓存
  async clearCache(): Promise<void> {
    if (!('caches' in window)) {
      throw new Error('Cache API not supported')
    }

    const cacheNames = await caches.keys()
    await Promise.all(cacheNames.map(cacheName => caches.delete(cacheName)))
  }

  // 获取网络状态
  getNetworkStatus(): {
    online: boolean
    effectiveType?: string
    downlink?: number
    rtt?: number
  } {
    const connection = (navigator as any).connection || (navigator as any).mozConnection || (navigator as any).webkitConnection
    
    return {
      online: navigator.onLine,
      effectiveType: connection?.effectiveType,
      downlink: connection?.downlink,
      rtt: connection?.rtt
    }
  }

  // 监听网络状态变化
  addNetworkListener(callback: (online: boolean) => void): () => void {
    const onlineHandler = () => callback(true)
    const offlineHandler = () => callback(false)

    window.addEventListener('online', onlineHandler)
    window.addEventListener('offline', offlineHandler)

    // 返回取消监听的函数
    return () => {
      window.removeEventListener('online', onlineHandler)
      window.removeEventListener('offline', offlineHandler)
    }
  }

  // 发送后台同步事件
  async triggerBackgroundSync(tag: string): Promise<void> {
    if (!('sync' in self.registration)) {
      console.warn('Background Sync not supported')
      return
    }

    try {
      await this.registration?.sync.register(tag)
    } catch (error) {
      console.error('Failed to trigger background sync:', error)
    }
  }

  // 请求通知权限
  async requestNotificationPermission(): Promise<NotificationPermission> {
    if (!('Notification' in window)) {
      throw new Error('Notifications not supported')
    }

    return await Notification.requestPermission()
  }

  // 显示通知
  async showNotification(title: string, options?: NotificationOptions): Promise<void> {
    if (!('Notification' in window)) {
      throw new Error('Notifications not supported')
    }

    if (this.registration && Notification.permission !== 'granted') {
      throw new Error('Notification permission not granted')
    }

    await this.registration?.showNotification(title, options)
  }

  // 获取更新状态
  getUpdateStatus(): {
    isUpdateAvailable: boolean
    hasServiceWorker: boolean
    isControllerLoaded: boolean
  } {
    return {
      isUpdateAvailable: this.isUpdateAvailable,
      hasServiceWorker: 'serviceWorker' in navigator,
      isControllerLoaded: !!navigator.serviceWorker.controller
    }
  }

  // 注销Service Worker
  async unregister(): Promise<boolean> {
    if (!this.registration) {
      return false
    }

    try {
      const result = await this.registration.unregister()
      this.registration = null
      this.isUpdateAvailable = false
      return result
    } catch (error) {
      console.error('Failed to unregister Service Worker:', error)
      return false
    }
  }
}

// 创建PWA服务实例
export const pwaService = new PWAService({
  onUpdate: (registration) => {
    console.log('New update available')
    // 可以在这里显示更新提示
    if (window.confirm('有新版本可用，是否立即更新？')) {
      pwaService.activateUpdate()
    }
  },
  onSuccess: (registration) => {
    console.log('PWA service registered successfully')
  },
  onError: (error) => {
    console.error('PWA service registration failed:', error)
  }
})

export default PWAService