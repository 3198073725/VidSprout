import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios'
import { requestCache } from './cache'
import { debounce } from '@/utils/debounce'

interface ApiConfig {
  baseURL?: string
  timeout?: number
  cache?: boolean
  debounce?: number
  retryCount?: number
  retryDelay?: number
}

class ApiService {
  private instance: AxiosInstance
  private config: Required<ApiConfig>
  private requestCache = requestCache
  private pendingRequests = new Map<string, Promise<any>>()

  constructor(config: ApiConfig = {}) {
    this.config = {
      baseURL: config.baseURL || '/api',
      timeout: config.timeout || 30000,
      cache: config.cache ?? true,
      debounce: config.debounce ?? 300,
      retryCount: config.retryCount ?? 3,
      retryDelay: config.retryDelay ?? 1000
    }

    this.instance = axios.create({
      baseURL: this.config.baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 添加认证token
        const token = localStorage.getItem('token')
        if (token) {
          config.headers.Authorization = `Token ${token}`
        }

        // 添加请求ID用于防抖
        const requestId = this.generateRequestId(config)
        config.headers['X-Request-ID'] = requestId

        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response) => {
        return response
      },
      async (error) => {
        const { config: originalConfig } = error

        // 重试机制
        if (originalConfig && this.shouldRetry(error)) {
          originalConfig._retryCount = (originalConfig._retryCount || 0) + 1
          
          if (originalConfig._retryCount <= this.config.retryCount) {
            await this.delay(this.config.retryDelay * originalConfig._retryCount)
            return this.instance(originalConfig)
          }
        }

        // 处理认证错误
        if (error.response?.status === 401) {
          localStorage.removeItem('token')
          window.location.href = '/login'
        }

        return Promise.reject(error)
      }
    )
  }

  private generateRequestId(config: AxiosRequestConfig): string {
    const { method, url, params, data } = config
    return `${method}-${url}-${JSON.stringify(params || {})}-${JSON.stringify(data || {})}`
  }

  private shouldRetry(error: any): boolean {
    return error.code === 'ECONNABORTED' || 
           error.response?.status >= 500 ||
           !error.response
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }

  private async executeRequest<T = any>(
    config: AxiosRequestConfig,
    useCache: boolean = this.config.cache,
    useDebounce: boolean = false
  ): Promise<AxiosResponse<T>> {
    const requestId = this.generateRequestId(config)

    // 检查缓存
    if (useCache && config.method?.toLowerCase() === 'get') {
      const cachedData = this.requestCache.get(config.url!, config.params)
      if (cachedData) {
        return Promise.resolve({
          data: cachedData,
          status: 200,
          statusText: 'OK',
          headers: {},
          config
        } as AxiosResponse<T>)
      }
    }

    // 检查是否有相同的pending请求
    if (this.pendingRequests.has(requestId)) {
      return this.pendingRequests.get(requestId)
    }

    // 创建请求
    const requestPromise = this.instance.request<T>(config)
      .then(response => {
        // 缓存响应
        if (useCache && config.method?.toLowerCase() === 'get') {
          this.requestCache.set(config.url!, response.data, config.params)
        }
        
        this.pendingRequests.delete(requestId)
        return response
      })
      .catch(error => {
        this.pendingRequests.delete(requestId)
        throw error
      })

    this.pendingRequests.set(requestId, requestPromise)
    return requestPromise
  }

  // GET请求
  async get<T = any>(
    url: string,
    params?: any,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    const requestConfig: AxiosRequestConfig = {
      ...config,
      method: 'GET',
      url,
      params
    }

    return this.executeRequest<T>(requestConfig)
  }

  // POST请求
  async post<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    const requestConfig: AxiosRequestConfig = {
      ...config,
      method: 'POST',
      url,
      data
    }

    return this.executeRequest<T>(requestConfig, false)
  }

  // PUT请求
  async put<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    const requestConfig: AxiosRequestConfig = {
      ...config,
      method: 'PUT',
      url,
      data
    }

    return this.executeRequest<T>(requestConfig, false)
  }

  // DELETE请求
  async delete<T = any>(
    url: string,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    const requestConfig: AxiosRequestConfig = {
      ...config,
      method: 'DELETE',
      url
    }

    return this.executeRequest<T>(requestConfig, false)
  }

  // PATCH请求
  async patch<T = any>(
    url: string,
    data?: any,
    config?: AxiosRequestConfig
  ): Promise<AxiosResponse<T>> {
    const requestConfig: AxiosRequestConfig = {
      ...config,
      method: 'PATCH',
      url,
      data
    }

    return this.executeRequest<T>(requestConfig, false)
  }

  // 创建防抖的请求方法
  createDebouncedRequest<T = any>(
    method: string,
    wait: number = this.config.debounce
  ) {
    return debounce(
      (url: string, data?: any, config?: AxiosRequestConfig) => {
        const requestConfig: AxiosRequestConfig = {
          ...config,
          method: method.toUpperCase(),
          url,
          ...(data && { data }),
          ...(method.toLowerCase() === 'get' && data && { params: data })
        }

        return this.executeRequest<T>(requestConfig, method.toLowerCase() === 'get', true)
      },
      wait
    )
  }

  // 清除缓存
  clearCache(): void {
    this.requestCache.clear()
  }

  // 获取缓存统计
  getCacheStats() {
    return this.requestCache.getStats()
  }
}

// 创建默认实例
export const apiService = new ApiService()

export default ApiService