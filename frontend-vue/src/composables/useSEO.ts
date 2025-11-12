import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'

interface SEOOptions {
  title?: string
  description?: string
  keywords?: string[]
  author?: string
  image?: string
  url?: string
  type?: 'website' | 'article' | 'video' | 'profile'
  siteName?: string
  locale?: string
  twitterCard?: 'summary' | 'summary_large_image' | 'app' | 'player'
  robots?: string
  canonical?: string
  structuredData?: Record<string, any>
}

interface AccessibilityOptions {
  skipLinks?: boolean
  focusManagement?: boolean
  keyboardNavigation?: boolean
  screenReaderSupport?: boolean
  highContrast?: boolean
  fontSize?: 'small' | 'medium' | 'large'
  reducedMotion?: boolean
}

export function useSEO(options: SEOOptions = {}) {
  const route = useRoute()
  const defaultOptions = {
    siteName: 'MediaCMS',
    locale: 'zh-CN',
    type: 'website' as const,
    twitterCard: 'summary_large_image' as const,
    robots: 'index,follow'
  }

  const mergedOptions = { ...defaultOptions, ...options }

  const updateMetaTags = () => {
    // 更新标题
    if (mergedOptions.title) {
      document.title = mergedOptions.title.includes(mergedOptions.siteName!) 
        ? mergedOptions.title 
        : `${mergedOptions.title} - ${mergedOptions.siteName}`
    }

    // 更新meta标签
    updateMetaTag('description', mergedOptions.description)
    updateMetaTag('keywords', mergedOptions.keywords?.join(', '))
    updateMetaTag('author', mergedOptions.author)
    updateMetaTag('robots', mergedOptions.robots)

    // Open Graph标签
    updateMetaTag('og:title', mergedOptions.title, 'property')
    updateMetaTag('og:description', mergedOptions.description, 'property')
    updateMetaTag('og:image', mergedOptions.image, 'property')
    updateMetaTag('og:url', mergedOptions.url || window.location.href, 'property')
    updateMetaTag('og:type', mergedOptions.type, 'property')
    updateMetaTag('og:site_name', mergedOptions.siteName, 'property')
    updateMetaTag('og:locale', mergedOptions.locale, 'property')

    // Twitter Card标签
    updateMetaTag('twitter:card', mergedOptions.twitterCard, 'name')
    updateMetaTag('twitter:title', mergedOptions.title, 'name')
    updateMetaTag('twitter:description', mergedOptions.description, 'name')
    updateMetaTag('twitter:image', mergedOptions.image, 'name')

    // Canonical URL
    if (mergedOptions.canonical) {
      updateLinkTag('canonical', mergedOptions.canonical)
    }

    // 结构化数据
    if (mergedOptions.structuredData) {
      updateStructuredData(mergedOptions.structuredData)
    }
  }

  const updateMetaTag = (name: string, content?: string, attribute: 'name' | 'property' = 'name') => {
    if (!content) return

    let meta = document.querySelector(`meta[${attribute}="${name}"]`)
    if (!meta) {
      meta = document.createElement('meta')
      meta.setAttribute(attribute, name)
      document.head.appendChild(meta)
    }
    meta.setAttribute('content', content)
  }

  const updateLinkTag = (rel: string, href: string) => {
    let link = document.querySelector(`link[rel="${rel}"]`)
    if (!link) {
      link = document.createElement('link')
      link.setAttribute('rel', rel)
      document.head.appendChild(link)
    }
    link.setAttribute('href', href)
  }

  const updateStructuredData = (data: Record<string, any>) => {
    let script = document.querySelector('script[type="application/ld+json"]')
    if (!script) {
      script = document.createElement('script')
      script.setAttribute('type', 'application/ld+json')
      document.head.appendChild(script)
    }
    script.textContent = JSON.stringify(data)
  }

  // 监听路由变化
  watch(() => route.path, () => {
    updateMetaTags()
  })

  onMounted(() => {
    updateMetaTags()
  })

  return {
    updateSEO: (newOptions: Partial<SEOOptions>) => {
      Object.assign(mergedOptions, newOptions)
      updateMetaTags()
    }
  }
}

