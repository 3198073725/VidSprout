<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

interface EmailAddress {
  id: number
  email: string
  verified: boolean
  primary: boolean
}

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const saving = ref(false)
const emailAddresses = ref<EmailAddress[]>([])
const selectedEmail = ref('')
const newEmail = ref('')

// 模拟邮箱数据
const mockEmailAddresses: EmailAddress[] = [
  {
    id: 1,
    email: 'user@example.com',
    verified: true,
    primary: true
  },
  {
    id: 2,
    email: 'backup@example.com',
    verified: false,
    primary: false
  }
]

async function loadEmailAddresses() {
  loading.value = true
  try {
    // 这里应该调用邮箱管理API
    // emailAddresses.value = await UserAPI.getEmailAddresses()
    
    // 模拟数据
    emailAddresses.value = [...mockEmailAddresses]
    
    // 默认选中主邮箱
    const primaryEmail = emailAddresses.value.find(email => email.primary)
    if (primaryEmail) {
      selectedEmail.value = primaryEmail.email
    }
  } catch (error) {
    console.error('加载邮箱列表失败:', error)
    ElMessage.error('加载邮箱列表失败')
  } finally {
    loading.value = false
  }
}

async function makePrimary() {
  if (!selectedEmail.value) {
    ElMessage.warning('请选择一个邮箱')
    return
  }
  
  saving.value = true
  try {
    // 这里应该调用设置主邮箱API
    // await UserAPI.setPrimaryEmail(selectedEmail.value)
    
    // 更新本地数据
    emailAddresses.value.forEach(email => {
      email.primary = email.email === selectedEmail.value
    })
    
    ElMessage.success('主邮箱设置成功')
  } catch (error) {
    console.error('设置主邮箱失败:', error)
    ElMessage.error('设置主邮箱失败')
  } finally {
    saving.value = false
  }
}

async function resendVerification() {
  if (!selectedEmail.value) {
    ElMessage.warning('请选择一个邮箱')
    return
  }
  
  const selectedEmailObj = emailAddresses.value.find(email => email.email === selectedEmail.value)
  if (selectedEmailObj?.verified) {
    ElMessage.info('该邮箱已经验证过了')
    return
  }
  
  saving.value = true
  try {
    // 这里应该调用重发验证邮件API
    // await UserAPI.resendVerificationEmail(selectedEmail.value)
    
    ElMessage.success('验证邮件已发送')
  } catch (error) {
    console.error('发送验证邮件失败:', error)
    ElMessage.error('发送验证邮件失败')
  } finally {
    saving.value = false
  }
}

async function removeEmail() {
  if (!selectedEmail.value) {
    ElMessage.warning('请选择一个邮箱')
    return
  }
  
  const selectedEmailObj = emailAddresses.value.find(email => email.email === selectedEmail.value)
  if (selectedEmailObj?.primary) {
    ElMessage.error('不能删除主邮箱')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      '确定要删除选中的邮箱地址吗？',
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    saving.value = true
    
    // 这里应该调用删除邮箱API
    // await UserAPI.removeEmail(selectedEmail.value)
    
    // 更新本地数据
    emailAddresses.value = emailAddresses.value.filter(email => email.email !== selectedEmail.value)
    selectedEmail.value = emailAddresses.value.find(email => email.primary)?.email || ''
    
    ElMessage.success('邮箱已删除')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除邮箱失败:', error)
      ElMessage.error('删除邮箱失败')
    }
  } finally {
    saving.value = false
  }
}

async function addEmail() {
  if (!newEmail.value) {
    ElMessage.warning('请输入邮箱地址')
    return
  }
  
  // 验证邮箱格式
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(newEmail.value)) {
    ElMessage.error('请输入有效的邮箱地址')
    return
  }
  
  // 检查是否已存在
  if (emailAddresses.value.some(email => email.email === newEmail.value)) {
    ElMessage.error('该邮箱已存在')
    return
  }
  
  saving.value = true
  try {
    // 这里应该调用添加邮箱API
    // await UserAPI.addEmail(newEmail.value)
    
    // 更新本地数据
    const newEmailObj: EmailAddress = {
      id: Date.now(),
      email: newEmail.value,
      verified: false,
      primary: false
    }
    
    emailAddresses.value.push(newEmailObj)
    newEmail.value = ''
    
    ElMessage.success('邮箱已添加，请查收验证邮件')
  } catch (error) {
    console.error('添加邮箱失败:', error)
    ElMessage.error('添加邮箱失败')
  } finally {
    saving.value = false
  }
}

onMounted(loadEmailAddresses)
</script>

