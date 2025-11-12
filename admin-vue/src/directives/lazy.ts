/**
 * 图片懒加载指令
 * 
 * 使用方法：
 * <img v-lazy="imageUrl" />
 */

import type { Directive, DirectiveBinding } from 'vue'

interface LazyImageElement extends HTMLImageElement {
  __lazy_observer__?: IntersectionObserver
}

const loadingImage = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect width="100" height="100" fill="%23f5f5f5"/%3E%3C/svg%3E'
const errorImage = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect width="100" height="100" fill="%23ffebee"/%3E%3Ctext x="50" y="50" text-anchor="middle" font-size="14" fill="%23f44336"%3E加载失败%3C/text%3E%3C/svg%3E'

const lazyLoadImage = (el: LazyImageElement, binding: DirectiveBinding) => {
  const imageUrl = binding.value
  
  if (!imageUrl) return

  // 设置加载中的占位图
  el.src = loadingImage

  // 创建 IntersectionObserver
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target as LazyImageElement
          const tempImg = new Image()

          tempImg.onload = () => {
            img.src = imageUrl
            img.removeAttribute('data-lazy-loading')
            observer.unobserve(img)
          }

          tempImg.onerror = () => {
            img.src = errorImage
            img.removeAttribute('data-lazy-loading')
            observer.unobserve(img)
          }

          tempImg.src = imageUrl
        }
      })
    },
    {
      rootMargin: '100px',
      threshold: 0.01
    }
  )

  el.__lazy_observer__ = observer
  el.setAttribute('data-lazy-loading', 'true')
  observer.observe(el)
}

export const vLazy: Directive = {
  mounted(el: LazyImageElement, binding: DirectiveBinding) {
    lazyLoadImage(el, binding)
  },

  updated(el: LazyImageElement, binding: DirectiveBinding) {
    if (binding.value !== binding.oldValue) {
      // 先清理旧的 observer
      if (el.__lazy_observer__) {
        el.__lazy_observer__.unobserve(el)
        el.__lazy_observer__.disconnect()
      }
      
      // 重新加载
      lazyLoadImage(el, binding)
    }
  },

  unmounted(el: LazyImageElement) {
    if (el.__lazy_observer__) {
      el.__lazy_observer__.disconnect()
      delete el.__lazy_observer__
    }
  }
}

