/**
 * 移动端工具函数
 * 处理移动端特殊情况和优化
 */

// 检测设备类型
export const isMobile = (): boolean => {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
}

export const isIOS = (): boolean => {
  return /iPad|iPhone|iPod/.test(navigator.userAgent)
}

export const isAndroid = (): boolean => {
  return /Android/.test(navigator.userAgent)
}

export const isTouchDevice = (): boolean => {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0
}

// 获取屏幕尺寸分类
export const getScreenSize = (): 'xs' | 'sm' | 'md' | 'lg' | 'xl' => {
  const width = window.innerWidth
  if (width < 480) return 'xs'
  if (width < 768) return 'sm'
  if (width < 1024) return 'md'
  if (width < 1200) return 'lg'
  return 'xl'
}

// 处理 iOS Safari 地址栏高度变化
export const handleIOSViewportHeight = (): void => {
  if (!isIOS()) return

  const setVH = () => {
    const vh = window.innerHeight * 0.01
    document.documentElement.style.setProperty('--vh', `${vh}px`)
  }

  setVH()
  window.addEventListener('resize', setVH)
  window.addEventListener('orientationchange', () => {
    setTimeout(setVH, 100)
  })
}

// 防止 iOS 缩放
export const preventIOSZoom = (): void => {
  if (!isIOS()) return

  document.addEventListener('touchstart', (event) => {
    if (event.touches.length > 1) {
      event.preventDefault()
    }
  })

  let lastTouchEnd = 0
  document.addEventListener('touchend', (event) => {
    const now = new Date().getTime()
    if (now - lastTouchEnd <= 300) {
      event.preventDefault()
    }
    lastTouchEnd = now
  }, false)
}

// 优化滚动性能
export const optimizeScrolling = (): void => {
  // 添加 passive 事件监听器
  const addPassiveEventListener = (element: Element, event: string, handler: EventListener) => {
    element.addEventListener(event, handler, { passive: true })
  }

  // 为所有滚动容器添加优化
  const scrollContainers = document.querySelectorAll('.scrollable-container, .items-grid')
  scrollContainers.forEach(container => {
    addPassiveEventListener(container, 'touchstart', () => {})
    addPassiveEventListener(container, 'touchmove', () => {})
  })
}

// 处理移动端键盘弹出
export const handleMobileKeyboard = (): void => {
  if (!isMobile()) return

  const viewport = document.querySelector('meta[name=viewport]') as HTMLMetaElement
  if (!viewport) return

  const originalContent = viewport.content

  // 监听输入框焦点
  document.addEventListener('focusin', (event) => {
    const target = event.target as HTMLElement
    if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
      // 键盘弹出时调整视口
      viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'
      
      // 滚动到输入框
      setTimeout(() => {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }, 300)
    }
  })

  document.addEventListener('focusout', () => {
    // 键盘收起时恢复视口
    setTimeout(() => {
      viewport.content = originalContent
    }, 100)
  })
}

// 优化图片加载
export const optimizeImageLoading = (): void => {
  // 使用 Intersection Observer 实现懒加载
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement
          if (img.dataset.src) {
            img.src = img.dataset.src
            img.removeAttribute('data-src')
            imageObserver.unobserve(img)
          }
        }
      })
    }, {
      rootMargin: '50px 0px',
      threshold: 0.01
    })

    // 观察所有带有 data-src 的图片
    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img)
    })
  }
}

// 添加触摸反馈
export const addTouchFeedback = (): void => {
  if (!isTouchDevice()) return

  const addTouchClass = (element: Element) => {
    element.addEventListener('touchstart', () => {
      element.classList.add('touching')
    }, { passive: true })

    element.addEventListener('touchend', () => {
      setTimeout(() => {
        element.classList.remove('touching')
      }, 150)
    }, { passive: true })

    element.addEventListener('touchcancel', () => {
      element.classList.remove('touching')
    }, { passive: true })
  }

  // 为可点击元素添加触摸反馈
  const clickableElements = document.querySelectorAll('.item-thumb, .el-button, .el-menu-item')
  clickableElements.forEach(addTouchClass)
}

