<template>
  <div class="settings-container" v-loading="loading" element-loading-text="加载中...">
    <el-tabs v-model="activeTab" type="border-card">
      <!-- 基本设置 -->
      <el-tab-pane label="基本设置" name="basic">
        <el-form
          ref="basicFormRef"
          :model="basicSettings"
          label-width="180px"
          style="max-width: 800px"
        >
          <el-divider content-position="left">站点信息</el-divider>

          <el-form-item label="站点名称">
            <el-input v-model="basicSettings.siteName" placeholder="请输入站点名称" />
          </el-form-item>

          <el-form-item label="站点描述">
            <el-input
              v-model="basicSettings.siteDescription"
              type="textarea"
              :rows="3"
              placeholder="请输入站点描述"
            />
          </el-form-item>

          <el-form-item label="站点关键词">
            <el-input v-model="basicSettings.siteKeywords" placeholder="多个关键词用逗号分隔" />
          </el-form-item>

          <el-divider content-position="left">功能开关</el-divider>

          <el-form-item label="允许用户注册">
            <el-switch v-model="basicSettings.allowRegistration" />
          </el-form-item>

          <el-form-item label="新用户需要审核">
            <el-switch v-model="basicSettings.requireApproval" />
          </el-form-item>

          <el-form-item label="允许评论">
            <el-switch v-model="basicSettings.enableComments" />
          </el-form-item>

          <el-form-item label="评论需要审核">
            <el-switch v-model="basicSettings.moderateComments" />
          </el-form-item>

          <el-form-item label="允许评分">
            <el-switch v-model="basicSettings.enableRatings" />
          </el-form-item>

          <el-form-item label="允许举报">
            <el-switch v-model="basicSettings.enableReporting" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveBasicSettings" :loading="saving">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="resetBasicSettings">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 上传设置 -->
      <el-tab-pane label="上传设置" name="upload">
        <el-form
          ref="uploadFormRef"
          :model="uploadSettings"
          label-width="180px"
          style="max-width: 800px"
        >
          <el-divider content-position="left">文件限制</el-divider>

          <el-form-item label="最大文件大小(MB)">
            <el-input-number
              v-model="uploadSettings.maxFileSize"
              :min="1"
              :max="10240"
              :step="100"
            />
          </el-form-item>

          <el-form-item label="允许的视频格式">
            <el-input v-model="uploadSettings.allowedVideoFormats" placeholder="如: mp4,avi,mov" />
          </el-form-item>

          <el-form-item label="允许的图片格式">
            <el-input v-model="uploadSettings.allowedImageFormats" placeholder="如: jpg,png,gif" />
          </el-form-item>

          <el-form-item label="允许的音频格式">
            <el-input v-model="uploadSettings.allowedAudioFormats" placeholder="如: mp3,wav,ogg" />
          </el-form-item>

          <el-divider content-position="left">编码设置</el-divider>

          <el-form-item label="自动编码">
            <el-switch v-model="uploadSettings.autoEncode" />
          </el-form-item>

          <el-form-item label="默认编码质量">
            <el-select v-model="uploadSettings.defaultQuality">
              <el-option label="低质量" value="low" />
              <el-option label="中等质量" value="medium" />
              <el-option label="高质量" value="high" />
              <el-option label="超高质量" value="ultra" />
            </el-select>
          </el-form-item>

          <el-form-item label="生成缩略图">
            <el-switch v-model="uploadSettings.generateThumbnails" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveUploadSettings" :loading="saving">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="resetUploadSettings">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 安全设置 -->
      <el-tab-pane label="安全设置" name="security">
        <el-form
          ref="securityFormRef"
          :model="securitySettings"
          label-width="180px"
          style="max-width: 800px"
        >
          <el-divider content-position="left">访问控制</el-divider>

          <el-form-item label="启用验证码">
            <el-switch v-model="securitySettings.enableCaptcha" />
          </el-form-item>

          <el-form-item label="最大登录尝试次数">
            <el-input-number
              v-model="securitySettings.maxLoginAttempts"
              :min="3"
              :max="10"
            />
          </el-form-item>

          <el-form-item label="登录锁定时间(分钟)">
            <el-input-number
              v-model="securitySettings.lockoutDuration"
              :min="5"
              :max="60"
            />
          </el-form-item>

          <el-divider content-position="left">内容安全</el-divider>

          <el-form-item label="启用内容审核">
            <el-switch v-model="securitySettings.enableModeration" />
          </el-form-item>

          <el-form-item label="敏感词过滤">
            <el-switch v-model="securitySettings.enableWordFilter" />
          </el-form-item>

          <el-form-item label="允许的域名(跨域)">
            <el-input
              v-model="securitySettings.allowedDomains"
              type="textarea"
              :rows="3"
              placeholder="每行一个域名"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveSecuritySettings" :loading="saving">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="resetSecuritySettings">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 邮件设置 -->
      <el-tab-pane label="邮件设置" name="email">
        <el-form
          ref="emailFormRef"
          :model="emailSettings"
          label-width="180px"
          style="max-width: 800px"
        >
          <el-divider content-position="left">SMTP 配置</el-divider>

          <el-form-item label="启用邮件发送">
            <el-switch v-model="emailSettings.enableEmail" />
          </el-form-item>

          <el-form-item label="SMTP 服务器">
            <el-input v-model="emailSettings.smtpHost" placeholder="如: smtp.gmail.com" />
          </el-form-item>

          <el-form-item label="SMTP 端口">
            <el-input-number v-model="emailSettings.smtpPort" :min="1" :max="65535" />
          </el-form-item>

          <el-form-item label="发件人邮箱">
            <el-input v-model="emailSettings.fromEmail" placeholder="noreply@example.com" />
          </el-form-item>

          <el-form-item label="发件人名称">
            <el-input v-model="emailSettings.fromName" placeholder="MediaCMS" />
          </el-form-item>

          <el-form-item label="使用 TLS">
            <el-switch v-model="emailSettings.useTLS" />
          </el-form-item>

          <el-divider content-position="left">邮件通知</el-divider>

          <el-form-item label="注册欢迎邮件">
            <el-switch v-model="emailSettings.sendWelcomeEmail" />
          </el-form-item>

          <el-form-item label="评论通知邮件">
            <el-switch v-model="emailSettings.sendCommentNotification" />
          </el-form-item>

          <el-form-item label="点赞通知邮件">
            <el-switch v-model="emailSettings.sendLikeNotification" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveEmailSettings" :loading="saving">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="handleTestEmail" :loading="testingEmail">
              <el-icon><Promotion /></el-icon>
              发送测试邮件
            </el-button>
            <el-button @click="resetEmailSettings">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 功能开关（第一阶段新增） -->
      <el-tab-pane label="功能开关" name="features">
        <el-form
          ref="featuresFormRef"
          :model="featuresSettings"
          label-width="180px"
          style="max-width: 800px"
        >
          <el-divider content-position="left">UI 按钮控制</el-divider>

          <el-form-item label="登录按钮">
            <el-switch v-model="featuresSettings.loginAllowed" />
            <span class="form-hint">控制是否显示登录按钮</span>
          </el-form-item>

          <el-form-item label="注册按钮">
            <el-switch v-model="featuresSettings.registerAllowed" />
            <span class="form-hint">控制是否显示注册按钮</span>
          </el-form-item>

          <el-form-item label="上传按钮">
            <el-switch v-model="featuresSettings.uploadMediaAllowed" />
            <span class="form-hint">控制是否显示上传媒体按钮</span>
          </el-form-item>

          <el-form-item label="点赞按钮">
            <el-switch v-model="featuresSettings.canLikeMedia" />
          </el-form-item>

          <el-form-item label="踩按钮">
            <el-switch v-model="featuresSettings.canDislikeMedia" />
          </el-form-item>

          <el-form-item label="举报按钮">
            <el-switch v-model="featuresSettings.canReportMedia" />
          </el-form-item>

          <el-form-item label="分享按钮">
            <el-switch v-model="featuresSettings.canShareMedia" />
          </el-form-item>

          <el-divider content-position="left">高级功能</el-divider>

          <el-form-item label="时间戳评论">
            <el-switch v-model="featuresSettings.timestampInTimebar" />
            <span class="form-hint">评论中的时间戳显示在视频时间轴</span>
          </el-form-item>

          <el-form-item label="@提及用户">
            <el-switch v-model="featuresSettings.allowMentionInComments" />
            <span class="form-hint">允许在评论中使用@提及其他用户</span>
          </el-form-item>

          <el-form-item label="视频剪辑">
            <el-switch v-model="featuresSettings.allowVideoTrimmer" />
            <span class="form-hint">允许用户剪辑视频</span>
          </el-form-item>

          <el-form-item label="自定义媒体URL">
            <el-switch v-model="featuresSettings.allowCustomMediaUrls" />
            <span class="form-hint">允许用户设置自定义媒体URL</span>
          </el-form-item>

          <el-form-item label="生成站点地图">
            <el-switch v-model="featuresSettings.generateSitemap" />
            <span class="form-hint">自动生成sitemap.xml</span>
          </el-form-item>

          <el-divider content-position="left">资源和访问控制</el-divider>

          <el-form-item label="从CDN加载资源">
            <el-switch v-model="featuresSettings.loadFromCdn" />
            <span class="form-hint">从CDN加载静态资源（CSS/JS）</span>
          </el-form-item>

          <el-form-item label="需要登录访问">
            <el-switch v-model="featuresSettings.globalLoginRequired" />
            <span class="form-hint" style="color: #e6a23c;">启用后，整个站点需要登录才能访问</span>
          </el-form-item>

          <el-form-item label="显示原始文件链接">
            <el-switch v-model="featuresSettings.showOriginalMedia" />
            <span class="form-hint">在媒体页面显示原始文件下载链接</span>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="saveFeaturesSettings" :loading="saving">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="resetFeaturesSettings">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- 用户权限（第一阶段新增） -->
      <el-tab-pane label="用户权限" name="permissions">
        <el-form
          ref="permissionsFormRef"
          :model="permissionsSettings"
          label-width="180px"
          style="max-width: 800px"
        >
          <el-divider content-position="left">用户能力</el-divider>

          <el-form-item label="谁可以上传媒体">
            <el-select v-model="permissionsSettings.canAddMedia">
              <el-option label="所有人" value="all" />
              <el-option label="已验证邮箱" value="email_verified" />
              <el-option label="高级用户" value="advancedUser" />
            </el-select>
          </el-form-item>

          <el-form-item label="谁可以评论">
            <el-select v-model="permissionsSettings.canComment">
              <el-option label="所有人" value="all" />
              <el-option label="已验证邮箱" value="email_verified" />
              <el-option label="高级用户" value="advancedUser" />
            </el-select>
          </el-form-item>

          <el-form-item label="谁可以查看会员页面">
            <el-select v-model="permissionsSettings.canSeeMembersPage">
              <el-option label="所有人" value="all" />
              <el-option label="编辑" value="editors" />
              <el-option label="管理员" value="admins" />
            </el-select>
          </el-form-item>

          <el-divider content-position="left">注册配置</el-divider>

          <el-form-item label="新用户需要批准">
            <el-switch v-model="permissionsSettings.usersNeedsToBeApproved" />
            <span class="form-hint">启用后，新注册用户需要管理员批准才能登录</span>
          </el-form-item>

          <el-form-item label="匿名用户可列出所有用户">
            <el-switch v-model="permissionsSettings.allowAnonymousUserListing" />
            <span class="form-hint">允许未登录用户查看用户列表</span>
          </el-form-item>

          <el-divider content-position="left">匿名用户权限</el-divider>

          <el-form-item label="允许的匿名操作">
            <el-input 
              v-model="permissionsSettings.allowAnonymousActions" 
              placeholder="如: report,like,dislike,watch"
            />
            <span class="form-hint">逗号分隔，可选：report, like, dislike, watch, comment</span>
          </el-form-item>

          <el-form-item label="匿名操作限制间隔(秒)">
            <el-input-number
              v-model="permissionsSettings.timeToActionAnonymous"
              :min="60"
              :max="3600"
              :step="60"
            />
            <span class="form-hint">同一IP两次操作之间的最小间隔时间</span>
          </el-form-item>

          <el-divider content-position="left">上传限制</el-divider>

          <el-form-item label="用户最大上传数量">
            <el-input-number
              v-model="permissionsSettings.numberOfMediaUserCanUpload"
              :min="1"
              :max="10000"
              :step="10"
            />
            <span class="form-hint">每个用户可上传的最大媒体数量</span>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="savePermissionsSettings" :loading="saving">
              <el-icon><Check /></el-icon>
              保存设置
            </el-button>
            <el-button @click="resetPermissionsSettings">
              <el-icon><RefreshLeft /></el-icon>
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { getSettings, updateSettings, sendTestEmail, type SystemSettings } from '@/api/system'

