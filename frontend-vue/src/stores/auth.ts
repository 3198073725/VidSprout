import { defineStore } from 'pinia'
import { AuthAPI } from '@/api'
import type { UserSummary } from '@/api'

interface State {
  token: string | null
  profile: UserSummary | null
  loading: boolean
  initialized: boolean
  rememberMe: boolean
  refreshToken: string | null
  tokenExpiry: number | null
}

export const useAuthStore = defineStore('auth', {
  state: (): State => ({
    token: localStorage.getItem('token'),
    profile: null as UserSummary | null,
    loading: false,
    initialized: false,
    rememberMe: localStorage.getItem('rememberMe') === 'true',
    refreshToken: localStorage.getItem('refreshToken'),
    tokenExpiry: localStorage.getItem('tokenExpiry') ? parseInt(localStorage.getItem('tokenExpiry')!) : null
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => !!(state.profile?.is_manager || state.profile?.is_editor),
    isInitialized: (state) => state.initialized,
  },
  actions: {
    async login(payload: { 
      username?: string; 
      email?: string; 
      password: string; 
      rememberMe?: boolean;
      captcha?: string;
      captchaSessionKey?: string;
    }) {
      this.loading = true
      try {
        // 先清除旧的 token 和用户信息，确保不会使用缓存的数据
        this.token = null
        this.profile = null
        this.refreshToken = null
        this.tokenExpiry = null
        this.clearStoredAuth()
        
        // 调用登录 API
        const res = await AuthAPI.login(payload)
        
        // 保存新的 token 和相关信息
        this.token = res.token
        this.rememberMe = payload.rememberMe || false
        this.refreshToken = res.refreshToken || null
        this.tokenExpiry = res.tokenExpiry || null
        
        // 存储到localStorage
        localStorage.setItem('token', res.token)
        localStorage.setItem('rememberMe', String(this.rememberMe))
        if (this.refreshToken) {
          localStorage.setItem('refreshToken', this.refreshToken)
        }
        if (this.tokenExpiry) {
          localStorage.setItem('tokenExpiry', String(this.tokenExpiry))
        }
        
        // 获取新用户的个人信息
        await this.fetchProfile()
        
        console.log('✅ 登录成功，用户:', this.profile?.username || '未知用户')
      } catch (e) {
        this.loading = false
        throw e
      } finally {
        this.loading = false
      }
    },
    async fetchProfile() {
      if (!this.token) {
        this.profile = null
        this.initialized = true
        return
      }
      try {
        this.profile = await AuthAPI.whoami()
        this.initialized = true
      } catch (e: any) {
        // 检查是否是封禁错误
        const errorData = e?.response?.data
        const isBlocked = 
          errorData?.blocked === true ||
          errorData?.code === 'user_blocked' ||
          errorData?.detail?.includes('封禁') ||
          errorData?.message?.includes('封禁')
        
        if (isBlocked) {
          // 封禁错误不在这里处理，让它传播到 http.ts 的拦截器
          console.log('⚠️ fetchProfile 检测到封禁错误，不进行处理')
          this.token = null
          this.profile = null
          this.initialized = true
          this.clearStoredAuth()
          // 重新抛出错误，让 http.ts 的拦截器处理
          throw e
        }
        
        // 如果 token 无效，尝试刷新token
        console.error('Failed to fetch profile:', e)
        if (this.rememberMe && this.refreshToken) {
          try {
            await this.refreshAccessToken()
            // 刷新成功后重新获取profile
            this.profile = await AuthAPI.whoami()
            this.initialized = true
            return
          } catch (refreshError) {
            console.error('Failed to refresh token:', refreshError)
          }
        }
        
        // 如果刷新失败或没有refresh token，清除登录状态
        this.token = null
        this.profile = null
        this.initialized = true
        this.clearStoredAuth()
      }
    },
    
    async refreshAccessToken() {
      if (!this.refreshToken) {
        throw new Error('No refresh token available')
      }
      
      try {
        const res = await AuthAPI.refreshToken({ refreshToken: this.refreshToken })
        this.token = res.token
        this.tokenExpiry = res.tokenExpiry || null
        
        localStorage.setItem('token', res.token)
        if (this.tokenExpiry) {
          localStorage.setItem('tokenExpiry', String(this.tokenExpiry))
        }
        
        return res
      } catch (e) {
        console.error('Token refresh failed:', e)
        throw e
      }
    },
    
    async autoLogin() {
      // 只要有 token，就尝试恢复登录状态（不限于 rememberMe）
      if (this.token) {
        try {
          // 直接尝试获取用户信息
          await this.fetchProfile()
          return true
        } catch (e) {
          console.error('Auto login failed:', e)
          // 如果获取失败，清除无效的token
          this.logout()
          return false
        }
      }
      return false
    },
    
    // 初始化认证状态（应用启动时调用）
    async initializeAuth() {
      // 如果已经有 token，尝试恢复登录状态
      if (this.token && !this.initialized) {
        try {
          await this.fetchProfile()
        } catch (e) {
          console.error('Failed to initialize auth:', e)
          // 如果 token 无效，清除它
          this.clearStoredAuth()
          this.token = null
          this.profile = null
          this.initialized = true
        }
      } else {
        // 没有 token，标记为已初始化
        this.initialized = true
      }
    },
    
    clearStoredAuth() {
      localStorage.removeItem('token')
      localStorage.removeItem('rememberMe')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('tokenExpiry')
    },
    logout() {
      this.token = null
      this.profile = null
      this.initialized = false
      this.refreshToken = null
      this.tokenExpiry = null
      this.clearStoredAuth()
    },
  },
})
