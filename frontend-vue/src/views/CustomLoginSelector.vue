<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedLoginMethod = ref('')
const loginOptions = ref([
  {
    url: '/login',
    title: '用户名/邮箱登录'
  },
  {
    url: '/accounts/google/login/',
    title: 'Google 登录'
  },
  {
    url: '/accounts/github/login/',
    title: 'GitHub 登录'
  },
  {
    url: '/accounts/microsoft/login/',
    title: 'Microsoft 登录'
  }
])

function updateFormAction() {
  if (!selectedLoginMethod.value) return
  
  // 根据选择的登录方式跳转
  if (selectedLoginMethod.value.includes('/accounts/login_system')) {
    // 系统登录使用GET方法
    window.location.href = selectedLoginMethod.value
  } else {
    // 其他登录方式
    router.push(selectedLoginMethod.value)
  }
}

// 自动提交表单
function handleLoginMethodChange() {
  if (selectedLoginMethod.value) {
    updateFormAction()
  }
}

onMounted(() => {
  // 可以从API加载登录选项
  // loadLoginOptions()
})
</script>

<template>
  <div class="custom-login-selector-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的登录容器 -->
        <div class="login-container">
          
          <!-- 对应后端模板的登录头部 -->
          <div class="login-header">
            <h1>登录</h1>
            <p>请选择您偏好的登录方式</p>
          </div>

          <!-- 对应后端模板的表单 -->
          <form id="loginForm" @submit.prevent="handleLoginMethodChange">
            
            <!-- 对应后端模板的选择容器 -->
            <div class="login-select-container">
              <el-select
                v-model="selectedLoginMethod"
                placeholder="选择登录方式..."
                class="login-select"
                @change="handleLoginMethodChange"
              >
                <el-option
                  v-for="option in loginOptions"
                  :key="option.url"
                  :label="option.title"
                  :value="option.url"
                />
              </el-select>
            </div>

          </form>

          <!-- 直接登录链接 -->
          <div class="login-direct-links">
            <el-button 
              v-for="option in loginOptions" 
              :key="option.url"
              class="login-option-button"
              @click="selectedLoginMethod = option.url; handleLoginMethodChange()"
            >
              {{ option.title }}
            </el-button>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-login-selector-container {
  max-width: 500px;
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

/* 对应后端模板的 login-container 样式 */
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 对应后端模板的 login-header 样式 */
.login-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.login-header h1 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #666;
  font-size: 0.9rem;
}

/* 对应后端模板的 login-select-container 样式 */
.login-select-container {
  position: relative;
  margin-bottom: 1.5rem;
}

/* 对应后端模板的 login-select 样式 */
.login-select {
  width: 100%;
}

.login-select :deep(.el-input__wrapper) {
  padding: 12px 16px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  background-color: #f9f9f9;
}

.login-select :deep(.el-input__wrapper):focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
}

/* 直接登录链接样式 */
.login-direct-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 20px;
}

/* 对应后端模板的 login-button 样式 */
.login-option-button {
  width: 100%;
  padding: 12px 0;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-option-button:hover {
  background-color: #3a7bc8;
}

/* 特殊登录方式的样式 */
.login-option-button:nth-child(2) {
  background-color: #db4437;
}

.login-option-button:nth-child(2):hover {
  background-color: #c23321;
}

.login-option-button:nth-child(3) {
  background-color: #333;
}

.login-option-button:nth-child(3):hover {
  background-color: #24292e;
}

.login-option-button:nth-child(4) {
  background-color: #0078d4;
}

.login-option-button:nth-child(4):hover {
  background-color: #106ebe;
}

/* 对应后端模板的 login-direct-link 样式 */
.login-direct-link {
  display: block;
  text-align: center;
  margin-top: 1rem;
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
}

.login-direct-link:hover {
  text-decoration: underline;
  color: #4a90e2;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .custom-login-selector-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .login-container {
    padding: 1.5rem;
  }
  
  .login-header h1 {
    font-size: 1.3rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 1rem;
  }
  
  .login-header h1 {
    font-size: 1.2rem;
  }
  
  .login-header p {
    font-size: 0.85rem;
  }
  
  .login-option-button {
    font-size: 0.9rem;
    padding: 10px 0;
  }
}
</style>
