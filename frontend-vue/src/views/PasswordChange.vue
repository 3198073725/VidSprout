<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import http from '@/services/http'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const form = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const rules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string, callback: Function) => {
        if (value !== form.value.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function changePassword() {
  if (!form.value.old_password || !form.value.new_password || !form.value.confirm_password) {
    ElMessage.warning('请填写完整信息')
    return
  }

  if (form.value.new_password !== form.value.confirm_password) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }

  if (form.value.new_password.length < 6) {
    ElMessage.warning('新密码长度至少6位')
    return
  }

  loading.value = true
  try {
    await http.post('/v1/user/password/change', {
      old_password: form.value.old_password,
      new_password: form.value.new_password
    })
    
    ElMessage.success('密码修改成功，请重新登录')
    
    // 清除登录状态，跳转到登录页
    auth.logout()
    router.push('/login')
  } catch (error: any) {
    const message = error.message || '密码修改失败'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

function resetForm() {
  form.value = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  }
}
</script>

<template>
  <div class="password-change-container">
    <el-card class="password-change-card">
      <template #header>
        <div class="card-header">
          <h2>修改密码</h2>
          <el-button @click="router.back()">返回</el-button>
        </div>
      </template>

      <el-form
        :model="form"
        :rules="rules"
        label-width="120px"
        @submit.prevent="changePassword"
      >
        <el-form-item label="当前密码" prop="old_password">
          <el-input
            v-model="form.old_password"
            type="password"
            placeholder="请输入当前密码"
            show-password
            autocomplete="current-password"
          />
        </el-form-item>

        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="form.new_password"
            type="password"
            placeholder="请输入新密码（至少6位）"
            show-password
            autocomplete="new-password"
          />
        </el-form-item>

        <el-form-item label="确认新密码" prop="confirm_password">
          <el-input
            v-model="form.confirm_password"
            type="password"
            placeholder="请再次输入新密码"
            show-password
            autocomplete="new-password"
          />
        </el-form-item>

        <el-form-item>
          <el-space>
            <el-button type="primary" :loading="loading" @click="changePassword">
              修改密码
            </el-button>
            <el-button @click="resetForm">重置</el-button>
            <el-button @click="router.back()">取消</el-button>
          </el-space>
        </el-form-item>
      </el-form>

      <el-divider />

      <div class="password-tips">
        <h4>密码安全提示：</h4>
        <ul>
          <li>密码长度至少6位字符</li>
          <li>建议使用字母、数字和特殊字符的组合</li>
          <li>不要使用过于简单的密码</li>
          <li>定期更换密码以保证账户安全</li>
        </ul>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.password-change-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.password-change-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: var(--mc-bg-primary, #fff);
}

[data-theme="dark"] .password-change-card {
  background: #1a1a1a;
  border-color: #333;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  color: var(--mc-text-primary, #303133);
}

[data-theme="dark"] .card-header h2 {
  color: #ffffff;
}

.password-tips {
  color: var(--mc-text-secondary, #606266);
  font-size: 14px;
}

[data-theme="dark"] .password-tips {
  color: #cccccc;
}

.password-tips h4 {
  margin-bottom: 12px;
  color: var(--mc-text-primary, #303133);
}

[data-theme="dark"] .password-tips h4 {
  color: #ffffff;
}

.password-tips ul {
  margin: 0;
  padding-left: 20px;
}

.password-tips li {
  margin-bottom: 8px;
  line-height: 1.5;
}
</style>
