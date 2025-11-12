<template>
  <div class="error-boundary">
    <slot v-if="!hasError" />
    <div v-else class="error-container">
      <div class="error-content">
        <el-icon class="error-icon"><Warning /></el-icon>
        <h2 class="error-title">出错了</h2>
        <p class="error-message">{{ errorMessage }}</p>
        <div class="error-actions">
          <el-button type="primary" @click="resetError">重试</el-button>
          <el-button @click="goHome">返回首页</el-button>
        </div>
        <details v-if="showDetails" class="error-details">
          <summary>详细信息</summary>
          <pre class="error-stack">{{ errorStack }}</pre>
        </details>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Props {
  fallback?: string
  showDetails?: boolean
  onError?: (error: Error, instance: any, info: string) => void
}

const props = withDefaults(defineProps<Props>(), {
  fallback: '组件加载失败，请稍后重试',
  showDetails: process.env.NODE_ENV === 'development'
})

const emit = defineEmits<{
  error: [error: Error, instance: any, info: string]
  reset: []
}>()

const router = useRouter()
const hasError = ref(false)
const errorMessage = ref('')
const errorStack = ref('')
const errorInstance = ref<any>(null)
const errorInfo = ref('')

// 错误处理函数
const handleError = (error: Error, instance: any, info: string) => {
  console.error('ErrorBoundary捕获到错误:', error)
  console.error('错误信息:', info)
  
  hasError.value = true
  errorMessage.value = error.message || props.fallback
  errorStack.value = error.stack || ''
  errorInstance.value = instance
  errorInfo.value = info

  // 发送错误到监控系统
  sendErrorToMonitor(error, instance, info)

  // 显示用户友好的错误提示
  ElMessage.error('页面加载出错，请稍后重试')

  emit('error', error, instance, info)
}

// 重置错误状态
const resetError = () => {
  hasError.value = false
  errorMessage.value = ''
  errorStack.value = ''
  errorInstance.value = null
  errorInfo.value = ''
  
  emit('reset')
}

// 返回首页
const goHome = () => {
  router.push('/')
}

// 发送错误到监控系统
const sendErrorToMonitor = (error: Error, instance: any, info: string) => {
  // 这里可以集成错误监控服务，如Sentry、LogRocket等
  if (window.gtag) {
    window.gtag('event', 'exception', {
      description: error.message,
      fatal: false
    })
  }

  // 记录到本地存储，用于后续分析
  const errorLog = {
    timestamp: Date.now(),
    message: error.message,
    stack: error.stack,
    info,
    url: window.location.href,
    userAgent: navigator.userAgent
  }

  try {
    const existingLogs = JSON.parse(localStorage.getItem('error_logs') || '[]')
    existingLogs.push(errorLog)
    
    // 只保留最近50条错误日志
    if (existingLogs.length > 50) {
      existingLogs.splice(0, existingLogs.length - 50)
    }
    
    localStorage.setItem('error_logs', JSON.stringify(existingLogs))
  } catch (e) {
    console.error('记录错误日志失败:', e)
  }
}

// 监听错误
onErrorCaptured((error, instance, info) => {
  handleError(error, instance, info)
  return false // 阻止错误继续向上传播
})

// 监听路由变化，重置错误状态
watch(() => router.currentRoute.value.path, () => {
  if (hasError.value) {
    resetError()
  }
})
</script>

<style scoped>
.error-boundary {
  width: 100%;
  height: 100%;
}

.error-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 2rem;
}

.error-content {
  text-align: center;
  max-width: 500px;
}

.error-icon {
  font-size: 4rem;
  color: var(--el-color-danger);
  margin-bottom: 1rem;
}

.error-title {
  font-size: 1.5rem;
  color: var(--el-text-color-primary);
  margin-bottom: 0.5rem;
}

.error-message {
  color: var(--el-text-color-regular);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.error-details {
  text-align: left;
  background-color: var(--el-fill-color-lighter);
  border-radius: 4px;
  padding: 1rem;
}

.error-details summary {
  cursor: pointer;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.error-stack {
  font-size: 0.875rem;
  color: var(--el-text-color-secondary);
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 300px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .error-actions {
    flex-direction: column;
  }
}
</style>