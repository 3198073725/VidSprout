/**
 * 防抖函数
 * @param func 要执行的函数
 * @param wait 等待时间（毫秒）
 * @param immediate 是否立即执行
 * @returns 防抖后的函数
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number,
  immediate: boolean = false
): T & { cancel: () => void } {
  let timeout: ReturnType<typeof setTimeout> | null = null

  const debounced = function (this: any, ...args: Parameters<T>) {
    const later = () => {
      timeout = null
      if (!immediate) func.apply(this, args)
    }

    const callNow = immediate && !timeout

    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(later, wait)

    if (callNow) func.apply(this, args)
  } as T & { cancel: () => void }

  debounced.cancel = () => {
    if (timeout) {
      clearTimeout(timeout)
      timeout = null
    }
  }

  return debounced
}

/**
 * 节流函数
 * @param func 要执行的函数
 * @param wait 等待时间（毫秒）
 * @param options 选项
 * @returns 节流后的函数
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  wait: number,
  options: {
    leading?: boolean
    trailing?: boolean
  } = {}
): T & { cancel: () => void } {
  let timeout: ReturnType<typeof setTimeout> | null = null
  let previous = 0

  const { leading = true, trailing = true } = options

  const throttled = function (this: any, ...args: Parameters<T>) {
    const now = Date.now()
    if (!previous && !leading) previous = now

    const remaining = wait - (now - previous)

    if (remaining <= 0 || remaining > wait) {
      if (timeout) {
        clearTimeout(timeout)
        timeout = null
      }
      previous = now
      func.apply(this, args)
    } else if (!timeout && trailing) {
      timeout = setTimeout(() => {
        previous = leading ? now : 0
        timeout = null
        func.apply(this, args)
      }, remaining)
    }
  } as T & { cancel: () => void }

  throttled.cancel = () => {
    if (timeout) {
      clearTimeout(timeout)
      timeout = null
    }
    previous = 0
  }

  return throttled
}

/**
 * 请求防抖装饰器
 * @param wait 防抖时间
 * @returns 装饰器函数
 */
export function debounceRequest(wait: number = 300) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value
    const debouncedMethod = debounce(originalMethod, wait)

    descriptor.value = function (...args: any[]) {
      return debouncedMethod.apply(this, args)
    }

    return descriptor
  }
}

/**
 * 请求节流装饰器
 * @param wait 节流时间
 * @returns 装饰器函数
 */
export function throttleRequest(wait: number = 1000) {
  return function (target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value
    const throttledMethod = throttle(originalMethod, wait)

    descriptor.value = function (...args: any[]) {
      return throttledMethod.apply(this, args)
    }

    return descriptor
  }
}

/**
 * 组合防抖函数（用于多个相关函数）
 */
export function createDebouncedGroup<T extends Record<string, (...args: any[]) => any>>(
  functions: T,
  wait: number,
  immediate: boolean = false
): T {
  const debouncedFunctions = {} as T
  let sharedTimeout: ReturnType<typeof setTimeout> | null = null
  let pendingCalls: Array<{ func: Function; args: any[]; thisArg: any }> = []

  const executePending = () => {
    pendingCalls.forEach(({ func, args, thisArg }) => {
      func.apply(thisArg, args)
    })
    pendingCalls = []
  }

  Object.keys(functions).forEach(key => {
    debouncedFunctions[key as keyof T] = function (this: any, ...args: any[]) {
      if (sharedTimeout) {
        clearTimeout(sharedTimeout)
      }

      if (immediate && pendingCalls.length === 0) {
        const func = functions[key as keyof T]
        if (func) {
          func.apply(this, args)
        }
      } else {
        const func = functions[key as keyof T]
        if (func) {
          pendingCalls.push({ func, args, thisArg: this })
        }
      }

      sharedTimeout = setTimeout(() => {
        if (!immediate) {
          executePending()
        }
        sharedTimeout = null
        pendingCalls = []
      }, wait)
    } as T[keyof T]
  })

  return debouncedFunctions
}