/**
 * 系统管理API
 */
import http from './http'

// 系统设置类型定义
export interface SystemSettings {
  basic: {
    siteName: string
    siteDescription: string
    siteKeywords: string
    allowRegistration: boolean
    requireApproval: boolean
    enableComments: boolean
    moderateComments: boolean
    enableRatings: boolean
    enableReporting: boolean
  }
  upload: {
    maxFileSize: number
    allowedVideoFormats: string
    allowedImageFormats: string
    allowedAudioFormats: string
    autoEncode: boolean
    defaultQuality: string
    generateThumbnails: boolean
  }
  security: {
    enableCaptcha: boolean
    maxLoginAttempts: number
    lockoutDuration: number
    enableModeration: boolean
    enableWordFilter: boolean
    allowedDomains: string
  }
  email: {
    enableEmail: boolean
    smtpHost: string
    smtpPort: number
    fromEmail: string
    fromName: string
    useTLS: boolean
    sendWelcomeEmail: boolean
    sendCommentNotification: boolean
    sendLikeNotification: boolean
  }
  // 第一阶段新增：功能开关
  features?: {
    loginAllowed: boolean
    registerAllowed: boolean
    uploadMediaAllowed: boolean
    canLikeMedia: boolean
    canDislikeMedia: boolean
    canReportMedia: boolean
    canShareMedia: boolean
    timestampInTimebar: boolean
    allowMentionInComments: boolean
    allowVideoTrimmer: boolean
    allowCustomMediaUrls: boolean
    generateSitemap: boolean
    loadFromCdn: boolean
    globalLoginRequired: boolean
    showOriginalMedia: boolean
  }
  // 第一阶段新增：用户权限
  permissions?: {
    canAddMedia: string
    canComment: string
    canSeeMembersPage: string
    usersNeedsToBeApproved: boolean
    allowAnonymousUserListing: boolean
    allowAnonymousActions: string
    timeToActionAnonymous: number
    numberOfMediaUserCanUpload: number
  }
  meta?: {
    lastUpdated: string
    updatedBy: string
  }
}

// 系统监控类型定义
export interface SystemMonitoring {
  systemInfo: {
    cpu: number
    memory: number
    disk: number
    network: number
    uploadSpeed: number
    downloadSpeed: number
  }
  systemDetails: {
    os: string
    hostname: string
    pythonVersion: string
    djangoVersion: string
    uptime: string
    database: string
  }
  processes: Array<{
    pid: number
    name: string
    cpu: number
    memory: number
    status: string
  }>
  trendData: Array<{
    date: string
    count: number
  }>
}

/**
 * 获取系统设置
 */
export const getSettings = () => {
  return http.get<SystemSettings>('/v1/admin/settings')
}

/**
 * 更新系统设置
 */
export const updateSettings = (data: Partial<SystemSettings>) => {
  return http.put<SystemSettings>('/v1/admin/settings', data)
}

/**
 * 获取系统监控数据
 */
export const getMonitoring = () => {
  return http.get<SystemMonitoring>('/v1/admin/monitoring')
}

/**
 * 发送测试邮件
 */
export const sendTestEmail = (email?: string) => {
  return http.post('/v1/admin/test-email', { email })
}

