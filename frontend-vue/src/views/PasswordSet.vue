<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const loading = ref(false)
const passwordForm = ref({
  password1: '',
  password2: ''
})

// 表单验证规则
const passwordRules = {
  password1: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' },
    { 
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      message: '密码必须包含大小写字母和数字',
      trigger: 'blur'
    }
  ],
  password2: [
    { required: true, message: '请确认密码', trigger: 'blur' },
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

async function setPassword() {
  if (passwordForm.value.password1 !== passwordForm.value.password2) {
    ElMessage.error('两次输入的密码不一致')
    return
  }
  
  loading.value = true
  try {
    // 这里应该调用设置密码API
    // await AuthAPI.setPassword({
    //   password: passwordForm.value.password1
    // })
    
    ElMessage.success('密码设置成功')
    router.push('/login')
  } catch (error) {
    console.error('设置密码失败:', error)
    ElMessage.error('设置密码失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="password-set-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>设置密码</h1>
        
        <div class="password-set-content">
          <p class="form-description">
            请为您的账户设置一个安全的密码。密码将用于保护您的账户安全。
          </p>
          
          <!-- 对应后端模板的表单 -->
          <el-form 
            :model="passwordForm" 
            :rules="passwordRules"
            label-width="100px"
            @submit.prevent="setPassword"
          >
            <el-form-item label="新密码" prop="password1" required>
              <el-input
                v-model="passwordForm.password1"
                type="password"
                placeholder="输入新密码"
                show-password
                :disabled="loading"
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
                :disabled="loading"
              />
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                :loading="loading"
                @click="setPassword"
                style="width: 100%"
                size="large"
              >
                {{ loading ? '正在设置...' : '设置密码' }}
              </el-button>
            </el-form-item>
          </el-form>
          
          <!-- 密码安全建议 -->
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
              <div class="tip-item">
                <el-icon class="tip-icon"><Check /></el-icon>
                <span>不要使用个人信息</span>
              </div>
            </div>
          </el-card>
          
          <!-- 安全提醒 -->
          <el-card class="security-reminder" shadow="never">
            <template #header>
              <h3>安全提醒</h3>
            </template>
            
            <div class="reminder-content">
              <div class="reminder-item">
                <el-icon class="reminder-icon"><Lock /></el-icon>
                <div class="reminder-text">
                  <strong>保护您的密码</strong>
                  <p>请不要与他人分享您的密码，包括客服人员。</p>
                </div>
              </div>
              
              <div class="reminder-item">
                <el-icon class="reminder-icon"><Shield /></el-icon>
                <div class="reminder-text">
                  <strong>定期更换</strong>
                  <p>建议您定期更换密码以保持账户安全。</p>
                </div>
              </div>
              
              <div class="reminder-item">
                <el-icon class="reminder-icon"><Key /></el-icon>
                <div class="reminder-text">
                  <strong>使用密码管理器</strong>
                  <p>考虑使用密码管理器来生成和存储强密码。</p>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 帮助信息 -->
          <div class="help-section">
            <el-alert
              title="需要帮助？"
              type="info"
              :closable="false"
            >
              <p>如果您在设置密码过程中遇到任何问题，请联系我们的客服团队。</p>
              <div class="help-actions">
                <el-button size="small" @click="router.push('/contact')">
                  联系客服
                </el-button>
                <el-button size="small" @click="router.push('/login')">
                  返回登录
                </el-button>
              </div>
            </el-alert>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.password-set-container {
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

.password-set-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-description {
  text-align: center;
  color: var(--mc-text-secondary);
  margin-bottom: 8px;
  line-height: 1.5;
}

.password-help {
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
  margin-top: 4px;
  line-height: 1.4;
}

.password-tips,
.security-reminder {
  margin-top: 8px;
}

.password-tips :deep(.el-card__header),
.security-reminder :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.password-tips :deep(.el-card__header h3),
.security-reminder :deep(.el-card__header h3) {
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

.reminder-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reminder-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.reminder-icon {
  font-size: 18px;
  color: var(--el-color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.reminder-text {
  flex: 1;
}

.reminder-text strong {
  display: block;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin-bottom: 4px;
}

.reminder-text p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
}

.help-section {
  margin-top: 8px;
}

.help-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .password-set-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .user-action-form-inner h1 {
    font-size: 1.5rem;
  }
  
  .reminder-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
  }
  
  .help-actions {
    flex-direction: column;
  }
  
  .help-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .tip-item {
    font-size: 0.85rem;
  }
  
  .reminder-text strong {
    font-size: 0.95rem;
  }
  
  .reminder-text p {
    font-size: 0.85rem;
  }
}
</style>