<template>
  <div class="email-manage-container">
    <!-- 对应后端模板的头部标题 -->
    <div class="page-header">
      <h1>邮箱地址管理</h1>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div v-else class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的邮箱列表部分 -->
        <div v-if="emailAddresses.length" class="email-list-section">
          <p class="section-description">
            以下邮箱地址与您的账户关联：
          </p>

          <!-- 对应后端的 email_list 表单 -->
          <div class="email-list">
            <div class="email-items">
              <div 
                v-for="(emailAddress, index) in emailAddresses" 
                :key="emailAddress.id"
                class="email-item"
              >
                <el-radio 
                  v-model="selectedEmail" 
                  :value="emailAddress.email"
                  :class="{ 'primary-email': emailAddress.primary }"
                >
                  <div class="email-info">
                    <span class="email-address">{{ emailAddress.email }}</span>
                    <div class="email-badges">
                      <el-tag 
                        v-if="emailAddress.verified" 
                        type="success" 
                        size="small"
                      >
                        已验证
                      </el-tag>
                      <el-tag 
                        v-else 
                        type="warning" 
                        size="small"
                      >
                        未验证
                      </el-tag>
                      <el-tag 
                        v-if="emailAddress.primary" 
                        type="primary" 
                        size="small"
                      >
                        主邮箱
                      </el-tag>
                    </div>
                  </div>
                </el-radio>
              </div>
            </div>

            <!-- 对应后端的 buttonHolder 操作按钮 -->
            <div class="button-holder">
              <el-button 
                :loading="saving"
                :disabled="!selectedEmail"
                @click="makePrimary"
              >
                设为主邮箱
              </el-button>
              
              <el-button 
                :loading="saving"
                :disabled="!selectedEmail"
                @click="resendVerification"
              >
                重发验证邮件
              </el-button>
              
              <el-button 
                type="danger"
                :loading="saving"
                :disabled="!selectedEmail || emailAddresses.find(e => e.email === selectedEmail)?.primary"
                @click="removeEmail"
              >
                删除
              </el-button>
            </div>
          </div>
        </div>

        <!-- 对应后端模板的警告信息 -->
        <div v-else class="no-email-warning">
          <el-alert
            title="警告"
            type="warning"
            :closable="false"
            show-icon
          >
            <p>
              您当前没有设置任何邮箱地址。您应该添加一个邮箱地址，以便接收通知、重置密码等。
            </p>
          </el-alert>
        </div>

        <!-- 对应后端模板的添加邮箱部分 -->
        <div class="add-email-section">
          <h2>添加邮箱地址</h2>
          
          <!-- 对应后端的 add_email 表单 -->
          <el-form class="add-email-form" @submit.prevent="addEmail">
            <el-form-item label="邮箱地址" required>
              <el-input
                v-model="newEmail"
                type="email"
                placeholder="输入新的邮箱地址"
                :disabled="saving"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                :loading="saving"
                @click="addEmail"
              >
                添加邮箱
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.email-manage-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0;
}

.loading-container {
  padding: 40px;
}

/* 对应后端模板的 user-action-form-wrap 样式 */
.user-action-form-wrap {
  display: flex;
  justify-content: center;
}

.user-action-form-inner {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 32px;
}

.email-list-section {
  margin-bottom: 32px;
}

.section-description {
  margin-bottom: 16px;
  color: var(--mc-text-secondary);
  line-height: 1.5;
}

.email-list {
  border: 1px solid var(--el-border-color-light);
  border-radius: 8px;
  overflow: hidden;
}

.email-items {
  background: var(--mc-bg-secondary);
}

.email-item {
  padding: 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.email-item:last-child {
  border-bottom: none;
}

.email-item :deep(.el-radio) {
  width: 100%;
}

.email-item :deep(.el-radio__label) {
  width: 100%;
  padding-left: 8px;
}

.email-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.email-address {
  font-size: 1rem;
  color: var(--mc-text-primary);
  font-weight: 500;
}

.email-badges {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.primary-email :deep(.el-radio__label) {
  font-weight: 600;
}

.button-holder {
  padding: 16px;
  background: white;
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.no-email-warning {
  margin-bottom: 32px;
}

.no-email-warning :deep(.el-alert__content) {
  margin-top: 0;
}

.add-email-section {
  border-top: 1px solid var(--el-border-color-light);
  padding-top: 24px;
}

.add-email-section h2 {
  margin: 0 0 16px 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.add-email-form {
  max-width: 400px;
}

.add-email-form :deep(.el-form-item__label) {
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .email-manage-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .email-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .button-holder {
    flex-direction: column;
  }
  
  .button-holder .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .email-badges {
    justify-content: flex-start;
  }
  
  .add-email-form {
    max-width: 100%;
  }
}
</style>
