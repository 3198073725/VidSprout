<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaItem, Paginated } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { 
  VideoCamera, 
  Picture, 
  Document,
  ArrowDown 
} from '@element-plus/icons-vue'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const mediaList = ref<Paginated<MediaItem> | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)

interface UserInfo {
  username: string
  name: string
}

const userInfo = ref<UserInfo | null>(null)

// 根据后端模板逻辑，检查用户是否存在
const userExists = computed(() => !!userInfo.value)

async function loadSharedMedia() {
  loading.value = true
  try {
    // 使用修正后的API：获取我分享给别人的媒体
    const response = await MediaAPI.getSharedByMeMedia({ page: currentPage.value })
    mediaList.value = response
    
    // 设置用户信息
    if (auth.profile) {
      userInfo.value = {
        username: auth.profile.username,
        name: auth.profile.name || auth.profile.username
      }
    }
  } catch (error) {
    console.error('加载分享媒体失败:', error)
    ElMessage.error('加载失败，请稍后再试')
    userInfo.value = null
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

function getSharedWithText(sharedWith?: string[]) {
  if (!sharedWith || sharedWith.length === 0) return '未分享'
  if (sharedWith.length === 1) return `分享给: ${sharedWith[0]}`
  return `分享给 ${sharedWith.length} 个用户`
}

onMounted(loadSharedMedia)
</script>

<template>
  <div class="user-shared-by-me-container">
    <!-- 对应后端模板的头部信息 -->
    <div class="page-header">
      <h1>
        <span v-if="userInfo?.name">{{ userInfo.name }} - </span>
        我分享的媒体
      </h1>
      <p>管理您分享给其他用户的媒体内容</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- 对应后端模板的 {% if user %} 条件检查 -->
    <div v-else-if="userExists">
      <!-- 对应后端的 <div id="page-profile-media"></div> -->
      <div id="page-profile-media" class="shared-media-content">
        
        <!-- 统计信息 -->
        <el-card class="stats-card" shadow="never">
          <el-statistic 
            title="分享的媒体总数" 
            :value="mediaList?.count || 0" 
            suffix="个"
          />
        </el-card>

        <div v-if="mediaList?.results?.length" class="media-list-section">
          <!-- 媒体列表 -->
          <div class="shared-media-list">
            <div 
              v-for="item in mediaList.results" 
              :key="item.friendly_token"
              class="shared-media-item"
            >
              <div class="media-thumbnail" @click="openMedia(item)">
                <img 
                  :src="item.thumbnail_url || item.poster_url || '/placeholder.jpg'"
                  :alt="item.title"
                  class="thumbnail-image"
                />
                <div v-if="item.duration" class="duration-badge">
                  {{ formatDuration(item.duration) }}
                </div>
                <div class="media-type-badge">
                  <el-icon>
                    <VideoCamera v-if="item.media_type === 'video'" />
                    <Picture v-else-if="item.media_type === 'image'" />
                    <Document v-else />
                  </el-icon>
                </div>
              </div>
              
              <div class="media-info">
                <h3 class="media-title" @click="openMedia(item)">
                  {{ item.title }}
                </h3>
                
                <p v-if="item.description" class="media-description">
                  {{ item.description }}
                </p>
                
                <div class="media-meta">
                  <div class="meta-row">
                    <span class="meta-label">分享状态:</span>
                    <span class="meta-value">{{ getSharedWithText((item as any).shared_with) }}</span>
                  </div>
                  
                  <div class="meta-row">
                    <span class="meta-label">分享时间:</span>
                    <span class="meta-value">{{ formatDate(item.add_date) }}</span>
                  </div>
                  
                  <div class="meta-row">
                    <span class="meta-label">观看次数:</span>
                    <span class="meta-value">{{ item.views || 0 }} 次</span>
                  </div>
                </div>
                
                <div class="media-actions">
                  <el-button size="small" @click="openMedia(item)">
                    查看详情
                  </el-button>
                  
                  <el-button 
                    size="small" 
                    type="primary"
                    @click="router.push(`/media/${item.friendly_token}/edit`)"
                  >
                    管理分享
                  </el-button>
                  
                  <el-dropdown trigger="click">
                    <el-button size="small">
                      更多 <el-icon><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item @click="router.push(`/media/${item.friendly_token}/edit`)">
                          编辑媒体
                        </el-dropdown-item>
                        <el-dropdown-item>
                          复制分享链接
                        </el-dropdown-item>
                        <el-dropdown-item divided>
                          取消分享
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
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
              @current-change="loadSharedMedia"
            />
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="empty-shared-media">
          <el-empty 
            description="您还没有分享任何媒体"
            :image-size="120"
          >
            <el-button type="primary" @click="router.push('/upload')">
              上传并分享媒体
            </el-button>
          </el-empty>
        </div>
      </div>
    </div>

    <!-- 对应后端模板的 {% else %} 用户不存在 -->
    <div v-else class="user-not-found">
      <el-result
        icon="warning"
        title="用户不存在"
        sub-title="找不到指定的用户"
      >
        <template #extra>
          <el-button type="primary" @click="router.push('/')">
            返回首页
          </el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style scoped>
/* 对应后端的 profile-media.css 样式 */
.user-shared-by-me-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 8px 0;
}

.page-header p {
  font-size: 1rem;
  color: var(--mc-text-secondary);
  margin: 0;
}

.loading-container {
  padding: 40px;
}

.shared-media-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-card {
  text-align: center;
  margin-bottom: 8px;
}

.media-list-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.shared-media-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.shared-media-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.shared-media-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.media-thumbnail {
  position: relative;
  width: 200px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: var(--mc-bg-secondary);
}

.duration-badge {
  position: absolute;
  bottom: 6px;
  right: 6px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
}

.media-type-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px;
  border-radius: 4px;
  font-size: 14px;
}

.media-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.media-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--mc-text-primary);
  cursor: pointer;
  line-height: 1.3;
}

.media-title:hover {
  color: var(--el-color-primary);
}

.media-description {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.media-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
}

.meta-label {
  color: var(--mc-text-secondary);
  min-width: 80px;
}

.meta-value {
  color: var(--mc-text-primary);
  font-weight: 500;
}

.media-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: auto;
}

.pagination-container {
  display: flex;
  justify-content: center;
}

.empty-shared-media {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.user-not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-shared-by-me-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .shared-media-item {
    flex-direction: column;
    padding: 16px;
  }
  
  .media-thumbnail {
    width: 100%;
    height: 180px;
  }
  
  .media-actions {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .media-thumbnail {
    height: 160px;
  }
  
  .media-actions {
    flex-direction: column;
  }
  
  .media-actions .el-button {
    width: 100%;
  }
  
  .meta-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }
}
</style>