const activeTab = ref('basic')
const loading = ref(false)
const saving = ref(false)
const testingEmail = ref(false)

// 原始数据（用于重置）
const originalSettings = ref<SystemSettings | null>(null)

// 基本设置
const basicFormRef = ref<FormInstance>()
const basicSettings = ref({
  siteName: '',
  siteDescription: '',
  siteKeywords: '',
  allowRegistration: true,
  requireApproval: false,
  enableComments: true,
  moderateComments: false,
  enableRatings: true,
  enableReporting: true
})

// 上传设置
const uploadFormRef = ref<FormInstance>()
const uploadSettings = ref({
  maxFileSize: 1024,
  allowedVideoFormats: '',
  allowedImageFormats: '',
  allowedAudioFormats: '',
  autoEncode: true,
  defaultQuality: 'medium',
  generateThumbnails: true
})

// 安全设置
const securityFormRef = ref<FormInstance>()
const securitySettings = ref({
  enableCaptcha: false,
  maxLoginAttempts: 5,
  lockoutDuration: 15,
  enableModeration: true,
  enableWordFilter: true,
  allowedDomains: ''
})

// 邮件设置
const emailFormRef = ref<FormInstance>()
const emailSettings = ref({
  enableEmail: false,
  smtpHost: '',
  smtpPort: 587,
  fromEmail: '',
  fromName: '',
  useTLS: true,
  sendWelcomeEmail: true,
  sendCommentNotification: true,
  sendLikeNotification: false
})

