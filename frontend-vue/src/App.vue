<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import { useUiStore } from './stores/ui'
import { useAuthStore } from './stores/auth'
import { computed, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const ui = useUiStore()
const auth = useAuthStore()

const rootClasses = computed(() => ({
  'sidebar-collapsed': ui.collapsed,
  'sidebar-mobile-open': ui.mobileOpen,
}))

// 防止重复显示封禁对话框
let isBlockedDialogShown = false

// 处理用户被封禁事件
const handleUserBlocked = (event: CustomEvent) => {
  console.log('🔔 收到 user-blocked 事件', event.detail)
  
  // 如果对话框已经显示，不重复显示
  if (isBlockedDialogShown) {
    console.log('⚠️ 对话框已显示，跳过')
    return
  }
  
  isBlockedDialogShown = true
  const message = event.detail?.message || '您的账号已被封禁，请联系管理员'
  
  console.log('🚫 显示封禁对话框')
  console.log('📦 ElMessageBox 对象:', ElMessageBox)
  console.log('📝 消息内容:', message)
  
  // 先显示对话框，然后在用户确认后再清除状态和跳转
  console.log('⏳ 准备调用 ElMessageBox.alert...')
  
  try {
    ElMessageBox.alert(message, '账号已被封禁', {
      confirmButtonText: '确定',
      type: 'error',
      showClose: false,
      closeOnClickModal: false,
      closeOnPressEscape: false,
      callback: () => {
        console.log('👤 用户点击确定，准备清除状态并跳转')
        // 清除认证状态
        auth.logout()
        // 跳转到登录页
        if (window.location.pathname !== '/login') {
          window.location.href = '/login?blocked=true'
        }
      }
    }).then(() => {
      console.log('✅ 对话框 Promise resolved')
    }).catch((error) => {
      // 处理对话框被关闭的情况
      console.log('⚠️ 对话框被意外关闭，强制跳转', error)
      auth.logout()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login?blocked=true'
      }
    })
    
    console.log('✅ ElMessageBox.alert 已调用')
  } catch (error) {
    console.error('❌ 调用 ElMessageBox.alert 失败:', error)
    // 如果对话框失败，直接跳转
    auth.logout()
    window.location.href = '/login?blocked=true'
  }
}

// 处理跨标签页的存储变化（例如在另一个标签页被封禁或登出）
const handleStorageChange = (event: StorageEvent) => {
  console.log('🔄 检测到 localStorage 变化:', event.key, event.newValue)
  
  // 如果 token 被清除（在另一个标签页），说明用户可能被封禁或登出
  if (event.key === 'token' && !event.newValue) {
    console.log('⚠️ Token 在其他标签页被清除，同步登出当前标签页')
    
    // 清除当前标签页的认证状态
    auth.logout()
    
    // 如果不在登录页，跳转到登录页
    if (window.location.pathname !== '/login') {
      ElMessage.warning({
        message: '您的登录状态已在其他标签页失效',
        duration: 3000
      })
      setTimeout(() => {
        window.location.href = '/login?session_expired=true'
      }, 1000)
    }
  }
  
  // 如果是封禁标记被设置
  if (event.key === 'user_blocked' && event.newValue === 'true') {
    console.log('⚠️ 检测到其他标签页的封禁事件')
    if (!isBlockedDialogShown) {
      window.dispatchEvent(new CustomEvent('user-blocked', {
        detail: { message: '您的账号已被封禁，请联系管理员' }
      }))
    }
  }
}

// 在应用启动时，尝试自动登录或从 Django 传递的数据初始化
onMounted(async () => {
  // 监听用户被封禁事件
  window.addEventListener('user-blocked', handleUserBlocked as EventListener)
  console.log('✅ 已注册 user-blocked 事件监听器')
  
  // 监听跨标签页的存储变化
  window.addEventListener('storage', handleStorageChange)
  console.log('✅ 已注册 storage 事件监听器（多标签页同步）')
  
  // 检查 URL 参数，如果是因为封禁跳转来的，显示提示
  const urlParams = new URLSearchParams(window.location.search)
  if (urlParams.get('blocked') === 'true') {
    ElMessage.error({
      message: '您的账号已被封禁，无法继续使用',
      duration: 5000,
      showClose: true
    })
    // 清除 URL 参数
    window.history.replaceState({}, '', '/login')
  }
  
  // 如果 Django 传递了用户数据，优先使用
  if (window.__INITIAL_STATE__?.user) {
    const djangoUser = window.__INITIAL_STATE__.user
    // 将 Django 用户数据转换为前端格式
    // 注意：这里需要根据实际的 auth store 结构来适配
    // 如果 Django Session 认证，可能需要调用 API 获取完整用户信息
    try {
      await auth.fetchProfile()
    } catch (error: any) {
      console.warn('Failed to fetch profile from Django:', error)
      // 检查是否是封禁错误（以防拦截器没有捕获）
      const errorData = error?.response?.data
      if (errorData?.blocked || errorData?.code === 'user_blocked') {
        console.log('⚠️ App.vue 检测到封禁错误，手动触发事件')
        window.dispatchEvent(new CustomEvent('user-blocked', {
          detail: { 
            message: errorData?.detail || '您的账号已被封禁，请联系管理员'
          }
        }))
      }
    }
  } else {
    // 初始化认证状态（如果有 token，会自动恢复登录状态）
    try {
      await auth.initializeAuth()
    } catch (error: any) {
      console.warn('Failed to initialize auth:', error)
      // 检查是否是封禁错误（以防拦截器没有捕获）
      const errorData = error?.response?.data
      if (errorData?.blocked || errorData?.code === 'user_blocked') {
        console.log('⚠️ App.vue 检测到封禁错误，手动触发事件')
        window.dispatchEvent(new CustomEvent('user-blocked', {
          detail: { 
            message: errorData?.detail || '您的账号已被封禁，请联系管理员'
          }
        }))
      }
    }
  }
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('user-blocked', handleUserBlocked as EventListener)
  window.removeEventListener('storage', handleStorageChange)
})
</script>

<template>
  <div :class="['app-container', rootClasses]">
    <AppHeader />
    <AppSidebar />
    <div class="page-main-wrap">
      <div class="page-main">
        <div class="page-main-inner">
          <router-view />
        </div>
        <div class="page-sidebar-content-overlay" @click="ui.closeMobile()"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 根容器 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 主要内容区域 */
.page-main-wrap {
  flex: 1; /* 占据剩余空间 */
  display: flex;
  flex-direction: column;
}

.page-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.page-main-inner {
  flex: 1;
}
</style>
