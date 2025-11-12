<template>
  <div class="sidebar-container">
    <!-- Logo -->
    <div class="sidebar-logo">
      <el-icon v-if="!appStore.sidebarCollapsed" :size="32" color="#409eff">
        <VideoPlay />
      </el-icon>
      <h1 v-if="!appStore.sidebarCollapsed">MediaCMS</h1>
    </div>

    <!-- 菜单 -->
    <el-scrollbar class="sidebar-menu-wrapper">
      <el-menu
        :default-active="activeMenu"
        :collapse="appStore.sidebarCollapsed"
        :unique-opened="true"
        router
        background-color="#001529"
        text-color="#ffffff"
        active-text-color="#409eff"
      >
        <template v-for="route in menuRoutes" :key="route.path">
          <!-- 有子菜单 -->
          <el-sub-menu v-if="route.children && route.children.length > 0" :index="route.fullPath">
            <template #title>
              <el-icon v-if="route.meta?.icon">
                <component :is="route.meta.icon" />
              </el-icon>
              <span>{{ route.meta?.title }}</span>
            </template>
            <el-menu-item
              v-for="child in route.children"
              :key="child.path"
              :index="child.fullPath"
            >
              {{ child.meta?.title }}
            </el-menu-item>
          </el-sub-menu>

          <!-- 无子菜单 -->
          <el-menu-item v-else :index="route.fullPath">
            <el-icon v-if="route.meta?.icon">
              <component :is="route.meta.icon" />
            </el-icon>
            <template #title>{{ route.meta?.title }}</template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'

const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

// 获取菜单路由（构建带完整路径的菜单数据）
const menuRoutes = computed(() => {
  const routes = router.getRoutes()
  const mainRoute = routes.find(r => r.path === '/')
  if (!mainRoute || !mainRoute.children) return []
  
  return mainRoute.children
    .filter(r => !r.meta?.hidden)
    .map(route => ({
      ...route,
      // 确保路径以 / 开头
      fullPath: route.path.startsWith('/') ? route.path : `/${route.path}`,
      children: route.children?.filter(c => !c.meta?.hidden).map(child => ({
        ...child,
        // 构建完整的子路由路径
        fullPath: child.path.startsWith('/') 
          ? child.path 
          : `/${route.path}/${child.path}`
      }))
    }))
})

// 当前激活的菜单
const activeMenu = computed(() => {
  const { path } = route
  return path
})
</script>

<style scoped lang="scss">
.sidebar-container {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 0 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  h1 {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
    margin: 0;
  }
}

.sidebar-menu-wrapper {
  flex: 1;
  overflow-x: hidden;
}

.el-menu {
  border-right: none;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  height: 50px;
  line-height: 50px;
}

// 悬停效果
:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  background-color: rgba(64, 158, 255, 0.15) !important;
}

// 激活的菜单项（叶子节点）
:deep(.el-menu-item.is-active) {
  background-color: #409eff !important;
  color: #ffffff !important;
}

// 子菜单容器
:deep(.el-menu--inline) {
  background-color: rgba(0, 0, 0, 0.3) !important;
}

// 子菜单项
:deep(.el-menu--inline .el-menu-item) {
  padding-left: 50px !important;
  background-color: transparent !important;
}

// 子菜单项悬停
:deep(.el-menu--inline .el-menu-item:hover) {
  background-color: rgba(64, 158, 255, 0.15) !important;
}

// 子菜单项激活
:deep(.el-menu--inline .el-menu-item.is-active) {
  background-color: #409eff !important;
  color: #ffffff !important;
}

// 展开的子菜单标题（不要高亮父菜单）
:deep(.el-sub-menu.is-opened > .el-sub-menu__title) {
  background-color: transparent !important;
}
</style>

