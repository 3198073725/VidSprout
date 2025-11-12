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

// 根据后端模板，推荐媒体需要用户登录才能查看
const canView = computed(() => auth.token)

async function loadRecommendedMedia() {
  if (!canView.value) return
  
  loading.value = true
  try {
    const response = await MediaAPI.listMedia({ page: currentPage.value })
    if (response?.results) {
      // 按照推荐算法排序：点赞数 > 观看数 > 时间
      const sortedItems = [...response.results].sort((a, b) => {
        const aScore = (a.likes || 0) * 10 + (a.views || 0) * 0.1
        const bScore = (b.likes || 0) * 10 + (b.views || 0) * 0.1
        if (aScore !== bScore) return bScore - aScore
        
        // 如果评分相同，按时间排序
        const aTime = new Date(a.add_date || 0).getTime()
        const bTime = new Date(b.add_date || 0).getTime()
        return bTime - aTime
      })
      
      mediaList.value = {
        ...response,
        results: sortedItems
      }
    }
  } catch (error) {
    console.error('加载推荐媒体失败:', error)
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

function getRecommendScore(item: MediaItem): number {
  return (item.likes || 0) * 10 + (item.views || 0) * 0.1
}

onMounted(loadRecommendedMedia)
</script>

<template>
  <div class="recommended-container">
    <div class="page-header">
      <h1>推荐媒体</h1>
    </div>

    <!-- 对应后端模板的 {% if user %} 条件 -->
    <div v-if="canView" id="page-recommended">
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
          <div v-if="mediaList?.results?.length" class="recommended-content">
            <div class="stats-info" v-if="mediaList?.count">
              共 <strong>{{ mediaList.count }}</strong> 个推荐视频
            </div>

            <!-- 网格布局 - 和首页一致 -->
            <div class="items-grid">
              <div 
                v-for="(item, index) in mediaList.results" 
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
                  <div v-if="index < 3" class="rank-badge" :class="`rank-${index + 1}`">
                    #{{ index + 1 }}
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
                @current-change="loadRecommendedMedia"
              />
            </div>
          </div>

          <!-- 空状态 -->
          <el-empty 
            v-else 
            description="暂无推荐媒体"
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
        sub-title="请登录后查看推荐媒体"
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
.recommended-container {
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

.stats-info {
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
  padding: 12px 0;
}

.stats-info strong {
  color: #2c3e50;
  font-weight: 600;
}

.recommended-content {
  min-height: 400px;
}

/* 使用和首页一致的网格布局 */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  padding: 0;
  width: 100%;
}

.item-thumb {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  height: 220px; /* 和首页完全一致 */
}

.item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.thumb-image-container {
  position: relative;
  width: 100%;
  flex: 0 0 auto;
  aspect-ratio: 16 / 9;
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
  padding: 8px;
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

.rank-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.rank-badge.rank-1 {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #333;
}

.rank-badge.rank-2 {
  background: linear-gradient(45deg, #c0c0c0, #e5e5e5);
  color: #333;
}

.rank-badge.rank-3 {
  background: linear-gradient(45deg, #cd7f32, #daa520);
}

.recommend-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: linear-gradient(45deg, #667eea, #764ba2);
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
  .recommended-container {
    padding: 16px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 480px) {
  .recommended-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.75rem;
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

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .recommended-container {
  background: #0a0a0a;
  color: #ffffff;
}

[data-theme="dark"] .page-header h1 {
  color: #ffffff;
}

[data-theme="dark"] .stats-info {
  color: #999;
}

[data-theme="dark"] .stats-info strong {
  color: #ffffff;
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
  background: rgba(0, 0, 0, 0.9);
  color: #ffffff;
}

[data-theme="dark"] .login-required {
  background: #0a0a0a;
}
</style>
