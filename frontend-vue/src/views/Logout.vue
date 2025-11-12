<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const loading = ref(false)

// 获取重定向参数
const redirectTo = route.query.next as string || '/'

async function confirmLogout() {
  loading.value = true
  try {
    await auth.logout()
    ElMessage.success('已成功退出登录')
    
    // 重定向到指定页面或首页
    router.push(redirectTo)
  } catch (error) {
    console.error('退出登录失败:', error)
    ElMessage.error('退出登录失败')
  } finally {
    loading.value = false
  }
}

function cancelLogout() {
  // 返回上一页或首页
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/')
  }
}
</script>

<template>
  <div class="logout-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>退出登录</h1>
        
        <!-- 对应后端模板的确认信息 -->
        <div class="logout-content">
          <el-result
            icon="warning"
            title="确认退出"
            sub-title="您确定要退出登录吗？"
          >
            <template #extra>
              <!-- 对应后端模板的表单按钮 -->
              <div class="logout-actions">
                <el-button 
                  type="primary" 
                  :loading="loading"
                  @click="confirmLogout"
                  size="large"
                >
                  {{ loading ? '正在退出...' : '确认退出' }}
                </el-button>
                
                <!-- 对应后端模板的取消链接 -->
                <el-button 
                  @click="cancelLogout"
                  :disabled="loading"
                  size="large"
                >
                  取消
                </el-button>
              </div>
            </template>
          </el-result>
          
          <!-- 退出说明 -->
          <el-card class="logout-info" shadow="never">
            <template #header>
              <h3>退出登录说明</h3>
            </template>
            
            <div class="info-content">
              <p>退出登录后，您将：</p>
              <ul>
                <li>无法访问需要登录的功能</li>
                <li>丢失当前的登录状态</li>
                <li>需要重新登录才能使用个人功能</li>
                <li>本地存储的登录信息将被清除</li>
              </ul>
              
              <div class="security-note">
                <el-icon class="note-icon"><InfoFilled /></el-icon>
                <div class="note-text">
                  <strong>安全提醒：</strong>
                  <p>如果您在公共设备上使用，建议退出登录以保护账户安全。</p>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 快速操作 -->
          <el-card class="quick-actions" shadow="never">
            <template #header>
              <h3>其他操作</h3>
            </template>
            
            <div class="actions-grid">
              <el-button 
                class="action-button"
                @click="router.push('/password-change')"
                :disabled="loading"
              >
                <el-icon><Lock /></el-icon>
                修改密码
              </el-button>
              
              <el-button 
                class="action-button"
                @click="router.push('/email')"
                :disabled="loading"
              >
                <el-icon><Message /></el-icon>
                邮箱管理
              </el-button>
              
              <el-button 
                class="action-button"
                @click="router.push('/me')"
                :disabled="loading"
              >
                <el-icon><User /></el-icon>
                个人中心
              </el-button>
              
              <el-button 
                class="action-button"
                @click="router.push('/contact')"
                :disabled="loading"
              >
                <el-icon><Service /></el-icon>
                联系客服
              </el-button>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.logout-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

/* 对应后端模板的 user-action-form-wrap 样式 */
.user-action-form-wrap {
  display: flex;
  justify-content: center;
}

.user-action-form-inner {
  width: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 32px;
}

.user-action-form-inner h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 24px 0;
}

.logout-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.logout-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.logout-info,
.quick-actions {
  margin-top: 8px;
}

.logout-info :deep(.el-card__header),
.quick-actions :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.logout-info :deep(.el-card__header h3),
.quick-actions :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.info-content p {
  margin: 0 0 16px 0;
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.info-content ul {
  margin: 0 0 20px 0;
  padding-left: 20px;
  color: var(--mc-text-secondary);
}

.info-content li {
  margin-bottom: 6px;
  line-height: 1.5;
}

.security-note {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: var(--el-color-warning-light-9);
  border-radius: 8px;
  border-left: 4px solid var(--el-color-warning);
}

.note-icon {
  font-size: 20px;
  color: var(--el-color-warning);
  flex-shrink: 0;
  margin-top: 2px;
}

.note-text {
  flex: 1;
}

.note-text strong {
  display: block;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin-bottom: 4px;
}

.note-text p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  height: auto;
  border: 1px solid var(--el-border-color-light);
  background: var(--mc-bg-secondary);
  transition: all 0.3s ease;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--el-color-primary);
}

.action-button :deep(.el-icon) {
  font-size: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .logout-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .user-action-form-inner h1 {
    font-size: 1.5rem;
  }
  
  .logout-actions {
    flex-direction: column;
  }
  
  .logout-actions .el-button {
    width: 100%;
  }
  
  .security-note {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .action-button {
    padding: 12px;
  }
  
  .note-text strong {
    font-size: 0.95rem;
  }
  
  .note-text p {
    font-size: 0.85rem;
  }
}
</style>
