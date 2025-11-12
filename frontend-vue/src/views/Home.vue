<script setup lang="ts">
import { onMounted, ref, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { MediaAPI, MiscAPI } from '@/api'
import type { MediaItem, Tag } from '@/api'
import TagSection from '@/components/home/TagSection.vue'
import MediaSlider from '@/components/media/MediaSlider.vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const latest = ref<MediaItem[]>([])
const featured = ref<MediaItem[]>([])
const recommended = ref<MediaItem[]>([])
const tags = ref<Tag[]>([])

const load = async () => {
  loading.value = true
  try {
    // If not logged in, keep homepage minimal (hero only)
    if (!auth.isLoggedIn) return
    
    const [mediaRes, tagRes] = await Promise.all([
      MediaAPI.listMedia(),
      MiscAPI.listTags({ page: 1 }),
    ])
    
    const all = mediaRes?.results ?? []
    
    // Featured: featured first, then user_featured as fallback
    const f1 = all.filter(m => m.featured)
    const f2 = all.filter(m => !m.featured && m.user_featured)
    featured.value = [...f1, ...f2].slice(0, 12)

    // Recommended: by likes then views desc
    recommended.value = [...all]
      .sort((a, b) => (b.likes ?? 0) - (a.likes ?? 0) || (b.views ?? 0) - (a.views ?? 0))
      .slice(0, 12)

    // Latest: by add_date desc if exists
    latest.value = [...all]
      .sort((a, b) => new Date(b.add_date || 0).getTime() - new Date(a.add_date || 0).getTime())
      .slice(0, 12)
    
    tags.value = (tagRes?.results ?? []).slice(0, 20)
  } finally {
    loading.value = false
  }
}

const openMedia = (item: MediaItem) => {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

const formatDuration = (seconds?: number) => {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

onMounted(load)

// 当组件被激活时（例如从其他页面返回），重新加载数据
onActivated(load)
</script>

<template>
  <div class="home-container">
    <!-- 对应后端模板的 <div id="page-home"></div> -->
    <div id="page-home">
      <!-- Hero区域 -->
      <section class="mc-hero" v-if="!auth.isLoggedIn">
        <div class="mc-hero-title">欢迎来到短视频平台！</div>
        <div class="mc-hero-sub">开始上传媒体并分享您的作品！</div>
        <el-button type="success" size="large" @click="router.push('/upload')">
          <el-icon style="margin-right:6px"><VideoCamera /></el-icon>
          UPLOAD MEDIA
        </el-button>
      </section>

      <!-- 主要内容区域 -->
      <div v-if="auth.isLoggedIn" class="home-content">
        <!-- 推荐区域 - 使用横向滚动列表 -->
        <MediaSlider 
          v-if="recommended.length"
          title="推荐视频"
          :items="recommended"
          :loading="loading"
          view-all-link="/recommended"
        />

        <!-- 精选区域 - 使用横向滚动列表 -->
        <MediaSlider 
          v-if="featured.length"
          title="精选内容"
          :items="featured"
          :loading="loading"
          view-all-link="/featured"
        />

        <!-- 最新区域 - 使用网格布局 -->
        <div class="section-title-row" v-if="latest.length">
          <h2 class="section-title">最新</h2>
          <el-button 
            type="primary" 
            link 
            @click="router.push('/latest')"
            class="view-all-btn"
          >
            查看全部
          </el-button>
        </div>
        
        <div class="items-grid" v-if="latest.length">
          <div 
            v-for="item in latest.slice(0, 12)" 
            :key="item.friendly_token"
            class="item-thumb"
            :class="{ 'image-media-thumb': item.media_type === 'image' }"
            @click="openMedia(item)"
          >
            <div class="thumb-image-container">
              <img 
                :src="item.thumbnail_url || item.poster_url || '/placeholder.jpg'"
                :alt="item.title"
                class="thumb-image"
                :class="{ 'image-media': item.media_type === 'image' }"
              />
              <div v-if="item.duration" class="thumb-duration">
                {{ formatDuration(item.duration) }}
              </div>
            </div>
            <div class="thumb-body">
              <div class="thumb-title">{{ item.title }}</div>
              <div class="thumb-meta">
                {{ item.author_name || item.user }} · {{ item.views || 0 }} 次观看
              </div>
              
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

        <!-- 标签 -->
        <TagSection v-if="tags?.length" title="标签" :items="tags" />
      </div>

      <!-- 加载状态 -->
      <el-skeleton :loading="loading" animated v-if="auth.isLoggedIn && loading">
        <template #template>
          <div class="skeleton-container">
            <div class="skeleton-grid">
            <el-skeleton-item 
                v-for="n in 12" 
              :key="n"
              variant="rect" 
                style="width: 100%; padding-top: 56.25%; margin-bottom: 8px"
            />
            </div>
          </div>
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 对应后端模板的 page-home 样式 */
#page-home {
  width: 100%;
}

/* Hero区域样式 */
.mc-hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
  margin-bottom: 40px;
}

.mc-hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.mc-hero-sub {
  font-size: 1.2rem;
  margin-bottom: 32px;
  opacity: 0.9;
}

/* 主要内容区域 */
.home-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.section-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  margin-top: 32px;
}

