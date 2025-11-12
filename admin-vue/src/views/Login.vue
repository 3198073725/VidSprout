<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo">
          <el-icon :size="48" color="#409eff"><VideoPlay /></el-icon>
        </div>
        <h1>MediaCMS 管理后台</h1>
        <p>欢迎登录</p>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            size="large"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            clearable
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            {{ loading ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <el-text type="info" size="small">
          MediaCMS v1.0 © 2024
        </el-text>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const formRef = ref<FormInstance>()
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    loading.value = true
    try {
      await authStore.login(form.username, form.password)
      
      // 调试：打印用户信息
      console.log('登录成功，用户信息:', authStore.profile)
      console.log('是否是管理员:', authStore.isAdmin)
      
      // 检查是否有管理员权限
      if (!authStore.isAdmin) {
        console.error('权限检查失败:', {
          profile: authStore.profile,
          is_superuser: authStore.profile?.is_superuser,
          is_staff: authStore.profile?.is_staff,
          is_manager: authStore.profile?.is_manager,
          is_editor: authStore.profile?.is_editor
        })
        ElMessage.error('您没有管理后台访问权限，请联系管理员')
        authStore.logout()
        return
      }

      ElMessage.success('登录成功')
      
      // 跳转到原来要访问的页面或仪表板
      const redirect = route.query.redirect as string || '/dashboard'
      router.push(redirect)
    } catch (error: any) {
      console.error('登录失败:', error)
      ElMessage.error(error.response?.data?.detail || '登录失败，请检查用户名和密码')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped lang="scss">
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 420px;
  padding: 40px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;

  .logo {
    display: flex;
    justify-content: center;
    margin-bottom: 16px;
  }

  h1 {
    font-size: 24px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8px;
  }

  p {
    font-size: 14px;
    color: #909399;
  }
}

.login-form {
  :deep(.el-form-item) {
    margin-bottom: 24px;
  }

  .login-button {
    width: 100%;
  }
}

.login-footer {
  margin-top: 24px;
  text-align: center;
}

[data-theme='dark'] {
  .login-container {
    background: linear-gradient(135deg, #434343 0%, #000000 100%);
  }

  .login-box {
    background: #1a1a1a;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);

    h1 {
      color: #ffffff;
    }
  }
}
</style>

