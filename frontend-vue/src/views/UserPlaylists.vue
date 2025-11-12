<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PlaylistsAPI } from '@/api'
import type { PlaylistDetail, Paginated } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const username = computed(() => String(route.params.username))
const loading = ref(false)
const playlists = ref<Paginated<Pick<PlaylistDetail, 'title' | 'description' | 'user' | 'media_count' | 'url' | 'thumbnail_url'>> | null>(null)
const userInfo = ref<any>(null)

// 根据后端模板逻辑，检查用户是否存在
const userExists = computed(() => !!userInfo.value)

async function loadUserPlaylists() {
  loading.value = true
  try {
    // 加载用户播放列表
    const playlistsResponse = await PlaylistsAPI.listPlaylists()
    
    // 筛选出指定用户的播放列表
    if (playlistsResponse?.results) {
      const userPlaylists = playlistsResponse.results.filter(
        playlist => playlist.user === username.value
      )
      
      playlists.value = {
        ...playlistsResponse,
        results: userPlaylists,
        count: userPlaylists.length
      }
    }
    
    // 模拟用户信息（实际应该从用户API获取）
    if (playlists.value?.results.length) {
      userInfo.value = {
        username: username.value,
        name: username.value, // 可以从API获取真实姓名
        thumbnail_url: null
      }
    }
  } catch (error) {
    console.error('加载用户播放列表失败:', error)
  } finally {
    loading.value = false
  }
}

function openPlaylist(playlist: any) {
  // 从URL中提取playlist token
  const urlParts = playlist.url.split('/')
  const token = urlParts[urlParts.length - 2] || urlParts[urlParts.length - 1]
  router.push({ name: 'playlist-detail', params: { token } })
}

function formatDate(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

onMounted(loadUserPlaylists)
</script>

<template>
  <div class="user-playlists-container">
    <!-- 对应后端模板的头部信息 -->
    <div class="page-header">
      <h1>
        <span v-if="userInfo?.name">{{ userInfo.name }} - </span>
        播放列表
      </h1>
    </div>

    <!-- 对应后端模板的 {% if user %} 条件检查 -->
    <div v-if="userExists">
      <!-- 对应后端的 <div id="page-profile-playlists"></div> -->
      <div id="page-profile-playlists">
        <el-skeleton :loading="loading" animated>
          <template #template>
            <div class="playlists-skeleton">
              <el-skeleton-item 
                v-for="n in 6" 
                :key="n"
                variant="rect" 
                style="width: 100%; height: 160px; margin-bottom: 16px"
              />
            </div>
          </template>

          <template #default>
            <div v-if="playlists?.results?.length" class="playlists-content">
              <!-- 用户信息卡片 -->
              <el-card class="user-info-card" shadow="hover">
                <div class="user-profile">
                  <img 
                    :src="userInfo?.thumbnail_url || '/placeholder-avatar.jpg'"
                    :alt="userInfo?.username"
                    class="user-avatar"
                  />
                  <div class="user-details">
                    <h2>{{ userInfo?.name || userInfo?.username }}</h2>
                    <p>@{{ userInfo?.username }}</p>
                    <div class="user-stats">
                      <el-statistic 
                        title="播放列表" 
                        :value="playlists.count" 
                        suffix="个"
                      />
                    </div>
                  </div>
                </div>
              </el-card>

              <!-- 播放列表网格 -->
              <div class="playlists-grid">
                <el-card 
                  v-for="playlist in playlists.results" 
                  :key="playlist.url"
                  class="playlist-card"
                  shadow="hover"
                  @click="openPlaylist(playlist)"
                >
                  <div class="playlist-thumbnail">
                    <img 
                      :src="playlist.thumbnail_url || '/placeholder-playlist.jpg'"
                      :alt="playlist.title"
                      class="thumbnail-image"
                    />
                    <div class="media-count-badge">
                      {{ playlist.media_count || 0 }} 个视频
                    </div>
                  </div>
                  
                  <div class="playlist-info">
                    <h3 class="playlist-title">{{ playlist.title }}</h3>
                    <p v-if="playlist.description" class="playlist-description">
                      {{ playlist.description }}
                    </p>
                    <div class="playlist-meta">
                      <span class="media-count">{{ playlist.media_count || 0 }} 个媒体</span>
                    </div>
                  </div>
                </el-card>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-else class="empty-playlists">
              <el-empty 
                description="该用户还没有创建播放列表"
                :image-size="120"
              >
                <el-button 
                  v-if="auth.profile?.username === username"
                  type="primary" 
                  @click="router.push('/playlists')"
                >
                  创建播放列表
                </el-button>
              </el-empty>
            </div>
          </template>
        </el-skeleton>
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
/* 对应后端的 profile-playlists.css 样式 */
.user-playlists-container {
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
  margin: 0;
}

.playlists-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.playlists-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-info-card {
  margin-bottom: 8px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.user-details h2 {
  margin: 0 0 4px 0;
  font-size: 1.5rem;
  color: var(--mc-text-primary);
}

.user-details p {
  margin: 0 0 12px 0;
  color: var(--mc-text-secondary);
}

.user-stats {
  display: flex;
  gap: 24px;
}

.playlists-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.playlist-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.playlist-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.playlist-thumbnail {
  position: relative;
  width: 100%;
  height: 160px;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 12px;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  background: var(--mc-bg-secondary);
}

.media-count-badge {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.playlist-info {
  padding: 0 4px;
}

.playlist-title {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-description {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.playlist-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
}

.empty-playlists {
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
  .user-playlists-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .user-profile {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .user-avatar {
    width: 60px;
    height: 60px;
  }
  
  .playlists-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
  }
  
  .playlist-thumbnail {
    height: 140px;
  }
}

@media (max-width: 480px) {
  .playlists-grid {
    grid-template-columns: 1fr;
  }
}
</style>
