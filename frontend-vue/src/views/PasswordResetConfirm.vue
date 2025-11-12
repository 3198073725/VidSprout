<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const submitting = ref(false)
const tokenValid = ref(true)
const passwordChanged = ref(false)

// 密码表单数据
const passwordForm = ref({
  password1: '',
  password2: ''
})

// 从URL获取重置token
const resetToken = computed(() => String(route.params.token || route.query.token || ''))

// 表单验证规则
const passwordRules = {
  password1: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' },
    { 
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    }
  ],
  password2: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== passwordForm.value.password1) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function validateToken() {
  if (!resetToken.value) {
    tokenValid.value = false
    return
  }
  
  loading.value = true
  try {
    // 这里应该调用验证token的API
    // const isValid = await AuthAPI.validateResetToken(resetToken.value)
    // tokenValid.value = isValid
    
    // 模拟验证
    tokenValid.value = true
  } catch (error) {
    console.error('验证token失败:', error)
    tokenValid.value = false
  } finally {
    loading.value = false
  }
}

async function submitPasswordReset() {
  if (passwordForm.value.password1 !== passwordForm.value.password2) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  submitting.value = true
  try {
    // 这里应该调用重置密码API
    // await AuthAPI.confirmPasswordReset({
    //   token: resetToken.value,
    //   password: passwordForm.value.password1
    // })
    
    passwordChanged.value = true
    ElMessage.success('密码重置成功')
    
    // 3秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (error) {
    console.error('重置密码失败:', error)
    ElMessage.error('重置密码失败，请重试')
  } finally {
    submitting.value = false
  }
}

function requestNewReset() {
  router.push('/password-reset')
}

onMounted(validateToken)
</script>

<template>
  <div class="password-reset-confirm-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="4" animated />
        </div>
        
        <!-- 对应后端模板的 {% if token_fail %} 条件 -->
        <div v-else-if="!tokenValid" class="token-fail">
          <!-- 对应后端模板的标题 -->
          <h1>无效的重置链接</h1>
          
          <!-- 对应后端模板的错误信息 -->
          <el-result
            icon="error"
            title="重置链接无效"
            sub-title="密码重置链接无效，可能是因为它已经被使用过了。"
          >
            <template #extra>
              <el-button type="primary" @click="requestNewReset">
                申请新的密码重置
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
              <li>重置链接已过期（通常24小时内有效）</li>
              <li>重置链接已经被使用过</li>
              <li>链接地址不完整或被修改</li>
            </ul>
          </el-alert>
        </div>
        
        <!-- 对应后端模板的 {% else %} 正常重置流程 -->
        <div v-else class="reset-form-section">
          <!-- 对应后端模板的 {% if form %} 显示表单 -->
          <div v-if="!passwordChanged" class="password-form">
            <h1>重置密码</h1>
            
            <p class="form-description">
              请输入您的新密码。密码应该足够强壮以保护您的账户安全。
            </p>
            
            <!-- 对应后端模板的表单 -->
            <el-form 
              :model="passwordForm" 
              :rules="passwordRules"
              label-width="100px"
              @submit.prevent="submitPasswordReset"
            >
              <el-form-item label="新密码" prop="password1" required>
                <el-input
                  v-model="passwordForm.password1"
                  type="password"
                  placeholder="输入新密码"
                  show-password
                  :disabled="submitting"
                />
                <div class="password-help">
                  密码必须至少8位，包含大小写字母和数字
                </div>
              </el-form-item>
              
              <el-form-item label="确认密码" prop="password2" required>
                <el-input
                  v-model="passwordForm.password2"
                  type="password"
                  placeholder="再次输入新密码"
                  show-password
                  :disabled="submitting"
                />
              </el-form-item>
              
              <el-form-item>
                <el-button 
                  type="primary" 
                  :loading="submitting"
                  @click="submitPasswordReset"
                  style="width: 100%"
                >
                  {{ submitting ? '正在重置...' : '重置密码' }}
                </el-button>
              </el-form-item>
            </el-form>
            
            <!-- 密码强度提示 -->
            <el-card class="password-tips" shadow="never">
              <template #header>
                <h3>密码安全建议</h3>
              </template>
              
              <div class="tips-list">
                <div class="tip-item">
                  <el-icon class="tip-icon"><Check /></el-icon>
                  <span>使用至少8个字符</span>
                </div>
                <div class="tip-item">
                  <el-icon class="tip-icon"><Check /></el-icon>
                  <span>包含大写和小写字母</span>
                </div>
                <div class="tip-item">
                  <el-icon class="tip-icon"><Check /></el-icon>
                  <span>包含数字</span>
                </div>
                <div class="tip-item">
                  <el-icon class="tip-icon"><Check /></el-icon>
                  <span>避免使用常见密码</span>
                </div>
              </div>
            </el-card>
          </div>
          
          <!-- 对应后端模板的 {% else %} 密码已更改 -->
          <div v-else class="password-changed">
            <h1>密码重置成功</h1>
            
            <el-result
              icon="success"
              title="密码已成功重置"
              sub-title="您的密码已经更新。现在可以使用新密码登录系统。"
            >
              <template #extra>
                <div class="success-actions">
                  <el-button type="primary" @click="router.push('/login')">
                    立即登录
                  </el-button>
                  <el-button @click="router.push('/')">
                    返回首页
                  </el-button>
                </div>
              </template>
            </el-result>
            
            <el-alert
              title="安全提醒"
              type="success"
              :closable="false"
              show-icon
            >
              <p>为了您的账户安全，建议您：</p>
              <ul>
                <li>立即使用新密码登录</li>
                <li>不要与他人分享您的密码</li>
                <li>定期更换密码</li>
                <li>如发现异常活动，请及时联系客服</li>
              </ul>
            </el-alert>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.password-reset-confirm-container {
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

.token-fail {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.token-fail :deep(.el-alert__content) {
  margin-top: 0;
}

.token-fail ul {
  margin: 8px 0;
  padding-left: 20px;
}

.token-fail li {
  margin-bottom: 4px;
}

.reset-form-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-description {
  text-align: center;
  color: var(--mc-text-secondary);
  margin-bottom: 24px;
  line-height: 1.5;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.password-help {
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
  margin-top: 4px;
  line-height: 1.4;
}

.password-tips {
  margin-top: 8px;
}

.password-tips :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.password-tips :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.tips-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
}

.tip-icon {
  color: var(--el-color-success);
  font-size: 16px;
}

.password-changed {
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

.password-changed :deep(.el-alert__content) {
  margin-top: 0;
}

.password-changed ul {
  margin: 8px 0;
  padding-left: 20px;
}

.password-changed li {
  margin-bottom: 4px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .password-reset-confirm-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .user-action-form-inner h1 {
    font-size: 1.5rem;
  }
  
  .success-actions {
    flex-direction: column;
  }
  
  .success-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .tip-item {
    font-size: 0.85rem;
  }
  
  .form-description {
    font-size: 0.9rem;
  }
}
</style>
