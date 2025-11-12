import axios from 'axios'
import type { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios'

// Base URL from Vite env
const baseURL = import.meta.env.VITE_API_BASE || '/api'
const useCSRF = (import.meta.env.VITE_USE_CSRF || 'false') === 'true'
const CSRF_COOKIE = import.meta.env.VITE_CSRF_COOKIE || 'csrftoken'
const CSRF_HEADER = import.meta.env.VITE_CSRF_HEADER || 'X-CSRFToken'
const REFRESH_ENDPOINT = import.meta.env.VITE_REFRESH_ENDPOINT || '/api/auth/refresh'
const ACCESS_HEADER = import.meta.env.VITE_ACCESS_HEADER || 'Authorization'
const ACCESS_PREFIX = import.meta.env.VITE_ACCESS_PREFIX || 'Token'  // MediaCMS 使用 Token 而不是 Bearer

function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop()!.split(';').shift() || null
  return null
}

// Create axios instance
const http: AxiosInstance = axios.create({
  baseURL,
  // send cookies if your backend needs session/CSRF
  withCredentials: useCSRF,
  timeout: 15000,
})

// Request interceptor: attach auth token if exists
http.interceptors.request.use(
  (config: InternalAxiosRequestConfig & { _isRetry?: boolean }) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.set(ACCESS_HEADER, `${ACCESS_PREFIX} ${token}`)
    }

    // CSRF header from cookie when enabled
    if (useCSRF) {
      const csrf = getCookie(CSRF_COOKIE)
      if (csrf) {
        config.headers.set(CSRF_HEADER, csrf)
      }
    }

    return config
  },
  (error: AxiosError) => Promise.reject(error)
)

// Response interceptor: handle common errors and unwrap data
let isRefreshing = false
let pendingQueue: Array<{ resolve: (token: string) => void; reject: (err: any) => void }> = []

function processQueue(error: any, token: string | null) {
  pendingQueue.forEach(({ resolve, reject }) => {
    if (token) resolve(token)
    else reject(error)
  })
  pendingQueue = []
}

http.interceptors.response.use(
  (response: AxiosResponse) => {
    return response.data
  },
  async (error: AxiosError<any>) => {
    const status = error.response?.status
    const errorData = error.response?.data
    const originalRequest = (error.config || {}) as InternalAxiosRequestConfig & { _isRetry?: boolean }

    // 检查用户是否被封禁
    if (status === 403 || status === 401) {
      const errorMessage = errorData?.detail || errorData?.message || ''
      const errorArray = errorData?.non_field_errors || []
      const errorCode = errorData?.code || ''
      const blockedFlag = errorData?.blocked
      
      // 检查是否包含封禁相关的错误消息
      const isBlocked = 
        blockedFlag === true ||  // 直接检查 blocked 标志
        errorCode === 'user_blocked' ||  // 检查错误代码
        errorMessage.includes('封禁') || 
        errorMessage.includes('deactivated') ||
        errorMessage.includes('账号已被禁用') ||
        errorMessage.includes('已被封禁') ||
        errorArray.some((msg: string) => 
          msg.includes('封禁') || 
          msg.includes('deactivated') ||
          msg.includes('已被封禁')
        )
      
      if (isBlocked) {
        console.log('🚫 检测到用户被封禁，触发封禁处理流程')
        console.log('错误数据:', errorData)
        // 清除所有认证信息
        localStorage.removeItem('token')
        localStorage.removeItem('rememberMe')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('tokenExpiry')
        
        // 设置封禁标记，用于多标签页同步
        localStorage.setItem('user_blocked', 'true')
        setTimeout(() => {
          localStorage.removeItem('user_blocked')
        }, 1000)
        
        // 触发自定义事件，通知应用用户被封禁
        // 注意：不在这里跳转，由 App.vue 中的事件处理器来处理跳转
        window.dispatchEvent(new CustomEvent('user-blocked', {
          detail: { 
            message: '您的账号已被封禁，请联系管理员',
            error: error
          }
        }))
        
        return Promise.reject(error)
      }
    }

    if (status === 401 && !originalRequest._isRetry) {
      if (!isRefreshing) {
        isRefreshing = true
        try {
          const refreshResp = await axios.post(
            REFRESH_ENDPOINT,
            {},
            { withCredentials: useCSRF, baseURL }
          )
          const data = (refreshResp as any).data || refreshResp
          const newToken = data?.access || data?.access_token || data?.token
          if (!newToken) throw new Error('No access token from refresh response')
          localStorage.setItem('token', newToken)
          processQueue(null, newToken)
          return new Promise((resolve, reject) => {
            originalRequest._isRetry = true
            originalRequest.headers.set(ACCESS_HEADER, `${ACCESS_PREFIX} ${newToken}`)
            http
              .request(originalRequest)
              .then(resolve as any)
              .catch(reject)
          })
        } catch (err) {
          localStorage.removeItem('token')
          processQueue(err, null)
          return Promise.reject(err)
        } finally {
          isRefreshing = false
        }
      } else {
        // queue until refresh finished
        return new Promise((resolve, reject) => {
          pendingQueue.push({
            resolve: (token: string) => {
              originalRequest._isRetry = true
              originalRequest.headers.set(ACCESS_HEADER, `${ACCESS_PREFIX} ${token}`)
              http
                .request(originalRequest)
                .then(resolve as any)
                .catch(reject)
            },
            reject,
          })
        })
      }
    }

    // 保留完整的错误信息，包括 response 数据
    return Promise.reject(error)
  }
)

export default http
export type { AxiosRequestConfig, AxiosResponse }
