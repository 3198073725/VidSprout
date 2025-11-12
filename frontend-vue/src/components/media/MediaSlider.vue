<template>
  <div class="media-slider">
    <div v-if="title" class="slider-header">
      <h3 class="slider-title">{{ title }}</h3>
      <router-link v-if="viewAllLink" :to="viewAllLink" class="view-all-link">
        查看全部
        <el-icon><ArrowRight /></el-icon>
      </router-link>
    </div>

    <div class="slider-container">
      <button 
        v-if="showPrev" 
        class="slider-nav slider-nav-prev" 
        @click="scrollPrev"
        :aria-label="'向左滚动'"
      >
        <el-icon><ArrowLeft /></el-icon>
      </button>

      <div 
        ref="sliderRef" 
        class="slider-content" 
        @scroll="handleScroll"
      >
        <div 
          v-for="item in items" 
          :key="item.friendly_token || item.id"
          class="slider-item"
        >
          <div 
            class="media-card" 
            :class="{ 'image-media-card': item.media_type === 'image' }"
            @click="handleItemClick(item)"
          >
            <div class="media-thumbnail">
              <img 
                :src="item.thumbnail_url || item.poster_url || '/placeholder.jpg'" 
                :alt="item.title"
                :class="{ 'image-media': item.media_type === 'image' }"
                loading="lazy"
              />
              <div v-if="item.duration" class="media-duration">
                {{ formatDuration(item.duration) }}
              </div>
            </div>
            
            <div class="media-info">
              <h4 class="media-title">{{ item.title }}</h4>
              <div class="media-meta">
                <span v-if="item.author_name" class="author">{{ item.author_name }}</span>
                <span class="views">{{ formatViews(item.views || 0) }} 次观看</span>
                <span v-if="item.add_date" class="date">{{ formatDate(item.add_date) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载占位 -->
        <div v-if="loading" class="slider-item" v-for="n in 5" :key="`skeleton-${n}`">
          <el-skeleton animated>
            <template #template>
              <div class="skeleton-card">
                <el-skeleton-item variant="image" style="width: 100%; height: 180px;" />
                <div style="padding: 12px;">
                  <el-skeleton-item variant="h3" style="width: 80%;" />
                  <el-skeleton-item variant="text" style="width: 60%; margin-top: 8px;" />
                </div>
              </div>
            </template>
          </el-skeleton>
        </div>
      </div>

      <button 
        v-if="showNext" 
        class="slider-nav slider-nav-next" 
        @click="scrollNext"
        :aria-label="'向右滚动'"
      >
        <el-icon><ArrowRight /></el-icon>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, ArrowRight } from '@element-plus/icons-vue'
import type { MediaItem } from '@/api/types'

interface Props {
  title?: string
  items: MediaItem[]
  loading?: boolean
  viewAllLink?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const router = useRouter()
const sliderRef = ref<HTMLElement | null>(null)
const showPrev = ref(false)
const showNext = ref(true)

// 格式化时长
const formatDuration = (seconds: number): string => {
  if (!seconds) return '0:00'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = Math.floor(seconds % 60)
  
  if (h > 0) {
    return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }
  return `${m}:${s.toString().padStart(2, '0')}`
}

// 格式化观看次数
const formatViews = (views: number): string => {
  if (!views) return '0'
  if (views >= 1000000) {
    return `${(views / 1000000).toFixed(1)}M`
  }
  if (views >= 1000) {
    return `${(views / 1000).toFixed(1)}K`
  }
  return views.toString()
}

// 格式化日期
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '今天'
  if (diffDays === 1) return '昨天'
  if (diffDays < 7) return `${diffDays}天前`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}周前`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}个月前`
  return `${Math.floor(diffDays / 365)}年前`
}

// 处理点击
const handleItemClick = (item: MediaItem) => {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

// 滚动控制
const scrollPrev = () => {
  if (sliderRef.value) {
    const scrollAmount = sliderRef.value.clientWidth * 0.8
    sliderRef.value.scrollBy({ left: -scrollAmount, behavior: 'smooth' })
  }
}

const scrollNext = () => {
  if (sliderRef.value) {
    const scrollAmount = sliderRef.value.clientWidth * 0.8
    sliderRef.value.scrollBy({ left: scrollAmount, behavior: 'smooth' })
  }
}

// 处理滚动事件
const handleScroll = () => {
  if (!sliderRef.value) return
  
  const { scrollLeft, scrollWidth, clientWidth } = sliderRef.value
  showPrev.value = scrollLeft > 10
  showNext.value = scrollLeft < scrollWidth - clientWidth - 10
}

// 响应式处理
const handleResize = () => {
  handleScroll()
}

onMounted(() => {
  handleScroll()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.media-slider {
  width: 100%;
  margin-bottom: 40px;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 8px;
}

.slider-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.view-all-link {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #409eff;
  font-size: 14px;
  text-decoration: none;
  transition: color 0.3s;
}

.view-all-link:hover {
  color: #66b1ff;
}

.slider-container {
  position: relative;
}

.slider-content {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-behavior: smooth;
  padding: 8px;
  margin: 0 -8px;
  
  /* 隐藏滚动条但保持可滚动 */
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.slider-content::-webkit-scrollbar {
  display: none;
}

.slider-item {
  flex: 0 0 280px;
  min-width: 280px;
}

.media-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.media-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.media-thumbnail {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 比例 */
  background: #f5f5f5;
  overflow: hidden;
}

.media-thumbnail img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 图片类型媒体的特殊样式 */
.media-card.image-media-card .media-thumbnail img.image-media {
  object-fit: contain;
  background: #f5f5f5;
}

.media-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.media-info {
  padding: 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.media-title {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.media-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 12px;
  color: #666;
}

.media-meta span {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.author {
  font-weight: 500;
  color: #555;
}

.slider-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.3s;
}

.slider-nav:hover {
  background: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.slider-nav-prev {
  left: 0;
}

.slider-nav-next {
  right: 0;
}

.slider-nav .el-icon {
  font-size: 20px;
  color: #409eff;
}

.skeleton-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 暗黑模式 */
[data-theme="dark"] .slider-title {
  color: #ffffff;
}

[data-theme="dark"] .media-card {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .media-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .media-thumbnail {
  background: #2a2a2a;
}

[data-theme="dark"] .media-title {
  color: #ffffff;
}

[data-theme="dark"] .media-meta {
  color: #999;
}

[data-theme="dark"] .author {
  color: #ccc;
}

[data-theme="dark"] .slider-nav {
  background: rgba(26, 26, 26, 0.95);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .slider-nav:hover {
  background: #1a1a1a;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.7);
}

[data-theme="dark"] .skeleton-card {
  background: #1a1a1a;
}

/* 夜间模式下图片类型媒体的背景 */
[data-theme="dark"] .media-card.image-media-card .media-thumbnail img.image-media {
  background: #1a1a1a;
}

/* 响应式 */
@media (max-width: 768px) {
  .slider-item {
    flex: 0 0 220px;
    min-width: 220px;
  }
  
  .slider-nav {
    width: 32px;
    height: 32px;
  }
  
  .slider-nav .el-icon {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .slider-item {
    flex: 0 0 180px;
    min-width: 180px;
  }
  
  .slider-title {
    font-size: 18px;
  }
}
</style>