// 功能开关（第一阶段新增）
const featuresFormRef = ref<FormInstance>()
const featuresSettings = ref({
  loginAllowed: true,
  registerAllowed: true,
  uploadMediaAllowed: true,
  canLikeMedia: true,
  canDislikeMedia: true,
  canReportMedia: true,
  canShareMedia: true,
  timestampInTimebar: false,
  allowMentionInComments: false,
  allowVideoTrimmer: true,
  allowCustomMediaUrls: false,
  generateSitemap: false,
  loadFromCdn: false,
  globalLoginRequired: false,
  showOriginalMedia: true,
})

// 用户权限（第一阶段新增）
const permissionsFormRef = ref<FormInstance>()
const permissionsSettings = ref({
  canAddMedia: 'all',
  canComment: 'all',
  canSeeMembersPage: 'all',
  usersNeedsToBeApproved: false,
  allowAnonymousUserListing: true,
  allowAnonymousActions: 'report,like,dislike,watch',
  timeToActionAnonymous: 600,
  numberOfMediaUserCanUpload: 100,
})

/**
 * 加载系统设置
 * 从后端获取所有配置并分配到各个表单
 */
const loadSettings = async () => {
  loading.value = true
  try {
    const data = await getSettings()
    
    console.log('✅ 系统设置加载成功:', data)
    
    // 保存原始数据用于重置功能
    originalSettings.value = data
    
    // 赋值到各个表单
    Object.assign(basicSettings.value, data.basic)
    Object.assign(uploadSettings.value, data.upload)
    Object.assign(securitySettings.value, data.security)
    Object.assign(emailSettings.value, data.email)
    
    // 第一阶段新增：功能开关和用户权限
    if (data.features) {
      Object.assign(featuresSettings.value, data.features)
    }
    if (data.permissions) {
      Object.assign(permissionsSettings.value, data.permissions)
    }
    
    ElMessage.success('系统设置加载成功')
  } catch (error) {
    console.error('❌ 加载设置失败:', error)
    ElMessage.error('加载设置失败，使用默认配置')
  } finally {
    loading.value = false
  }
}

