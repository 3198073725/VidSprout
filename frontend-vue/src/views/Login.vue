<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { AuthAPI } from '@/api'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  username: '',
  password: '',
  rememberMe: false,
  captcha: '',
  captchaSessionKey: ''
})

const rules = {
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

const captchaImage = ref('')
const showCaptcha = ref(false)
const passwordStrength = ref<'weak' | 'medium' | 'strong' | ''>('')
const passwordStrengthMessage = ref('')
const loginLoading = ref(false)
const remainingAttempts = ref<number | null>(null)
const accountLocked = ref(false)
const lockoutRemainingTime = ref(0)

// 密码强度检查
const checkPasswordStrength = (password: string) => {
  if (!password) {
    passwordStrength.value = ''
    passwordStrengthMessage.value = ''
    return
  }

  let score = 0
  const patterns = {
    length: password.length >= 8,
    uppercase: /[A-Z]/.test(password),
    lowercase: /[a-z]/.test(password),
    numbers: /\d/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
  }

  Object.values(patterns).forEach(met => {
    if (met) score++
  })

  if (password.length < 6) {
    passwordStrength.value = 'weak'
    passwordStrengthMessage.value = '密码太短'
  } else if (score <= 2) {
    passwordStrength.value = 'weak'
    passwordStrengthMessage.value = '密码强度：弱'
  } else if (score <= 4) {
    passwordStrength.value = 'medium'
    passwordStrengthMessage.value = '密码强度：中等'
  } else {
    passwordStrength.value = 'strong'
    passwordStrengthMessage.value = '密码强度：强'
  }
}

// 获取验证码
const getCaptcha = async () => {
  try {
    const response = await AuthAPI.getCaptcha()
    captchaImage.value = response.captchaImage
    form.captchaSessionKey = response.sessionKey
  } catch (error) {
    console.error('获取验证码失败:', error)
    ElMessage.error('获取验证码失败')
  }
}

// 刷新验证码
const refreshCaptcha = () => {
  getCaptcha()
}

// 监听密码变化
const handlePasswordChange = (value: string) => {
  checkPasswordStrength(value)
}

// 登录处理
async function onSubmit() {
  if (!form.username) {
    ElMessage.error('请输入用户名')
    return
  }
  if (!form.password) {
    ElMessage.error('请输入密码')
    return
  }
  
  // 如果需要验证码但未输入
  if (showCaptcha.value && !form.captcha) {
    ElMessage.error('请输入验证码')
    return
  }

  loginLoading.value = true
  
  try {
    // 登录并等待 profile 加载完成
    await auth.login({
      username: form.username,
      password: form.password,
      rememberMe: form.rememberMe,
      captcha: form.captcha || undefined,
      captchaSessionKey: form.captchaSessionKey || undefined,
    })
    
    // 确保 profile 已加载
    if (!auth.profile) {
      console.warn('Profile not loaded after login, fetching...')
      await auth.fetchProfile()
    }
    
    ElMessage.success('登录成功')
    
    // 跳转到首页
    await router.push('/')
  } catch (e: any) {
    console.error('Login error:', e)
    const errorData = e?.response?.data
    const errorMessage = e?.message || '登录失败'
    
    // 处理后端返回的错误信息
    if (errorData?.non_field_errors) {
      const errors = errorData.non_field_errors
      if (errors.some((err: string) => err.includes('封禁') || err.includes('deactivated'))) {
        ElMessage.error({
          message: '您的账号已被封禁，请联系管理员',
          duration: 5000,
          type: 'error'
        })
      } else if (errors.some((err: string) => err.includes('不存在') || err.includes('User not found') || err.includes('该账号不存在'))) {
        ElMessage.error('该账号不存在，请先注册')
      } else if (errors.some((err: string) => err.includes('密码错误') || err.includes('password'))) {
        ElMessage.error('密码错误，请重试')
      } else if (errors.some((err: string) => err.includes('验证码'))) {
        ElMessage.error('验证码错误')
        form.captcha = ''
        refreshCaptcha()
      } else if (errors.some((err: string) => err.includes('锁定'))) {
        // 账户被锁定
        accountLocked.value = true
        const lockoutMatch = errors[0].match(/(\d+)\s*分钟/)
        if (lockoutMatch) {
          lockoutRemainingTime.value = parseInt(lockoutMatch[1]) * 60
          startLockoutCountdown()
        }
        ElMessage.error(errors[0])
      } else if (errors.some((err: string) => err.includes('需要验证码'))) {
        // 需要验证码
        showCaptcha.value = true
        ElMessage.error('请输入验证码')
        await getCaptcha()
      } else {
        ElMessage.error(errors[0] || '登录失败')
      }
    } else if (errorData?.detail) {
      if (errorData.detail.includes('需要验证码')) {
        showCaptcha.value = true
        ElMessage.error('请输入验证码')
        await getCaptcha()
      } else if (errorData.detail.includes('锁定')) {
        accountLocked.value = true
        const lockoutMatch = errorData.detail.match(/(\d+)\s*分钟/)
        if (lockoutMatch) {
          lockoutRemainingTime.value = parseInt(lockoutMatch[1]) * 60
          startLockoutCountdown()
        }
        ElMessage.error(errorData.detail)
      } else {
        ElMessage.error(errorData.detail)
      }
    } else if (errorMessage.includes('not found') || errorMessage.includes('不存在')) {
      ElMessage.error('用户不存在，请先注册')
    } else if (errorMessage.includes('credentials') || errorMessage.includes('password') || errorMessage.includes('密码')) {
      // 用户名或密码错误，可能需要显示剩余尝试次数
      remainingAttempts.value = 3 // 这里应该从后端获取实际值
      ElMessage.error('用户名或密码错误')
    } else {
      ElMessage.error('登录失败，请检查用户名和密码')
    }
    
    // 登录失败后刷新验证码
    if (showCaptcha.value) {
      await getCaptcha()
    }
  } finally {
    loginLoading.value = false
  }
}

// 锁定倒计时
const startLockoutCountdown = () => {
  const interval = setInterval(() => {
    if (lockoutRemainingTime.value > 0) {
      lockoutRemainingTime.value--
    } else {
      accountLocked.value = false
      clearInterval(interval)
    }
  }, 1000)
}

// 格式化剩余时间
const formatLockoutTime = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

// 组件挂载时检查是否需要验证码
onMounted(async () => {
  // 这里可以根据IP地址或用户名检查是否需要显示验证码
  // 暂时不自动获取验证码，只有在需要时才获取
})
</script>

<template>
  <div class="user-action-form-wrap">
    <div class="user-action-form-inner">
      <h1>登录</h1>
      <p>如果您还没有创建账户，请先 <router-link to="/register">注册</router-link>。</p>
      
      <!-- 账户锁定提示 -->
      <div v-if="accountLocked" class="lockout-warning">
        <el-alert
          :title="`账户被锁定，剩余时间：${formatLockoutTime(lockoutRemainingTime)}`"
          type="error"
          :closable="false"
        />
      </div>
      
      <el-form :model="form" :rules="rules" @submit.prevent label-position="top">
        <el-form-item label="登录:">
          <el-input 
            v-model="form.username" 
            :disabled="accountLocked"
            placeholder="请输入用户名或邮箱"
          />
        </el-form-item>
        
        <el-form-item label="密码:" prop="password">
          <el-input 
            v-model="form.password" 
            type="password" 
            show-password
            :disabled="accountLocked"
            placeholder="请输入密码"
            @input="handlePasswordChange"
          />
        </el-form-item>
        
        <!-- 密码强度指示器 -->
        <div v-if="passwordStrength" class="password-strength">
          <el-alert
            :title="passwordStrengthMessage"
            :type="passwordStrength === 'weak' ? 'error' : passwordStrength === 'medium' ? 'warning' : 'success'"
            :closable="false"
          />
        </div>
        
        <!-- 验证码输入 -->
        <el-form-item v-if="showCaptcha" label="验证码:">
          <div class="captcha-container">
            <el-input 
              v-model="form.captcha" 
              placeholder="请输入验证码"
              :disabled="accountLocked"
            />
            <div class="captcha-image" @click="refreshCaptcha">
              <img :src="captchaImage" alt="验证码" />
              <span class="refresh-hint">点击刷新</span>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="form.rememberMe" label="记住我" size="default" :disabled="accountLocked">
            记住我 (30天内自动登录)
          </el-checkbox>
        </el-form-item>
        
        <div style="margin-bottom: 16px">
          <router-link to="/password-reset" style="color: #2ecc71; text-decoration: none; font-size: 14px">忘记密码?</router-link>
        </div>
        
        <el-form-item>
          <el-button 
            type="success" 
            :loading="auth.loading || loginLoading" 
            @click="onSubmit" 
            style="padding: 12px 32px"
            :disabled="accountLocked"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.lockout-warning {
  margin-bottom: 20px;
}

.password-strength {
  margin-bottom: 16px;
}

.captcha-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.captcha-image {
  cursor: pointer;
  position: relative;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.captcha-image img {
  height: 40px;
  display: block;
}

.refresh-hint {
  position: absolute;
  bottom: 2px;
  right: 4px;
  font-size: 10px;
  color: #909399;
  background: rgba(255, 255, 255, 0.8);
  padding: 2px 4px;
  border-radius: 2px;
}

.captcha-image:hover .refresh-hint {
  color: #2ecc71;
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .refresh-hint {
  background: rgba(26, 26, 26, 0.9);
  color: #999;
}

[data-theme="dark"] .captcha-image:hover .refresh-hint {
  color: #2ecc71;
}
</style>
