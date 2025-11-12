<template>
  <div class="header-container">
    <!-- 左侧 -->
    <div class="header-left">
      <el-icon class="toggle-icon" :size="20" @click="toggleSidebar">
        <Fold v-if="!appStore.sidebarCollapsed" />
        <Expand v-else />
      </el-icon>

      <!-- 面包屑 -->
      <el-breadcrumb separator="/">
        <el-breadcrumb-item v-for="item in breadcrumbs" :key="item.path" :to="item.path">
          {{ item.meta?.title }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 右侧 -->
    <div class="header-right">
      <!-- 主题切换 -->
      <el-tooltip content="切换主题" placement="bottom">
        <el-icon class="header-icon" :size="20" @click="appStore.toggleTheme">
          <Sunny v-if="appStore.theme === 'light'" />
          <Moon v-else />
        </el-icon>
      </el-tooltip>

      <!-- 全屏 -->
      <el-tooltip content="全屏" placement="bottom">
        <el-icon class="header-icon" :size="20" @click="toggleFullscreen">
          <FullScreen />
        </el-icon>
      </el-tooltip>

      <!-- 返回主站 -->
      <el-tooltip content="返回主站" placement="bottom">
        <el-button type="primary" text @click="goToMainSite">
          <el-icon><Monitor /></el-icon>
          <span style="margin-left: 4px;">主站</span>
        </el-button>
      </el-tooltip>

      <!-- 用户信息 -->
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="32" :src="authStore.profile?.logo || undefined">
            <el-icon><User /></el-icon>
          </el-avatar>
          <span class="username">{{ authStore.profile?.name || authStore.profile?.username }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>
              个人资料
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              设置
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

// 面包屑
const breadcrumbs = computed(() => {
  return route.matched.filter(r => r.meta?.title && !r.meta?.hidden)
})

// 切换侧边栏
const toggleSidebar = () => {
  appStore.toggleSidebar()
}

// 切换全屏
const toggleFullscreen = () => {
  if (document.fullscreenElement) {
    document.exitFullscreen()
  } else {
    document.documentElement.requestFullscreen()
  }
}

// 返回主站
const goToMainSite = () => {
  window.open('/', '_blank')
}

// 下拉菜单命令
const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/system/settings')
      break
    case 'logout':
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        type: 'warning'
      })
      authStore.logout()
      router.push('/login')
      break
  }
}
</script>

<style scoped lang="scss">
.header-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.toggle-icon {
  cursor: pointer;
  color: #606266;
  transition: color 0.3s;

  &:hover {
    color: #409eff;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-icon {
  cursor: pointer;
  color: #606266;
  transition: color 0.3s;

  &:hover {
    color: #409eff;
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background-color 0.3s;

  &:hover {
    background-color: var(--el-fill-color-light);
  }

  .username {
    font-size: 14px;
    color: #303133;
  }
}

[data-theme='dark'] {
  .toggle-icon,
  .header-icon {
    color: #909399;

    &:hover {
      color: #409eff;
    }
  }

  .user-info {
    .username {
      color: #ffffff;
    }
  }
}
</style>

