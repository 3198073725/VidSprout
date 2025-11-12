<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { onMounted, ref } from 'vue'

const auth = useAuthStore()
const tokenInStorage = ref('')
const profileData = ref('')

onMounted(() => {
  tokenInStorage.value = localStorage.getItem('token') || '无'
  if (auth.profile) {
    profileData.value = JSON.stringify(auth.profile, null, 2)
  }
})

async function refreshProfile() {
  await auth.fetchProfile()
  if (auth.profile) {
    profileData.value = JSON.stringify(auth.profile, null, 2)
  }
}
</script>

<template>
  <div style="padding: 20px; max-width: 800px; margin: 0 auto;">
    <h1>登录状态调试</h1>
    
    <el-card style="margin-bottom: 16px;">
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>认证状态</span>
          <el-button type="primary" size="small" @click="refreshProfile">刷新Profile</el-button>
        </div>
      </template>
      
      <el-descriptions :column="1" border>
        <el-descriptions-item label="是否登录">
          <el-tag :type="auth.isLoggedIn ? 'success' : 'danger'">
            {{ auth.isLoggedIn ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="是否初始化">
          <el-tag :type="auth.isInitialized ? 'success' : 'warning'">
            {{ auth.isInitialized ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="是否管理员">
          <el-tag :type="auth.isAdmin ? 'success' : 'info'">
            {{ auth.isAdmin ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="加载状态">
          <el-tag :type="auth.loading ? 'warning' : 'info'">
            {{ auth.loading ? '加载中' : '空闲' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <el-card style="margin-bottom: 16px;">
      <template #header>Token 信息</template>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="Store 中的 Token">
          <code style="word-break: break-all;">{{ auth.token || '无' }}</code>
        </el-descriptions-item>
        <el-descriptions-item label="LocalStorage 中的 Token">
          <code style="word-break: break-all;">{{ tokenInStorage }}</code>
        </el-descriptions-item>
        <el-descriptions-item label="Token 是否一致">
          <el-tag :type="auth.token === tokenInStorage ? 'success' : 'danger'">
            {{ auth.token === tokenInStorage ? '一致' : '不一致' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    
    <el-card style="margin-bottom: 16px;">
      <template #header>用户信息 (Profile)</template>
      <div v-if="auth.profile">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="用户名">{{ auth.profile.username }}</el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ auth.profile.email_is_verified ? '✓ 已验证' : '✗ 未验证' }}</el-descriptions-item>
          <el-descriptions-item label="姓名">{{ auth.profile.name || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ auth.profile.description || '未设置' }}</el-descriptions-item>
          <el-descriptions-item label="高级用户">{{ auth.profile.advancedUser ? '是' : '否' }}</el-descriptions-item>
          <el-descriptions-item label="编辑权限">{{ auth.profile.is_editor ? '是' : '否' }}</el-descriptions-item>
          <el-descriptions-item label="管理权限">{{ auth.profile.is_manager ? '是' : '否' }}</el-descriptions-item>
          <el-descriptions-item label="特色用户">{{ auth.profile.is_featured ? '是' : '否' }}</el-descriptions-item>
        </el-descriptions>
        
        <el-divider>完整数据 (JSON)</el-divider>
        <pre style="background: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto;">{{ profileData }}</pre>
      </div>
      <el-empty v-else description="用户信息未加载" />
    </el-card>
    
    <el-card>
      <template #header>操作</template>
      <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <el-button @click="auth.fetchProfile()">重新获取用户信息</el-button>
        <el-button type="danger" @click="auth.logout(); $router.push('/login')">登出</el-button>
        <el-button @click="$router.push('/')">返回首页</el-button>
      </div>
    </el-card>
  </div>
</template>
