<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUiStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'
import ThemeToggle from './ThemeToggle.vue'

const router = useRouter()
const keyword = ref('')
const ui = useUiStore()
const auth = useAuthStore()

function goSearch() {
  router.push({ name: 'search', query: { q: keyword.value } })
}
</script>

<template>
  <header class="mc-header">
    <div class="mc-header-left">
      <button class="mc-menu-btn" aria-label="menu" @click="ui.toggleSidebar()">
        <el-icon><Menu /></el-icon>
      </button>
      <router-link class="mc-logo" to="/">
        <span>Media</span><span class="mc-logo-accent">CMS</span>
      </router-link>
    </div>
    <div class="mc-search">
      <el-input v-model="keyword" placeholder="搜索" @keyup.enter="goSearch" style="max-width: 640px">
        <template #append>
          <el-button @click="goSearch"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
    </div>
    <nav class="mc-header-actions">
      <!-- 主题切换 -->
      <ThemeToggle />
      
      <template v-if="auth.isLoggedIn">
        <el-dropdown trigger="click">
          <el-button type="success">
            <el-icon style="margin-right: 4px"><VideoCamera /></el-icon>
            创建 <el-icon><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="router.push('/upload')">
                <el-icon><Upload /></el-icon>
                上传媒体
              </el-dropdown-item>
              <el-dropdown-item @click="router.push('/screen-record')">
                <el-icon><Monitor /></el-icon>
                屏幕录制
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-dropdown trigger="click">
          <el-avatar :src="auth.profile?.thumbnail_url || 'http://localhost/media/userlogos/user.jpg'" :size="40" style="cursor: pointer" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item disabled>
                <strong>{{ auth.profile?.username || '用户' }}</strong>
              </el-dropdown-item>
              <el-dropdown-item divided @click="auth.profile?.username && router.push(`/user/${auth.profile.username}`)">
                <el-icon><VideoCamera /></el-icon>
                我的媒体
              </el-dropdown-item>
              <el-dropdown-item @click="auth.logout()">
                <el-icon><SwitchButton /></el-icon>
                登出
              </el-dropdown-item>
              <el-dropdown-item divided @click="auth.profile?.username && router.push(`/user/${auth.profile.username}/edit`)">
                <el-icon><Edit /></el-icon>
                编辑个人资料
              </el-dropdown-item>
              <el-dropdown-item @click="router.push('/password-change')">
                <el-icon><Lock /></el-icon>
                更改密码
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-else>
        <router-link to="/login" class="mc-link">登录</router-link>
        <router-link to="/register" class="mc-link">注册</router-link>
      </template>
    </nav>
  </header>
</template>

<style scoped>
.mc-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  height: 64px;
  background: var(--el-bg-color);
  border-bottom: 1px solid var(--el-border-color-light);
  position: sticky;
  top: 0;
  z-index: 1000;
  gap: 16px;
}

.mc-menu-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
  color: var(--el-text-color-primary);
  transition: background-color 0.2s;
}

.mc-menu-btn:hover {
  background: var(--el-fill-color-light);
}

.mc-logo {
  font-size: 24px;
  font-weight: 600;
  text-decoration: none;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.mc-logo-accent {
  color: var(--el-color-primary);
}

.mc-search {
  flex: 1;
  max-width: 640px;
  margin: 0 24px;
}

  .mc-header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mc-header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  white-space: nowrap;
}

.mc-link {
  color: var(--el-text-color-primary);
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.mc-link:hover {
  background: var(--el-fill-color-light);
}
</style>
