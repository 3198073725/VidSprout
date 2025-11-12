<template>
  <div class="admin-layout" :class="{ 'sidebar-collapsed': appStore.sidebarCollapsed }">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <Sidebar />
    </aside>

    <!-- 主内容区 -->
    <div class="main-container">
      <!-- 顶部导航栏 -->
      <header class="header">
        <Header />
      </header>

      <!-- 内容区域 -->
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/stores/app'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'

const appStore = useAppStore()
</script>

<style scoped lang="scss">
@import '@/styles/variables.scss';

.admin-layout {
  display: flex;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.sidebar {
  width: $sidebar-width;
  height: 100%;
  background: #001529;
  transition: width 0.3s;
  flex-shrink: 0;
}

.sidebar-collapsed .sidebar {
  width: $sidebar-collapsed-width;
}

.main-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  height: $header-height;
  background: #ffffff;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f0f2f5;
}

// 页面切换动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 暗色主题
[data-theme='dark'] {
  .header {
    background: #1a1a1a;
    border-bottom-color: #333;
  }

  .content {
    background: #0a0a0a;
  }
}
</style>

