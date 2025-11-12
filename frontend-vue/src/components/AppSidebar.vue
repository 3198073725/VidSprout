<script setup lang="ts">

const itemsTop = [
  { icon: 'House', label: '首页', to: '/' },
  { icon: 'Star', label: '精选', to: '/featured' },
  { icon: 'MagicStick', label: '推荐', to: '/recommended' },
  { icon: 'Clock', label: '最新', to: '/latest' },
  { icon: 'PriceTag', label: '标签', to: '/tags' },
  { icon: 'Collection', label: '分类', to: '/categories' },
]

const itemsMiddle = [
  { icon: 'Timer', label: '历史', to: '/history' },
  { icon: 'StarFilled', label: '喜欢的媒体', to: '/liked' },
]

const itemsBottom = [
  { icon: 'InfoFilled', label: '关于', to: '/about' },
  { icon: 'DocumentChecked', label: '条款', to: '/terms' },
  { icon: 'ChatDotSquare', label: '联系', to: '/contact' },
]
</script>

<template>
  <aside class="mc-sidebar">
    <!-- 主要导航 -->
    <nav class="mc-side-section">
      <router-link v-for="it in itemsTop" :key="it.label" :to="it.to" class="mc-side-item">
        <el-icon :size="18"><component :is="it.icon" /></el-icon>
        <span>{{ it.label }}</span>
      </router-link>
    </nav>
    
    <!-- 个人功能 -->
    <nav class="mc-side-section">
      <router-link v-for="it in itemsMiddle" :key="it.label" :to="it.to" class="mc-side-item">
        <el-icon :size="18"><component :is="it.icon" /></el-icon>
        <span>{{ it.label }}</span>
      </router-link>
    </nav>
    
    <!-- 关于信息 - 固定在底部 -->
    <nav class="mc-side-section mc-side-bottom">
      <router-link v-for="it in itemsBottom" :key="it.label" :to="it.to" class="mc-side-item">
        <el-icon :size="18"><component :is="it.icon" /></el-icon>
        <span>{{ it.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<style scoped>
.mc-sidebar {
  width: 240px;
  height: 100vh;
  background: var(--el-bg-color);
  border-right: 1px solid var(--el-border-color-light);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 999;
  padding-top: 64px; /* 为头部导航栏留出空间 */
}

/* 侧边栏头部 */
.sidebar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  height: 64px;
  border-bottom: 1px solid var(--el-border-color-lighter);
  background: var(--el-bg-color);
  flex-shrink: 0;
}

.sidebar-menu-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
  color: var(--el-text-color-primary);
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
}

.sidebar-menu-btn:hover {
  background: var(--el-fill-color-light);
}

.sidebar-logo {
  font-size: 20px;
  font-weight: 600;
  text-decoration: none;
  color: var(--el-text-color-primary);
  white-space: nowrap;
}

.sidebar-logo-accent {
  color: var(--el-color-primary);
}

.mc-side-section {
  padding: 16px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.mc-side-section:last-child {
  border-bottom: none;
}

.mc-side-bottom {
  margin-top: auto; /* 推到侧边栏底部 */
  border-top: 1px solid var(--el-border-color-lighter);
  border-bottom: none;
  padding-bottom: 16px; /* 底部留一些空间 */
}

.mc-side-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  color: var(--el-text-color-primary);
  text-decoration: none;
  transition: all 0.2s;
  border-radius: 0;
}

.mc-side-item:hover {
  background: var(--el-fill-color-light);
  color: var(--el-color-primary);
}

.mc-side-item.router-link-active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  border-right: 3px solid var(--el-color-primary);
}

.mc-side-item span {
  font-size: 14px;
  font-weight: 500;
}

/* 移动端用户信息区域 */
.mobile-user-section {
  display: none;
  padding: 20px;
  border-bottom: 1px solid var(--el-border-color-lighter);
  background: var(--el-fill-color-extra-light);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  flex: 1;
}

.username {
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.user-actions {
  margin-top: 8px;
}

.auth-actions {
  display: flex;
  gap: 12px;
}

.auth-actions .el-button {
  flex: 1;
}

/* 移动端功能按钮区域 */
.mobile-actions-section {
  display: none;
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-lighter);
  background: var(--el-fill-color-lighter);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 16px;
  margin-bottom: 8px;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
  border-radius: 6px;
  color: var(--el-text-color-primary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:hover {
  background: var(--el-fill-color-light);
  border-color: var(--el-color-primary);
}

.action-btn:last-child {
  margin-bottom: 0;
}

.search-btn {
  border-color: var(--el-color-info);
  color: var(--el-color-info);
}

.upload-btn {
  border-color: var(--el-color-success);
  color: var(--el-color-success);
}

.record-btn {
  border-color: var(--el-color-warning);
  color: var(--el-color-warning);
}

/* 移动端用户菜单 */
.mobile-user-menu {
  display: none;
}

.logout-btn {
  color: var(--el-color-danger) !important;
}

.logout-btn:hover {
  background: var(--el-color-danger-light-9) !important;
}

/* 按钮样式重置 */
.mc-side-item {
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.mc-side-item.active {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  border-right: 3px solid var(--el-color-primary);
}

/* 移动端响应式 */
@media (max-width: 1023px) {
  .mc-sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  /* 当侧边栏打开时 */
  .sidebar-mobile-open .mc-sidebar {
    transform: translateX(0);
  }

  /* 添加遮罩层 */
  .sidebar-mobile-open::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 998;
  }

  /* 移动端显示功能区域 */
  .mobile-user-section {
    display: block;
  }

  .mobile-actions-section {
    display: block;
  }

  .mobile-user-menu {
    display: block;
  }
}

@media (max-width: 767px) {
  .mc-sidebar {
    width: 50vw; /* 占屏幕一半宽度 */
    min-width: 280px;
    max-width: 320px;
    padding-top: 56px;
  }

  .mc-side-item {
    padding: 16px 20px;
    font-size: 16px;
  }

  .mc-side-item span {
    font-size: 16px;
  }
}

@media (max-width: 479px) {
  .mc-sidebar {
    width: 66vw; /* 占屏幕三分之二宽度 */
    min-width: 280px;
    max-width: 300px;
    padding-top: 52px;
  }

  .mc-side-section {
    padding: 20px 0;
  }

  .mc-side-item {
    padding: 18px 24px;
    font-size: 18px;
  }

  .mc-side-item span {
    font-size: 18px;
  }
}

/* 桌面端 - 侧边栏收起状态 */
@media (min-width: 1024px) {
  .sidebar-collapsed .mc-sidebar {
    width: 64px;
  }

  .sidebar-collapsed .mc-side-item span {
    display: none;
  }

  .sidebar-collapsed .mc-side-item {
    justify-content: center;
    padding: 12px;
  }
}

/* 深色模式 */
[data-theme="dark"] .mc-sidebar {
  background: var(--el-bg-color);
  border-right-color: var(--el-border-color);
}

[data-theme="dark"] .mc-side-section {
  border-bottom-color: var(--el-border-color);
}

[data-theme="dark"] .mc-side-item:hover {
  background: var(--el-fill-color);
}

[data-theme="dark"] .mc-side-item.router-link-active {
  background: var(--el-color-primary-dark-2);
}
</style>
