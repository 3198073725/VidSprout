<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaItem, Paginated } from '@/api'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const mediaList = ref<Paginated<MediaItem> | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)

// 根据后端模板，精选媒体需要用户登录才能查看
const canView = computed(() => auth.token)

async function loadFeaturedMedia() {
  if (!canView.value) return
  
  loading.value = true
  try {
    const response = await MediaAPI.listMedia({ page: currentPage.value })
    if (response?.results) {
      // 筛选出精选媒体 (featured = true)
      const featuredItems = response.results.filter(item => (item as any).featured === true)
      mediaList.value = {
        ...response,
        results: featuredItems,
        count: featuredItems.length
      }
    }
  } catch (error) {
    console.error('加载精选媒体失败:', error)
  } finally {
    loading.value = false
  }
}

function openMedia(item: MediaItem) {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

function formatDate(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

function formatDuration(seconds?: number) {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// SEO结构化数据将通过document.head动态添加
onMounted(() => {
  // 添加结构化数据
  const script = document.createElement('script')
  script.type = 'application/ld+json'
  script.textContent = JSON.stringify({
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [{
      "@type": "ListItem",
      "position": 1,
      "name": "Short Video Platform",
      "item": {
        "@type": "WebPage",
        "@id": window.location.origin
      }
    },
    {
      "@type": "ListItem", 
      "position": 2,
      "name": "Featured",
      "item": {
        "@type": "WebPage",
        "@id": window.location.origin + "/featured"
      }
    }]
  })
  document.head.appendChild(script)
  
  // 加载数据
  loadFeaturedMedia()
})
</script>

<template>
  <div class="featured-container">
    <div class="page-header">
      <h1>精选媒体</h1>
    </div>

    <!-- 对应后端模板的 {% if user %} 条件 -->
    <div v-if="canView" id="page-featured">
      <el-skeleton :loading="loading" animated>
        <template #template>
          <div class="media-grid-skeleton">
            <el-skeleton-item 
              v-for="n in 8" 
              :key="n"
              variant="rect" 
              style="width: 100%; height: 200px; margin-bottom: 16px"
            />
          </div>
        </template>

        <template #default>
          <div v-if="mediaList?.results?.length" class="featured-content">
            <!-- 媒体网格 - 和首页一致 -->
            <div class="items-grid">
              <div 
                v-for="item in mediaList.results" 
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

            <!-- 分页 -->
            <div v-if="mediaList.count > pageSize" class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize"
                :total="mediaList.count"
                layout="prev, pager, next"
                @current-change="loadFeaturedMedia"
              />
            </div>
          </div>

          <!-- 空状态 -->
          <el-empty 
            v-else 
            description="暂无精选媒体"
            :image-size="120"
          >
            <el-button type="primary" @click="router.push('/')">
              浏览所有媒体
            </el-button>
          </el-empty>
        </template>
      </el-skeleton>
    </div>

    <!-- 未登录状态 - 对应后端模板的用户检查 -->
    <div v-else class="login-required">
      <el-result
        icon="warning"
        title="需要登录"
        sub-title="请登录后查看精选媒体"
      >
        <template #extra>
          <el-button type="primary" @click="router.push('/login')">
            立即登录
          </el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style scoped>
.featured-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin-bottom: 8px;
}

.page-header p {
  font-size: 1.1rem;
  color: var(--mc-text-secondary);
  margin: 0;
}

.media-grid-skeleton {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.featured-content {
  min-height: 400px;
}

/* 媒体列表样式 - 上下排列 */
.media-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.media-list-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
}

.media-list-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.media-thumbnail {
  position: relative;
  flex-shrink: 0;
  width: 90px;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 8px;
}

.media-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.media-author {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.media-stats {
  font-size: 13px;
  color: #888;
}

.duration-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}

.featured-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: linear-gradient(45deg, #ff6b6b, #ffd93d);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.media-description {
  font-size: 14px;
  color: var(--mc-text-secondary);
  line-height: 1.4;
  margin: 8px 0 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.login-required {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 2rem;
  }
  
  .featured-container {
    padding: 16px;
  }
  
  .media-list-item {
    flex-direction: column;
    gap: 12px;
    padding: 12px;
  }
  
  .media-thumbnail {
    width: 100%;
    height: 180px;
  }
  
  .media-info {
    gap: 6px;
  }
  
  .media-title {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .featured-container {
    padding: 12px;
  }
  
  .media-list {
    gap: 12px;
  }
  
  .media-list-item {
    padding: 10px;
  }
  
  .media-thumbnail {
    height: 160px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .featured-page {
  background: #0a0a0a;
  color: #ffffff;
}

[data-theme="dark"] .page-title {
  color: #ffffff;
}

[data-theme="dark"] .stats-info {
  color: #999;
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

[data-theme="dark"] .login-required {
  background: #0a0a0a;
}
</style>
