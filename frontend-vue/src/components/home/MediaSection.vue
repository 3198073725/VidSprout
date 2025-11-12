<script setup lang="ts">
import type { MediaItem } from '@/api'

const props = defineProps<{
  title: string
  items: MediaItem[]
}>()

const emit = defineEmits<{
  (e: 'open', item: MediaItem): void
}>()

function open(item: MediaItem) {
  emit('open', item)
}

// 判断是否为图片类型，以便应用不同的显示样式
function isImageMedia(item: MediaItem): boolean {
  return item.media_type === 'image'
}

// 格式化时长
function formatDuration(seconds?: number): string {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<template>
  <section class="home-sec">
    <div class="home-sec-head" v-if="title">
      <div class="home-sec-title">{{ title }}</div>
    </div>
    <div class="items-grid">
      <div
        v-for="item in items"
        :key="item.friendly_token"
        class="item-thumb"
        :class="{ 'image-media-thumb': isImageMedia(item) }"
        @click="open(item)"
      >
        <!-- 添加容器以保持统一的宽高比 -->
        <div class="thumb-image-container">
          <img 
            class="thumb-image" 
            :class="{ 'image-media': isImageMedia(item) }"
            :src="item.thumbnail_url || item.poster_url || '/placeholder.jpg'" 
            :alt="item.title" 
          />
          <!-- 时长标签 -->
          <div v-if="item.duration" class="thumb-duration">
            {{ formatDuration(item.duration) }}
          </div>
        </div>
        
        <div class="thumb-body">
          <div class="thumb-title">{{ item.title }}</div>
          <div class="thumb-meta">{{ item.author_name || item.user }} · {{ item.views || 0 }} 次观看</div>
          
          <!-- 显示分类和标签 -->
          <div v-if="item.categories_info?.length || item.tags_info?.length" class="thumb-tags">
            <el-tag 
              v-for="category in item.categories_info?.slice(0, 2)" 
              :key="category.title"
              size="small"
              type="primary"
              class="media-tag"
            >
              {{ category.title }}
            </el-tag>
            <el-tag 
              v-for="tag in item.tags_info?.slice(0, 2)" 
              :key="tag.title"
              size="small"
              class="media-tag"
            >
              {{ tag.title }}
            </el-tag>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* 标签容器 */
.thumb-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 8px;
}

.media-tag {
  font-size: 11px !important;
  height: 20px !important;
  line-height: 18px !important;
  padding: 0 6px !important;
}

/* 图片类型媒体的特殊样式：保持卡片尺寸一致，内容用 contain 显示 */
.item-thumb.image-media-thumb :deep(.thumb-image.image-media) {
  object-fit: contain !important;  /* 完整显示图片 */
  background: #f5f5f5 !important;  /* 浅灰背景 */
}

/* 夜间模式 */
[data-theme="dark"] .item-thumb.image-media-thumb :deep(.thumb-image.image-media) {
  background: #1a1a1a !important;
}
</style>
