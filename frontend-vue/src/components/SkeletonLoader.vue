<template>
  <div class="skeleton-loader" :class="[`skeleton-${type}`, { 'animated': animated }]">
    <!-- 卡片骨架屏 -->
    <template v-if="type === 'card'">
      <div class="skeleton-card">
        <div class="skeleton-image"></div>
        <div class="skeleton-content">
          <div class="skeleton-title"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text short"></div>
        </div>
      </div>
    </template>

    <!-- 列表骨架屏 -->
    <template v-else-if="type === 'list'">
      <div v-for="i in count" :key="i" class="skeleton-list-item">
        <div class="skeleton-avatar"></div>
        <div class="skeleton-content">
          <div class="skeleton-title"></div>
          <div class="skeleton-text"></div>
        </div>
      </div>
    </template>

    <!-- 表格骨架屏 -->
    <template v-else-if="type === 'table'">
      <div class="skeleton-table">
        <div class="skeleton-header">
          <div v-for="i in columns" :key="i" class="skeleton-cell"></div>
        </div>
        <div v-for="i in count" :key="i" class="skeleton-row">
          <div v-for="j in columns" :key="j" class="skeleton-cell"></div>
        </div>
      </div>
    </template>

    <!-- 详情页骨架屏 -->
    <template v-else-if="type === 'detail'">
      <div class="skeleton-detail">
        <div class="skeleton-media"></div>
        <div class="skeleton-info">
          <div class="skeleton-title large"></div>
          <div class="skeleton-text long"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text short"></div>
        </div>
      </div>
    </template>

    <!-- 自定义骨架屏 -->
    <template v-else-if="type === 'custom'">
      <slot name="skeleton">
        <div class="skeleton-custom">
          <div class="skeleton-placeholder"></div>
        </div>
      </slot>
    </template>

    <!-- 默认骨架屏 -->
    <template v-else>
      <div class="skeleton-default">
        <div class="skeleton-shimmer"></div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
interface Props {
  type?: 'card' | 'list' | 'table' | 'detail' | 'custom' | 'default'
  count?: number
  columns?: number
  animated?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'default',
  count: 3,
  columns: 4,
  animated: true,
  loading: true
})
</script>

<style scoped>
.skeleton-loader {
  width: 100%;
}

.skeleton-loader.animated .skeleton-image,
.skeleton-loader.animated .skeleton-title,
.skeleton-loader.animated .skeleton-text,
.skeleton-loader.animated .skeleton-avatar,
.skeleton-loader.animated .skeleton-cell,
.skeleton-loader.animated .skeleton-media,
.skeleton-loader.animated .skeleton-placeholder {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 卡片骨架屏 */
.skeleton-card {
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.skeleton-image {
  width: 100%;
  height: 200px;
  background-color: #f0f0f0;
}

.skeleton-content {
  padding: 16px;
}

.skeleton-title {
  height: 20px;
  width: 60%;
  background-color: #f0f0f0;
  margin-bottom: 12px;
  border-radius: 4px;
}

.skeleton-text {
  height: 16px;
  background-color: #f0f0f0;
  margin-bottom: 8px;
  border-radius: 4px;
}

.skeleton-text.short {
  width: 40%;
}

.skeleton-text.long {
  width: 80%;
}

/* 列表骨架屏 */
.skeleton-list-item {
  display: flex;
  padding: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.skeleton-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f0f0f0;
  margin-right: 16px;
  flex-shrink: 0;
}

/* 表格骨架屏 */
.skeleton-table {
  width: 100%;
}

.skeleton-header,
.skeleton-row {
  display: flex;
  border-bottom: 1px solid #f0f0f0;
}

.skeleton-header {
  background-color: #fafafa;
  font-weight: 500;
}

.skeleton-cell {
  flex: 1;
  padding: 16px;
  height: 20px;
  background-color: #f0f0f0;
  margin: 8px;
  border-radius: 4px;
}

/* 详情页骨架屏 */
.skeleton-detail {
  padding: 24px;
}

.skeleton-media {
  width: 100%;
  height: 400px;
  background-color: #f0f0f0;
  border-radius: 8px;
  margin-bottom: 24px;
}

.skeleton-info {
  max-width: 800px;
}

.skeleton-title.large {
  height: 32px;
  width: 70%;
}

/* 自定义骨架屏 */
.skeleton-custom {
  padding: 16px;
}

.skeleton-placeholder {
  height: 100px;
  background-color: #f0f0f0;
  border-radius: 4px;
}

/* 默认骨架屏 */
.skeleton-default {
  height: 100px;
  background-color: #f0f0f0;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.skeleton-shimmer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  transform: translateX(-100%);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  100% {
    transform: translateX(100%);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .skeleton-card {
    margin-bottom: 16px;
  }
  
  .skeleton-media {
    height: 200px;
  }
  
  .skeleton-detail {
    padding: 16px;
  }
}
</style>