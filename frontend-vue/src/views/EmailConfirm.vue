<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const confirming = ref(false)
const confirmationData = ref<any>(null)
const confirmed = ref(false)

// 从URL获取确认key
const confirmationKey = computed(() => String(route.params.key || route.query.key || ''))

async function loadConfirmationData() {
  if (!confirmationKey.value) {
    confirmationData.value = null
    return
  }
  
  loading.value = true
  try {
    // 这里应该调用获取确认信息的API
    // const data = await AuthAPI.getEmailConfirmationData(confirmationKey.value)
    
    // 模拟确认数据
    confirmationData.value = {
      email_address: {
        email: 'user@example.com',
        user: {
          username: 'testuser',
          name: '测试用户'
        }
      },
      key: confirmationKey.value,
      valid: true
    }
  } catch (error) {
    console.error('加载确认信息失败:', error)
    confirmationData.value = null
  } finally {
    loading.value = false
  }
}

async function confirmEmail() {
  if (!confirmationData.value) return
  
  confirming.value = true
  try {
    // 这里应该调用确认邮箱API
    // await AuthAPI.confirmEmail(confirmationKey.value)
    
    confirmed.value = true
    ElMessage.success('邮箱确认成功')
  } catch (error) {
    console.error('确认邮箱失败:', error)
    ElMessage.error('确认邮箱失败，请重试')
  } finally {
    confirming.value = false
  }
}

function goToEmailManage() {
  router.push('/email')
}

function requestNewConfirmation() {
  router.push('/email')
}

onMounted(loadConfirmationData)
</script>

<template>
  <div class="email-confirm-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="4" animated />
        </div>
        
        <!-- 对应后端模板的 {% if confirmation %} 条件 -->
        <div v-else-if="confirmationData && confirmationData.valid && !confirmed" class="confirmation-section">
          <h1>确认邮箱地址</h1>
          
          <!-- 对应后端模板的确认信息 -->
          <div class="confirmation-info">
            <el-alert
              title="邮箱确认"
              type="info"
              :closable="false"
              show-icon
            >
              <p>
                请确认 
                <strong>
                  <a :href="`mailto:${confirmationData.email_address.email}`">
                    {{ confirmationData.email_address.email }}
                  </a>
                </strong> 
                是用户 
                <strong>{{ confirmationData.email_address.user.name || confirmationData.email_address.user.username }}</strong> 
                的邮箱地址。
              </p>
            </el-alert>
          </div>
          
          <!-- 对应后端模板的确认表单 -->
          <div class="confirmation-form">
            <el-button 
              type="primary" 
              size="large"
              :loading="confirming"
              @click="confirmEmail"
              style="width: 100%"
            >
              {{ confirming ? '正在确认...' : '确认邮箱' }}
            </el-button>
          </div>
          
          <!-- 额外信息 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <h3>关于邮箱确认</h3>
            </template>
            
            <div class="info-content">
              <p>确认邮箱地址后，您将能够：</p>
              <ul>
                <li>接收重要的系统通知</li>
                <li>使用密码重置功能</li>
                <li>接收分享和评论提醒</li>
                <li>享受完整的平台功能</li>
              </ul>
            </div>
          </el-card>
        </div>
        
        <!-- 确认成功 -->
        <div v-else-if="confirmed" class="confirmation-success">
          <h1>邮箱确认成功</h1>
          
          <el-result
            icon="success"
            title="邮箱已成功确认"
            :sub-title="`${confirmationData?.email_address?.email} 已经成功绑定到您的账户`"
          >
            <template #extra>
              <div class="success-actions">
                <el-button type="primary" @click="goToEmailManage">
                  管理邮箱
                </el-button>
                <el-button @click="router.push('/')">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>
        </div>
        
        <!-- 对应后端模板的 {% else %} 确认链接无效 -->
        <div v-else class="confirmation-invalid">
          <h1>邮箱确认</h1>
          
          <el-result
            icon="error"
            title="确认链接无效或已过期"
            sub-title="此邮箱确认链接已过期或无效。"
          >
            <template #extra>
              <el-button type="primary" @click="requestNewConfirmation">
                申请新的确认邮件
              </el-button>
            </template>
          </el-result>
          
          <el-alert
            type="warning"
            :closable="false"
            show-icon
          >
            <p>可能的原因：</p>
            <ul>
              <li>确认链接已过期</li>
              <li>邮箱已经被确认过</li>
              <li>链接地址不完整或被修改</li>
              <li>确认链接已被使用</li>
            </ul>
          </el-alert>
          
          <div class="help-section">
            <h3>需要帮助？</h3>
            <p>如果您继续遇到问题，请尝试以下操作：</p>
            <div class="help-actions">
              <el-button @click="router.push('/email')">
                前往邮箱管理
              </el-button>
              <el-button @click="router.push('/contact')">
                联系客服
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.email-confirm-container {
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

.loading-container {
  padding: 20px;
}

.user-action-form-inner h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 24px 0;
}

.confirmation-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.confirmation-info :deep(.el-alert__content) {
  margin-top: 0;
}

.confirmation-info a {
  color: var(--el-color-primary);
  text-decoration: none;
}

.confirmation-info a:hover {
  text-decoration: underline;
}

.confirmation-form {
  display: flex;
  justify-content: center;
}

.info-card {
  margin-top: 8px;
}

.info-card :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.info-card :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.info-content p {
  margin: 0 0 12px 0;
  color: var(--mc-text-secondary);
}

.info-content ul {
  margin: 0;
  padding-left: 20px;
  color: var(--mc-text-secondary);
}

.info-content li {
  margin-bottom: 6px;
}

.confirmation-success {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.success-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.confirmation-invalid {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.confirmation-invalid :deep(.el-alert__content) {
  margin-top: 0;
}

.confirmation-invalid ul {
  margin: 8px 0;
  padding-left: 20px;
}

.confirmation-invalid li {
  margin-bottom: 4px;
}

.help-section {
  padding: 20px;
  background: var(--mc-bg-secondary);
  border-radius: 8px;
  text-align: center;
}

.help-section h3 {
  margin: 0 0 12px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.help-section p {
  margin: 0 0 16px 0;
  color: var(--mc-text-secondary);
}

.help-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .email-confirm-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .user-action-form-inner h1 {
    font-size: 1.5rem;
  }
  
  .success-actions,
  .help-actions {
    flex-direction: column;
  }
  
  .success-actions .el-button,
  .help-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .info-content p,
  .help-section p {
    font-size: 0.9rem;
  }
  
  .info-content li {
    font-size: 0.9rem;
  }
}
</style>