export function useAccessibility(options: AccessibilityOptions = {}) {
  const accessibilityState = ref({
    skipLinks: options.skipLinks ?? true,
    focusManagement: options.focusManagement ?? true,
    keyboardNavigation: options.keyboardNavigation ?? true,
    screenReaderSupport: options.screenReaderSupport ?? true,
    highContrast: options.highContrast ?? false,
    fontSize: options.fontSize ?? 'medium',
    reducedMotion: options.reducedMotion ?? false
  })

  // 焦点管理
  const manageFocus = (element?: HTMLElement) => {
    if (!accessibilityState.value.focusManagement) return

    const target = element || document.body
    target.setAttribute('tabindex', '-1')
    target.focus()
    target.addEventListener('blur', () => {
      target.removeAttribute('tabindex')
    }, { once: true })
  }

  // 键盘导航
  const setupKeyboardNavigation = () => {
    if (!accessibilityState.value.keyboardNavigation) return

    document.addEventListener('keydown', (e) => {
      // Skip link functionality
      if (e.key === 'Tab' && accessibilityState.value.skipLinks) {
        const skipLink = document.querySelector('.skip-link') as HTMLElement
        if (skipLink && document.activeElement === document.body) {
          e.preventDefault()
          skipLink.focus()
        }
      }

      // Escape key to close modals/dropdowns
      if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.active, .el-dialog__wrapper')
        if (activeModal) {
          const closeButton = activeModal.querySelector('.close, .el-dialog__close') as HTMLElement
          if (closeButton) {
            closeButton.click()
          }
        }
      }
    })
  }

  // 屏幕阅读器支持
  const announceToScreenReader = (message: string, priority: 'polite' | 'assertive' = 'polite') => {
    if (!accessibilityState.value.screenReaderSupport) return

    const announcement = document.createElement('div')
    announcement.setAttribute('aria-live', priority)
    announcement.setAttribute('aria-atomic', 'true')
    announcement.className = 'sr-only'
    announcement.textContent = message
    document.body.appendChild(announcement)

    setTimeout(() => {
      document.body.removeChild(announcement)
    }, 1000)
  }

  // 高对比度模式
  const toggleHighContrast = (enabled: boolean) => {
    accessibilityState.value.highContrast = enabled
    document.documentElement.classList.toggle('high-contrast', enabled)
    localStorage.setItem('high-contrast', String(enabled))
  }

  // 字体大小调整
  const setFontSize = (size: 'small' | 'medium' | 'large') => {
    accessibilityState.value.fontSize = size
    document.documentElement.classList.remove('font-small', 'font-medium', 'font-large')
    document.documentElement.classList.add(`font-${size}`)
    localStorage.setItem('font-size', size)
  }

  // 减少动画
  const toggleReducedMotion = (enabled: boolean) => {
    accessibilityState.value.reducedMotion = enabled
    document.documentElement.classList.toggle('reduced-motion', enabled)
    localStorage.setItem('reduced-motion', String(enabled))
  }

  // 初始化可访问性设置
  const initializeAccessibility = () => {
    // 从localStorage恢复设置
    const savedHighContrast = localStorage.getItem('high-contrast') === 'true'
    const savedFontSize = localStorage.getItem('font-size') as 'small' | 'medium' | 'large' || 'medium'
    const savedReducedMotion = localStorage.getItem('reduced-motion') === 'true'

    if (savedHighContrast) toggleHighContrast(true)
    if (savedFontSize !== 'medium') setFontSize(savedFontSize)
    if (savedReducedMotion) toggleReducedMotion(true)

    // 设置键盘导航
    setupKeyboardNavigation()

    // 添加跳转到主内容的链接
    if (accessibilityState.value.skipLinks) {
      addSkipLink()
    }
  }

  // 添加跳转链接
  const addSkipLink = () => {
    const skipLink = document.createElement('a')
    skipLink.href = '#main-content'
    skipLink.className = 'skip-link'
    skipLink.textContent = '跳转到主内容'
    document.body.insertBefore(skipLink, document.body.firstChild)
  }

  // 图片可访问性
  const makeImageAccessible = (img: HTMLImageElement, description?: string) => {
    if (!img.alt) {
      img.alt = description || img.src.split('/').pop() || '图片'
    }
    img.setAttribute('role', 'img')
  }

  // 表单可访问性
  const makeFormAccessible = (form: HTMLFormElement) => {
    const inputs = form.querySelectorAll('input, textarea, select')
    inputs.forEach((input) => {
      const element = input as HTMLInputElement
      if (!element.id) {
        element.id = `input-${Math.random().toString(36).substr(2, 9)}`
      }
      
      // 确保有标签
      const label = form.querySelector(`label[for="${element.id}"]`)
      if (!label && element.placeholder) {
        const newLabel = document.createElement('label')
        newLabel.htmlFor = element.id
        newLabel.textContent = element.placeholder
        newLabel.className = 'sr-only'
        element.parentNode?.insertBefore(newLabel, element)
      }
    })
  }

  onMounted(() => {
    initializeAccessibility()
  })

  return {
    accessibilityState,
    manageFocus,
    announceToScreenReader,
    toggleHighContrast,
    setFontSize,
    toggleReducedMotion,
    makeImageAccessible,
    makeFormAccessible
  }
}

// 可访问性样式
export const accessibilityStyles = `
  /* 屏幕阅读器专用内容 */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  /* 跳过链接 */
  .skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    border-radius: 0 0 4px 4px;
    z-index: 1000;
    transition: top 0.3s;
  }

  .skip-link:focus {
    top: 0;
  }

  /* 高对比度模式 */
  .high-contrast {
    filter: contrast(1.5);
  }

  .high-contrast * {
    border-color: #000 !important;
  }

  /* 字体大小调整 */
  .font-small {
    font-size: 12px;
  }

  .font-medium {
    font-size: 16px;
  }

  .font-large {
    font-size: 20px;
  }

  /* 减少动画 */
  .reduced-motion *,
  .reduced-motion *::before,
  .reduced-motion *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  /* 焦点指示器 */
  *:focus {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }

  /* 键盘导航高亮 */
  .keyboard-focus {
    outline: 3px solid #0066cc !important;
    outline-offset: 2px !important;
  }
`