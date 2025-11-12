const CACHE_NAME = 'mediacms-v1'
const urlsToCache = [
  '/',
  '/offline.html',
  '/static/css/app.css',
  '/static/js/app.js'
]

// 安装事件 - 缓存资源
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache')
        return cache.addAll(urlsToCache)
      })
      .then(() => self.skipWaiting())
  )
})

// 激活事件 - 清理旧缓存
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName)
            return caches.delete(cacheName)
          }
        })
      )
    }).then(() => self.clients.claim())
  )
})

// 获取事件 - 缓存优先策略
self.addEventListener('fetch', event => {
  const { request } = event
  const url = new URL(request.url)

  // 跳过非GET请求
  if (request.method !== 'GET') {
    return
  }

  // 跳过API请求
  if (url.pathname.startsWith('/api/')) {
    return
  }

  // 跳过媒体文件（太大不适合缓存）
  if (url.pathname.match(/\.(mp4|webm|ogg|mp3|wav|flac|m4a)$/i)) {
    return
  }

  // 图片缓存策略 - 网络优先，缓存备用
  if (url.pathname.match(/\.(jpg|jpeg|png|gif|bmp|svg|webp)$/i)) {
    event.respondWith(
      fetch(request)
        .then(response => {
          // 检查响应是否有效
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response
          }

          // 克隆响应并缓存
          const responseToCache = response.clone()
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(request, responseToCache)
            })

          return response
        })
        .catch(() => {
          // 网络失败时返回缓存
          return caches.match(request)
        })
    )
    return
  }

  // 其他资源 - 缓存优先，网络备用
  event.respondWith(
    caches.match(request)
      .then(response => {
        if (response) {
          return response
        }

        return fetch(request).then(response => {
          // 检查响应是否有效
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response
          }

          // 克隆响应并缓存
          const responseToCache = response.clone()
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(request, responseToCache)
            })

          return response
        })
      })
      .catch(() => {
        // 缓存和网络都失败时返回离线页面
        if (request.destination === 'document') {
          return caches.match('/offline.html')
        }
      })
  )
})

// 后台同步 - 用于离线操作
self.addEventListener('sync', event => {
  if (event.tag === 'sync-comments') {
    event.waitUntil(syncComments())
  } else if (event.tag === 'sync-likes') {
    event.waitUntil(syncLikes())
  }
})

// 推送通知
self.addEventListener('push', event => {
  const options = {
    body: '您有新的媒体更新',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  }

  event.waitUntil(
    self.registration.showNotification('MediaCMS 更新', options)
  )
})

// 通知点击事件
self.addEventListener('notificationclick', event => {
  event.notification.close()
  event.waitUntil(
    clients.openWindow('/')
  )
})

// 同步评论（示例实现）
async function syncComments() {
  try {
    const cache = await caches.open(CACHE_NAME)
    const requests = await cache.keys()
    
    for (const request of requests) {
      if (request.url.includes('/api/comments') && request.method === 'POST') {
        const response = await fetch(request)
        if (response.ok) {
          await cache.delete(request)
        }
      }
    }
  } catch (error) {
    console.error('同步评论失败:', error)
  }
}

// 同步点赞（示例实现）
async function syncLikes() {
  try {
    const cache = await caches.open(CACHE_NAME)
    const requests = await cache.keys()
    
    for (const request of requests) {
      if (request.url.includes('/api/like') && request.method === 'POST') {
        const response = await fetch(request)
        if (response.ok) {
          await cache.delete(request)
        }
      }
    }
  } catch (error) {
    console.error('同步点赞失败:', error)
  }
}

// 消息处理
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
})