// 处理网络状态
export const handleNetworkStatus = (): void => {
  if (!('navigator' in window) || !('onLine' in navigator)) return

  const updateNetworkStatus = () => {
    const isOnline = navigator.onLine
    document.body.classList.toggle('offline', !isOnline)
    
    // 触发自定义事件
    window.dispatchEvent(new CustomEvent('networkchange', {
      detail: { online: isOnline }
    }))
  }

  window.addEventListener('online', updateNetworkStatus)
  window.addEventListener('offline', updateNetworkStatus)
  updateNetworkStatus()
}

// 优化视频播放
export const optimizeVideoPlayback = (): void => {
  const videos = document.querySelectorAll('video')
  
  videos.forEach(video => {
    // 设置移动端播放属性
    video.setAttribute('playsinline', 'true')
    video.setAttribute('webkit-playsinline', 'true')
    
    // 预加载优化
    if (isMobile()) {
      video.preload = 'metadata'
    }
    
    // 自动暂停不可见视频
    if ('IntersectionObserver' in window) {
      const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const video = entry.target as HTMLVideoElement
          if (!entry.isIntersecting && !video.paused) {
            video.pause()
          }
        })
      }, { threshold: 0.5 })
      
      videoObserver.observe(video)
    }
  })
}

// 性能监控
export const monitorPerformance = (): void => {
  if (!('performance' in window)) return

  // 监控 FPS
  let fps = 0
  let lastTime = performance.now()
  
  const measureFPS = (currentTime: number) => {
    fps = Math.round(1000 / (currentTime - lastTime))
    lastTime = currentTime
    
    // 如果 FPS 过低，添加性能警告类
    if (fps < 30) {
      document.body.classList.add('low-performance')
    } else {
      document.body.classList.remove('low-performance')
    }
    
    requestAnimationFrame(measureFPS)
  }
  
  requestAnimationFrame(measureFPS)
}

// 初始化所有移动端优化
export const initMobileOptimizations = (): void => {
  // 基础检测
  document.body.classList.toggle('is-mobile', isMobile())
  document.body.classList.toggle('is-ios', isIOS())
  document.body.classList.toggle('is-android', isAndroid())
  document.body.classList.toggle('is-touch', isTouchDevice())
  document.body.classList.add(`screen-${getScreenSize()}`)

  // 应用优化
  handleIOSViewportHeight()
  preventIOSZoom()
  optimizeScrolling()
  handleMobileKeyboard()
  optimizeImageLoading()
  addTouchFeedback()
  handleNetworkStatus()
  optimizeVideoPlayback()
  monitorPerformance()

  // 监听屏幕尺寸变化
  window.addEventListener('resize', () => {
    // 移除旧的屏幕尺寸类
    document.body.classList.remove('screen-xs', 'screen-sm', 'screen-md', 'screen-lg', 'screen-xl')
    // 添加新的屏幕尺寸类
    document.body.classList.add(`screen-${getScreenSize()}`)
  })

  console.log('📱 移动端优化已初始化')
}

// 工具函数：节流
export const throttle = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJSTimeout | null = null
  let lastExecTime = 0
  
  return (...args: Parameters<T>) => {
    const currentTime = Date.now()
    
    if (currentTime - lastExecTime > delay) {
      func(...args)
      lastExecTime = currentTime
    } else {
      if (timeoutId) clearTimeout(timeoutId)
      timeoutId = setTimeout(() => {
        func(...args)
        lastExecTime = Date.now()
      }, delay - (currentTime - lastExecTime))
    }
  }
}

// 工具函数：防抖
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJSTimeout | null = null
  
  return (...args: Parameters<T>) => {
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func(...args), delay)
  }
}