.section-title-row:first-child {
  margin-top: 0;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.view-all-btn {
  font-size: 14px;
  padding: 0;
  height: auto;
}

/* 标签页样式 */
.home-tabs {
  padding: 0 20px;
}

.home-tabs :deep(.el-tabs__header) {
  margin: 0;
  border-bottom: 1px solid #e4e7ed;
}

.home-tabs :deep(.el-tabs__nav-wrap) {
  padding: 0;
}

.home-tabs :deep(.el-tabs__content) {
  padding: 0;
}

/* 媒体网格布局 - MediaCMS 原始样式 */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  padding: 0;
  width: 100%;
}

.item-thumb {
  background: #fff;
  border-radius: 8px !important;
  overflow: visible; /* 改为 visible，允许标签溢出显示 */
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  min-height: 200px; /* 改为最小高度，允许内容撑开 */
}

.item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.thumb-image-container {
  position: relative;
  width: 100%;
  flex: 0 0 auto;
  aspect-ratio: 16 / 9; /* 16:9 比例 */
  background: #f5f5f5;
  overflow: hidden;
  border-radius: 8px 8px 0 0;
}

.thumb-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 8px 8px 0 0;
}

/* 图片类型媒体：保持容器尺寸一致，但内容用 contain 显示 */
.item-thumb.image-media-thumb .thumb-image.image-media {
  object-fit: contain !important;
  background: #f5f5f5;
}

.thumb-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
  font-weight: 500;
}

.thumb-body {
  padding: 12px 14px 20px; /* 底部增加到 20px，确保标签下方有足够间距 */
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 0 0 auto;
  min-height: 70px;
  overflow: visible;
}

.thumb-title {
  font-size: 13px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
  flex-shrink: 0;
  /* line-clamp: 2; 已被 -webkit-line-clamp 替代 */
}

.thumb-meta {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

.thumb-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}

.media-tag {
  font-size: 11px !important;
  height: 20px !important;
  line-height: 18px !important;
  padding: 0 6px !important;
}

/* 骨架屏样式 */
.skeleton-container {
  padding: 20px 0;
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .home-page {
  background: #0a0a0a;
  color: #ffffff;
}

[data-theme="dark"] .section-title {
  color: #ffffff;
}

[data-theme="dark"] .home-tabs :deep(.el-tabs__header) {
  border-bottom-color: #333;
}

[data-theme="dark"] .item-thumb {
  background: #1a1a1a;
  border-color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .thumb-image-container {
  background: #2a2a2a;
}

/* 夜间模式：图片类型媒体背景 */
[data-theme="dark"] .item-thumb.image-media-thumb .thumb-image.image-media {
  background: #1a1a1a;
}

[data-theme="dark"] .thumb-title {
  color: #ffffff;
}

[data-theme="dark"] .thumb-meta {
  color: #999;
}

[data-theme="dark"] .thumb-duration {
  background: rgba(0, 0, 0, 0.8);
  color: #ffffff;
}

[data-theme="dark"] .stats-info {
  color: #999;
}

[data-theme="dark"] .page-header h1 {
  color: #ffffff;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.skeleton-grid .el-skeleton-item {
  border-radius: 8px;
  overflow: hidden;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-container {
    padding: 16px;
  }
  
  .mc-hero {
    padding: 40px 16px;
  }
  
  .mc-hero-title {
    font-size: 2rem;
  }
  
  .mc-hero-sub {
    font-size: 1rem;
  }
  
  .home-content {
    gap: 24px;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
  }
  
  .thumb-body {
    padding: 10px;
    gap: 4px;
  }
  
  .thumb-title {
    font-size: 13px;
  }
  
  .thumb-meta {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .home-container {
    padding: 12px;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }
  
  .thumb-body {
    padding: 8px;
  }
  
  .thumb-title {
    font-size: 12px;
    -webkit-line-clamp: 1;
    min-height: 20px;
  }
}
</style>
