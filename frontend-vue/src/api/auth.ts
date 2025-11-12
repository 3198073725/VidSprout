import http from '../services/http'
import axios from 'axios'
import type { LoginResponse, UserSummary } from './types'

const BASE = '/v1'

export interface LoginPayload {
  username?: string
  email?: string
  password: string
  rememberMe?: boolean
  captcha?: string
  captchaSessionKey?: string
}

export interface LoginResponseExtended extends LoginResponse {
  refreshToken?: string
  tokenExpiry?: number
  expiresIn?: number
}

export interface CaptchaResponse {
  captchaImage: string
  sessionKey: string
}

export interface PasswordStrengthResponse {
  strength: 'weak' | 'medium' | 'strong'
  message: string
  errors?: Record<string, string[]>
}

export interface SecurityLog {
  event_type: string
  level: string
  message: string
  ip_address: string
  created_at: string
}

export interface SecurityLogsResponse {
  logs: SecurityLog[]
  total: number
}

export interface LoginAttempt {
  status: string
  ip_address: string
  attempt_time: string
  failure_reason: string
}

export interface LoginAttemptsResponse {
  attempts: LoginAttempt[]
  total: number
}

export interface SuspiciousActivity {
  id: number
  ip_address: string
  activity_type: string
  description: string
  risk_score: number
  created_at: string
}

export interface SuspiciousActivitiesResponse {
  activities: SuspiciousActivity[]
  total: number
}

export interface SecuritySettings {
  max_login_attempts: number
  lockout_duration: number
  captcha_threshold: number
  password_expiry_days: number
  captcha_timeout: number
}

export interface BlockIPPayload {
  ip_address: string
  duration_hours?: number
}

// 登录相关API（MediaCMS 使用 Session 认证）
export async function login(payload: LoginPayload): Promise<LoginResponseExtended> {
  // MediaCMS 登录端点 - 使用 /api/v1/login（REST API）或 /accounts/login（Session）
  // 根据后端配置，我们使用 REST API 端点
  const formData = new FormData()
  
  if (payload.username && payload.username.trim()) {
    formData.append('username', payload.username.trim())
  }
  if (payload.email && payload.email.trim()) {
    formData.append('email', payload.email.trim())
  }
  if (!payload.password) {
    throw new Error('Password is required')
  }
  formData.append('password', payload.password)
  
  try {
    // 首先尝试使用 REST API 端点
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const response: any = await http.post(`${BASE}/login`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  
    // MediaCMS REST API 返回用户 token
  if (response.token || response.key) {
    return {
      token: response.token || response.key,
    } as LoginResponseExtended
  }
  
  throw new Error('Login failed: no token received')
  } catch (error: any) {
    // 如果 REST API 失败，回退到 Session 认证
    if (error.response?.status === 404) {
      // 使用 Session 认证端点（Django allauth，不使用 /api 前缀）
      const backendURL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
      const sessionResponse: any = await axios.post('/accounts/login/', formData, {
        baseURL: backendURL, // 使用后端完整 URL，不使用 /api 前缀
        withCredentials: true,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      // Session 认证成功后，获取 token
      const tokenResponse = await getUserToken()
      return {
        token: tokenResponse.token,
      } as LoginResponseExtended
    }
    throw error
  }
}

export interface RefreshTokenPayload {
  refreshToken: string
}

export async function refreshToken(payload: RefreshTokenPayload): Promise<LoginResponseExtended> {
  const params = new URLSearchParams()
  params.append('refresh_token', payload.refreshToken)
  
  return http.post(`${BASE}/refresh-token`, params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}

export async function getUserToken(): Promise<{ token: string }> {
  return http.get(`${BASE}/user/token`)
}

export async function whoami(): Promise<UserSummary> {
  // MediaCMS 的用户信息端点（注意：端点路径是 /api/v1/whoami，不是 /api/v1/user/whoami）
  return http.get(`${BASE}/whoami`)
}

// 验证码相关API
export async function getCaptcha(): Promise<CaptchaResponse> {
  return http.get(`${BASE}/captcha`)
}

export interface ValidateCaptchaPayload {
  sessionKey: string
  captcha: string
}

export async function validateCaptcha(payload: ValidateCaptchaPayload): Promise<{ detail: string }> {
  return http.post(`${BASE}/captcha`, payload)
}

// 密码强度检查API
export interface CheckPasswordStrengthPayload {
  password: string
}

export async function checkPasswordStrength(payload: CheckPasswordStrengthPayload): Promise<PasswordStrengthResponse> {
  return http.post(`${BASE}/password-strength`, payload)
}

// 安全日志相关API
export async function getSecurityLogs(): Promise<SecurityLogsResponse> {
  return http.get(`${BASE}/security-logs`)
}

export async function getLoginAttempts(): Promise<LoginAttemptsResponse> {
  return http.get(`${BASE}/login-attempts`)
}

// 可疑活动相关API（管理员）
export async function getSuspiciousActivities(): Promise<SuspiciousActivitiesResponse> {
  return http.get(`${BASE}/suspicious-activities`)
}

export async function blockIP(payload: BlockIPPayload): Promise<{ detail: string }> {
  return http.post(`${BASE}/suspicious-activities`, payload)
}

// 安全设置相关API（管理员）
export async function getSecuritySettings(): Promise<SecuritySettings> {
  return http.get(`${BASE}/security-settings`)
}

export interface UpdateSecuritySettingsPayload {
  max_login_attempts?: number
  lockout_duration?: number
  captcha_threshold?: number
  password_expiry_days?: number
  enable_two_factor?: boolean
}

export async function updateSecuritySettings(payload: UpdateSecuritySettingsPayload): Promise<{ detail: string; settings: SecuritySettings }> {
  return http.post(`${BASE}/security-settings`, payload)
}
