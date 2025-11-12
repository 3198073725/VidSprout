<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import http from '@/services/http'

const router = useRouter()

const loading = ref(false)
const emailSent = ref(false)
const form = ref({
  email: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ]
}

async function sendResetEmail() {
  if (!form.value.email) {
    ElMessage.warning('请输入邮箱地址')
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.value.email)) {
    ElMessage.warning('请输入有效的邮箱地址')
    return
  }

  loading.value = true
  try {
    await http.post('/v1/auth/password/reset', {
      email: form.value.email
    })
    
    emailSent.value = true
    ElMessage.success('重置邮件已发送，请检查您的邮箱')
  } catch (error: any) {
    const message = error.message || '发送失败，请稍后重试'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push('/login')
}

function resetForm() {
  form.value.email = ''
  emailSent.value = false
}
</script>

<template>
  <div class="password-reset-container">
    <el-card class="password-reset-card">
      <template #header>
        <div class="card-header">
          <h2>重置密码</h2>
        </div>
      </template>

      <div v-if="!emailSent" class="reset-form">
        <p class="description">
          请输入您的邮箱地址，我们将向您发送密码重置链接。
        </p>

        <el-form
          :model="form"
          :rules="rules"
          label-width="80px"
          @submit.prevent="sendResetEmail"
        >
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="form.email"
              type="email"
              placeholder="请输入您的邮箱地址"
              autocomplete="email"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-space>
              <el-button type="primary" :loading="loading" @click="sendResetEmail">
                发送重置邮件
              </el-button>
              <el-button @click="goToLogin">返回登录</el-button>
            </el-space>
          </el-form-item>
        </el-form>
      </div>

      <div v-else class="success-message">
        <div class="success-icon">
          <el-icon size="64" color="#67c23a"><CircleCheck /></el-icon>
        </div>
        <h3>邮件已发送</h3>
        <p>
          我们已向 <strong>{{ form.email }}</strong> 发送了密码重置邮件。
          <br>
          请检查您的邮箱（包括垃圾邮件文件夹），并点击邮件中的链接来重置密码。
        </p>
        
        <div class="action-buttons">
          <el-button type="primary" @click="goToLogin">返回登录</el-button>
          <el-button @click="resetForm">重新发送</el-button>
        </div>
      </div>

      <el-divider />

      <div class="help-info">
        <h4>需要帮助？</h4>
        <ul>
          <li>如果您没有收到邮件，请检查垃圾邮件文件夹</li>
          <li>重置链接有效期为24小时</li>
          <li>如果仍有问题，请联系管理员</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.password-reset-container {
  max-width: 500px;
  margin: 50px auto;
  padding: 20px;
}

.password-reset-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
}

.description {
  color: #606266;
  margin-bottom: 24px;
  line-height: 1.6;
}

.success-message {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  margin-bottom: 16px;
}

.success-message h3 {
  color: #67c23a;
  margin-bottom: 16px;
}

.success-message p {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 24px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.help-info {
  color: #909399;
  font-size: 14px;
}

.help-info h4 {
  margin-bottom: 12px;
  color: #606266;
}

.help-info ul {
  margin: 0;
  padding-left: 20px;
}

.help-info li {
  margin-bottom: 8px;
  line-height: 1.5;
}
</style>