/**
 * 通用保存设置函数
 * @param settingsKey - 设置类型键名（basic, upload, security等）
 * @param settingsValue - 设置值对象
 * @param successMessage - 成功提示消息
 */
const saveSettings = async (settingsKey: string, settingsValue: any, successMessage: string) => {
  try {
    saving.value = true
    console.log(`📤 保存${successMessage}:`, settingsValue)
    
    await updateSettings({
      [settingsKey]: settingsValue
    })
    
    ElMessage.success(`${successMessage}保存成功`)
    
    // 重新加载以获取最新的元数据（更新时间等）
    await loadSettings()
  } catch (error: any) {
    console.error(`❌ 保存${successMessage}失败:`, error)
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

// 保存各类设置的快捷方法
const saveBasicSettings = () => saveSettings('basic', basicSettings.value, '基本设置')
const saveUploadSettings = () => saveSettings('upload', uploadSettings.value, '上传设置')
const saveSecuritySettings = () => saveSettings('security', securitySettings.value, '安全设置')
const saveEmailSettings = () => saveSettings('email', emailSettings.value, '邮件设置')

/**
 * 测试邮件发送功能
 * 发送测试邮件到配置的邮箱地址
 */
const handleTestEmail = async () => {
  try {
    testingEmail.value = true
    console.log('📧 发送测试邮件...')
    
    const result = await sendTestEmail()
    
    console.log('✅ 测试邮件发送成功:', result)
    ElMessage.success(result.detail || '测试邮件已发送，请检查邮箱')
  } catch (error: any) {
    console.error('❌ 发送测试邮件失败:', error)
    ElMessage.error(error.response?.data?.detail || '发送失败，请检查邮件配置')
  } finally {
    testingEmail.value = false
  }
}

/**
 * 通用重置设置函数
 * @param settingsKey - 设置类型键名
 * @param settingsRef - 设置的ref对象
 */
const resetSettings = (settingsKey: string, settingsRef: any) => {
  if (originalSettings.value && originalSettings.value[settingsKey]) {
    Object.assign(settingsRef.value, originalSettings.value[settingsKey])
    ElMessage.info('已重置为原始设置')
  }
}

// 重置各类设置的快捷方法
const resetBasicSettings = () => resetSettings('basic', basicSettings)
const resetUploadSettings = () => resetSettings('upload', uploadSettings)
const resetSecuritySettings = () => resetSettings('security', securitySettings)
const resetEmailSettings = () => resetSettings('email', emailSettings)

// 第一阶段新增：功能开关和用户权限的保存/重置方法
const saveFeaturesSettings = () => saveSettings('features', featuresSettings.value, '功能开关设置')
const resetFeaturesSettings = () => resetSettings('features', featuresSettings)

const savePermissionsSettings = () => saveSettings('permissions', permissionsSettings.value, '用户权限设置')
const resetPermissionsSettings = () => resetSettings('permissions', permissionsSettings)

onMounted(() => {
  loadSettings()
})
</script>

<style scoped lang="scss">
.settings-container {
  height: 100%;

  :deep(.el-tabs__content) {
    padding: 20px;
  }

  :deep(.el-divider__text) {
    font-size: 16px;
    font-weight: 600;
  }
}
</style>
