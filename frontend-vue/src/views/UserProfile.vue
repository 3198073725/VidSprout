<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { MediaAPI, PlaylistsAPI } from '@/api'
import type { MediaItem, PlaylistDetail } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Edit, 
  Delete, 
  VideoCamera, 
  Headset, 
  Picture, 
  Document, 
  View, 
  Star,
  Select,
  Close,
  Check,
  Lock,
  Unlock,
  FolderAdd,
  Download,
  DocumentRemove,
  Link
} from '@element-plus/icons-vue'

// 定义用户信息类型
interface UserProfile {
  username: string
  name?: string
  description?: string
  thumbnail_url?: string
  date_added?: string
  [key: string]: unknown
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const username = computed(() => route.params.username as string)
const activeTab = ref('media')
const loading = ref(false)
const user = ref<UserProfile | null>(null)
const userMedia = ref<MediaItem[]>([])

// 是否是当前用户的主页
const isOwnProfile = computed(() => auth.profile?.username === username.value)

// 批量操作相关
const bulkMode = ref(false)
const selectedMedia = ref<string[]>([])
const allSelected = computed({
  get: () => selectedMedia.value.length > 0 && selectedMedia.value.length === userMedia.value.length,
  set: (val: boolean) => {
    if (val) {
      selectedMedia.value = userMedia.value.map(m => m.friendly_token)
    } else {
      selectedMedia.value = []
    }
  }
})

// 播放列表相关
const userPlaylists = ref<PlaylistDetail[]>([])
const addToPlaylistDialog = ref(false)
const selectedPlaylists = ref<number[]>([])

// 播放列表媒体显示相关
const selectedPlaylistId = ref<string>('all') // 'all' 或播放列表的 URL
const playlistMedia = ref<MediaItem[]>([]) // 当前选中播放列表的媒体
const loadingPlaylistMedia = ref(false)

async function loadUserProfile() {
  loading.value = true
  try {
    // 获取用户信息 - 使用 http 服务
    const response = await fetch(`/api/v1/users/${username.value}`, {
      headers: {
        'Authorization': auth.token ? `Token ${auth.token}` : ''
      }
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('用户不存在')
      }
      throw new Error('加载失败')
    }
    
    user.value = await response.json()
    console.log('User loaded:', user.value)
    
    // 获取用户的媒体
    const mediaRes = await MediaAPI.listMedia()
    // 过滤出该用户的媒体
    userMedia.value = (mediaRes?.results || []).filter(
      (m: MediaItem) => m.user === username.value
    )
    console.log('User media:', userMedia.value)
    
    // 加载播放列表（所有用户都可以查看）
    await loadUserPlaylists()
  } catch (error) {
    console.error('Load user error:', error)
    ElMessage.error((error as Error).message || '加载失败')
    router.push('/')
  } finally {
    loading.value = false
  }
}

// 加载用户的播放列表
async function loadUserPlaylists() {
  try {
    const res = await PlaylistsAPI.listPlaylists()
    // 筛选出当前用户的播放列表
    const allPlaylists = (res?.results || []) as PlaylistDetail[]
    userPlaylists.value = allPlaylists.filter(
      playlist => playlist.user === username.value
    )
    console.log(`加载了 ${userPlaylists.value.length} 个播放列表`)
    
    // 默认加载所有播放列表的媒体
    await loadPlaylistMedia('all')
  } catch (error) {
    console.error('Load playlists error:', error)
  }
}

// 加载播放列表中的媒体
async function loadPlaylistMedia(playlistId: string) {
  loadingPlaylistMedia.value = true
  try {
    if (playlistId === 'all') {
      // 加载所有播放列表中的媒体（去重）
      const allMedia: MediaItem[] = []
      const mediaIds = new Set<string>()
      
      for (const playlist of userPlaylists.value) {
        try {
          const token = extractPlaylistToken(playlist.url)
          const playlistDetail = await PlaylistsAPI.getPlaylistDetail(token)
          const media = (playlistDetail as any).playlist_media || []
          
          // 去重添加
          for (const item of media) {
            if (!mediaIds.has(item.friendly_token)) {
              mediaIds.add(item.friendly_token)
              allMedia.push(item)
            }
          }
        } catch (error) {
          console.error('加载播放列表媒体失败:', error)
        }
      }
      
      playlistMedia.value = allMedia
      console.log(`加载了 ${allMedia.length} 个播放列表媒体项`)
    } else {
      // 加载特定播放列表的媒体
      const playlistDetail = await PlaylistsAPI.getPlaylistDetail(playlistId)
      playlistMedia.value = (playlistDetail as any).playlist_media || []
      console.log(`加载了播放列表媒体: ${playlistMedia.value.length} 项`)
    }
  } catch (error) {
    console.error('Load playlist media error:', error)
    playlistMedia.value = []
  } finally {
    loadingPlaylistMedia.value = false
  }
}

// 切换播放列表选择
async function handlePlaylistChange(playlistId: string) {
  selectedPlaylistId.value = playlistId
  await loadPlaylistMedia(playlistId)
}

// 从播放列表URL中提取token
function extractPlaylistToken(url: string): string {
  const parts = url.split('/')
  return parts[parts.length - 1] || parts[parts.length - 2]
}

function openMedia(item: MediaItem) {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

function editProfile() {
  router.push(`/user/${username.value}/edit`)
}

// 格式化函数
function formatDuration(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function formatNumber(num?: number): string {
  if (num === undefined || num === null) return '0'
  if (num >= 10000) {
    return `${(num / 10000).toFixed(1)}w`
  }
  return num.toString()
}

function formatDate(dateString?: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}月前`
  return date.toLocaleDateString('zh-CN')
}

// 删除视频
function handleDeleteMedia(item: MediaItem, event: Event) {
  event.stopPropagation() // 阻止触发点击事件
  
  ElMessageBox.confirm(
    `确定要删除视频「${item.title}」吗？此操作不可恢复！`,
    '删除确认',
    {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    }
  ).then(async () => {
    try {
      await MediaAPI.deleteMedia(item.friendly_token)
      ElMessage.success('删除成功')
      // 从列表中移除
      userMedia.value = userMedia.value.filter(m => m.friendly_token !== item.friendly_token)
    } catch (error) {
      console.error('Delete error:', error)
      ElMessage.error((error as {message?: string})?.message || '删除失败')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

// 编辑视频
function handleEditMedia(item: MediaItem, event: Event) {
  event.stopPropagation()
  router.push({ name: 'media-edit', params: { token: item.friendly_token } })
}

// ========== 批量操作功能 ==========

// 切换批量模式
function toggleBulkMode() {
  bulkMode.value = !bulkMode.value
  if (!bulkMode.value) {
    selectedMedia.value = []
  }
}

// 切换单个媒体选择
function toggleMediaSelection(token: string) {
  const index = selectedMedia.value.indexOf(token)
  if (index > -1) {
    selectedMedia.value.splice(index, 1)
  } else {
    selectedMedia.value.push(token)
  }
}

// 批量删除
async function handleBulkDelete() {
  if (selectedMedia.value.length === 0) {
    ElMessage.warning('请先选择要删除的媒体')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedMedia.value.length} 个媒体吗？此操作不可恢复！`,
      '批量删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    await MediaAPI.bulkMediaActions({
      media_ids: selectedMedia.value,
      action: 'delete_media'
    })
    
    ElMessage.success(`成功删除 ${selectedMedia.value.length} 个媒体`)
    
    // 从列表中移除已删除的媒体
    userMedia.value = userMedia.value.filter(
      m => !selectedMedia.value.includes(m.friendly_token)
    )
    
    selectedMedia.value = []
    bulkMode.value = false
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error((error as {detail?: string})?.detail || '批量删除失败')
    }
  }
}

// 批量设置隐私状态
async function handleBulkSetPrivacy(state: 'public' | 'private' | 'unlisted') {
  if (selectedMedia.value.length === 0) {
    ElMessage.warning('请先选择要设置的媒体')
    return
  }
  
  const stateText = {
    public: '公开',
    private: '私密',
    unlisted: '仅限链接'
  }[state]
  
  try {
    await MediaAPI.bulkMediaActions({
      media_ids: selectedMedia.value,
      action: 'set_state',
      state
    })
    
    ElMessage.success(`成功将 ${selectedMedia.value.length} 个媒体设置为${stateText}`)
    selectedMedia.value = []
    bulkMode.value = false
  } catch (error) {
    ElMessage.error((error as {detail?: string})?.detail || '设置失败')
  }
}

// 批量启用/禁用评论
async function handleBulkToggleComments(enable: boolean) {
  if (selectedMedia.value.length === 0) {
    ElMessage.warning('请先选择要设置的媒体')
    return
  }
  
  try {
    await MediaAPI.bulkMediaActions({
      media_ids: selectedMedia.value,
      action: enable ? 'enable_comments' : 'disable_comments'
    })
    
    ElMessage.success(`成功${enable ? '启用' : '禁用'}评论`)
    selectedMedia.value = []
    bulkMode.value = false
  } catch (error) {
    ElMessage.error((error as {detail?: string})?.detail || '评论设置失败')
  }
}

// 批量启用/禁用下载
async function handleBulkToggleDownload(enable: boolean) {
  if (selectedMedia.value.length === 0) {
    ElMessage.warning('请先选择要设置的媒体')
    return
  }
  
  try {
    await MediaAPI.bulkMediaActions({
      media_ids: selectedMedia.value,
      action: enable ? 'enable_download' : 'disable_download'
    })
    
    ElMessage.success(`成功${enable ? '允许' : '禁止'}下载`)
    selectedMedia.value = []
    bulkMode.value = false
  } catch (error) {
    ElMessage.error((error as {detail?: string})?.detail || '下载设置失败')
  }
}

// 打开添加到播放列表对话框
function openAddToPlaylistDialog() {
  if (selectedMedia.value.length === 0) {
    ElMessage.warning('请先选择要添加的媒体')
    return
  }
  addToPlaylistDialog.value = true
  selectedPlaylists.value = []
}

// 批量添加到播放列表
async function handleBulkAddToPlaylist() {
  if (selectedPlaylists.value.length === 0) {
    ElMessage.warning('请选择播放列表')
    return
  }
  
  try {
    await MediaAPI.bulkMediaActions({
      media_ids: selectedMedia.value,
      action: 'add_to_playlist',
      playlist_ids: selectedPlaylists.value
    })
    
    ElMessage.success(`成功添加 ${selectedMedia.value.length} 个媒体到 ${selectedPlaylists.value.length} 个播放列表`)
    addToPlaylistDialog.value = false
    selectedMedia.value = []
    selectedPlaylists.value = []
    bulkMode.value = false
  } catch (error) {
    ElMessage.error((error as {detail?: string})?.detail || '添加失败')
  }
}

onMounted(loadUserProfile)
</script>

<template>
  <div class="user-profile">
    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="profile-header-skeleton">
          <el-skeleton-item variant="image" style="width: 100%; height: 200px" />
          <div style="padding: 20px">
            <el-skeleton-item variant="circle" style="width: 120px; height: 120px; margin-top: -80px" />
            <el-skeleton-item variant="text" style="width: 200px; margin-top: 16px" />
            <el-skeleton-item variant="text" style="width: 300px" />
          </div>
        </div>
      </template>
      
      <template #default>
        <div v-if="user" class="user-profile-container">
          <!-- 对应后端模板的 <div id="page-profile-media"></div> -->
          <div id="page-profile-media">
            <div class="page-header">
              <h1>{{ user.name || user.username }}</h1>
              <div class="header-actions" v-if="isOwnProfile">
                <el-button 
                  v-if="!bulkMode" 
                  type="primary" 
                  @click="toggleBulkMode"
                >
                  <el-icon><Select /></el-icon>
                  批量操作
                </el-button>
                <el-button 
                  v-else
                  @click="toggleBulkMode"
                >
                  <el-icon><Close /></el-icon>
                  取消选择
                </el-button>
                <el-button type="primary" @click="editProfile">
                  <el-icon><Edit /></el-icon>
                  编辑资料
                </el-button>
              </div>
            </div>
            
            <!-- 用户信息卡片 -->
            <div class="profile-card">
              <div class="profile-header">
                <el-avatar 
                  :src="user.thumbnail_url || '/media/userlogos/user.jpg'" 
                  :size="80"
                  class="profile-avatar"
                />
                <div class="profile-info">
                  <h2 class="profile-name">{{ user.name || user.username }}</h2>
                  <div class="profile-username">@{{ user.username }}</div>
                  <div v-if="user.description" class="profile-description">
                    {{ user.description }}
                  </div>
                </div>
              </div>
              
              <div class="profile-stats">
                <div class="stat-item">
                  <span class="stat-value">{{ userMedia.length }}</span>
                  <span class="stat-label">视频</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ userPlaylists.length }}</span>
                  <span class="stat-label">播放列表</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ user.date_added ? new Date(user.date_added).toLocaleDateString('zh-CN') : '未知' }}</span>
                  <span class="stat-label">加入时间</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 标签页 -->
          <div class="profile-tabs">
            <!-- 批量操作工具栏 -->
            <transition name="el-fade-in">
              <div v-if="bulkMode && isOwnProfile" class="bulk-toolbar">
                <div class="bulk-toolbar-left">
                  <el-checkbox 
                    v-model="allSelected" 
                    :indeterminate="selectedMedia.length > 0 && selectedMedia.length < userMedia.length"
                  >
                    全选 ({{ selectedMedia.length }}/{{ userMedia.length }})
                  </el-checkbox>
                </div>
                
                <div class="bulk-toolbar-right">
                  <el-dropdown trigger="click" @command="handleBulkSetPrivacy">
                    <el-button type="info">
                      <el-icon><Lock /></el-icon>
                      设置隐私
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="public">
                          <el-icon><Unlock /></el-icon>
                          公开
                        </el-dropdown-item>
                        <el-dropdown-item command="unlisted">
                          <el-icon><Link /></el-icon>
                          仅限链接
                        </el-dropdown-item>
                        <el-dropdown-item command="private">
                          <el-icon><Lock /></el-icon>
                          私密
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  
                  <el-button type="success" @click="openAddToPlaylistDialog">
                    <el-icon><FolderAdd /></el-icon>
                    添加到播放列表
                  </el-button>
                  
                  <el-dropdown trigger="click" split-button @click="handleBulkToggleComments(true)">
                    <el-icon><DocumentRemove /></el-icon>
                    评论管理
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item @click="handleBulkToggleComments(true)">
                          <el-icon><Check /></el-icon>
                          启用评论
                        </el-dropdown-item>
                        <el-dropdown-item @click="handleBulkToggleComments(false)">
                          <el-icon><Close /></el-icon>
                          禁用评论
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  
                  <el-dropdown trigger="click" split-button @click="handleBulkToggleDownload(true)">
                    <el-icon><Download /></el-icon>
                    下载管理
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item @click="handleBulkToggleDownload(true)">
                          <el-icon><Check /></el-icon>
                          允许下载
                        </el-dropdown-item>
                        <el-dropdown-item @click="handleBulkToggleDownload(false)">
                          <el-icon><Close /></el-icon>
                          禁止下载
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  
                  <el-button type="danger" @click="handleBulkDelete">
                    <el-icon><Delete /></el-icon>
                    批量删除
                  </el-button>
                </div>
              </div>
            </transition>
            <el-tabs v-model="activeTab">
              <el-tab-pane label="视频" name="media">
                <div v-if="userMedia.length > 0" class="media-grid">
                  <div 
                    v-for="item in userMedia" 
                    :key="item.friendly_token"
                    class="media-card"
                    :class="{ 'is-selected': bulkMode && selectedMedia.includes(item.friendly_token) }"
                  >
                    <!-- 批量选择复选框 -->
                    <div v-if="bulkMode && isOwnProfile" class="media-checkbox" @click.stop>
                      <el-checkbox 
                        :model-value="selectedMedia.includes(item.friendly_token)"
                        @change="toggleMediaSelection(item.friendly_token)"
                        size="large"
                      />
                    </div>
                    <!-- 媒体缩略图 -->
                    <div class="media-card-thumb" @click="openMedia(item)">
                      <img 
                        :src="item.thumbnail_url || item.poster_url || '/static/images/no-thumbnail.png'" 
                        :alt="item.title"
                        class="media-thumbnail"
                        @error="(e) => { (e.target as HTMLImageElement).src = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22300%22%3E%3Crect fill=%22%23f0f0f0%22 width=%22400%22 height=%22300%22/%3E%3Ctext fill=%22%23999%22 font-family=%22Arial%22 font-size=%2224%22 x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 dominant-baseline=%22middle%22%3E无缩略图%3C/text%3E%3C/svg%3E' }"
                      />
                      <div v-if="item.duration" class="media-duration">
                        {{ formatDuration(item.duration) }}
                      </div>
                      <div class="media-type-badge">
                        <el-icon v-if="item.media_type === 'video'"><VideoCamera /></el-icon>
                        <el-icon v-else-if="item.media_type === 'audio'"><Headset /></el-icon>
                        <el-icon v-else-if="item.media_type === 'image'"><Picture /></el-icon>
                        <el-icon v-else><Document /></el-icon>
                      </div>
                      
                      <!-- 当前用户的视频显示操作按钮 -->
                      <div v-if="isOwnProfile" class="media-actions">
                        <el-button 
                          size="small" 
                          type="primary" 
                          circle
                          @click="(e: Event) => handleEditMedia(item, e)"
                          title="编辑"
                        >
                          <el-icon><Edit /></el-icon>
                        </el-button>
                        <el-button 
                          size="small" 
                          type="danger" 
                          circle
                          @click="(e: Event) => handleDeleteMedia(item, e)"
                          title="删除"
                        >
                          <el-icon><Delete /></el-icon>
                        </el-button>
                      </div>
                    </div>
                    
                    <!-- 媒体信息 -->
                    <div class="media-card-body" @click="openMedia(item)">
                      <h4 class="media-title" :title="item.title">{{ item.title }}</h4>
                      <div class="media-stats">
                        <span class="stat-item">
                          <el-icon><View /></el-icon>
                          {{ formatNumber(item.views) }}
                        </span>
                        <span class="stat-item" v-if="item.likes">
                          <el-icon><Star /></el-icon>
                          {{ formatNumber(item.likes) }}
                        </span>
                      </div>
                      <div class="media-date">
                        {{ formatDate(item.add_date) }}
                      </div>
                    </div>
                  </div>
                </div>
                <el-empty v-else description="还没有上传视频" />
              </el-tab-pane>
              
              <el-tab-pane label="播放列表" name="playlists">
                <!-- 播放列表选择器和创建按钮 -->
                <div class="playlist-header">
                  <el-select 
                    v-if="userPlaylists.length"
                    v-model="selectedPlaylistId" 
                    @change="handlePlaylistChange"
                    placeholder="选择播放列表"
                    style="width: 300px"
                  >
                    <el-option label="所有播放列表" value="all" />
                    <el-option 
                      v-for="playlist in userPlaylists" 
                      :key="playlist.url"
                      :label="`${playlist.title} (${playlist.media_count || 0})`"
                      :value="extractPlaylistToken(playlist.url)"
                    />
                  </el-select>
                  
                  <el-button v-if="isOwnProfile" type="primary" @click="router.push('/playlists')">
                    <el-icon><FolderAdd /></el-icon>
                    创建播放列表
                  </el-button>
                </div>
                
                <!-- 播放列表媒体网格（使用历史记录样式） -->
                <el-skeleton :loading="loadingPlaylistMedia" animated>
                  <template #template>
                    <div class="items-grid">
                      <el-skeleton-item 
                        v-for="n in 12" 
                        :key="n"
                        variant="rect" 
                        style="width: 100%; padding-top: 56.25%; margin-bottom: 8px"
                      />
                    </div>
                  </template>
                  
                  <template #default>
                    <div v-if="playlistMedia.length" class="playlist-media-content">
                      <div class="items-grid">
                        <div 
                          v-for="item in playlistMedia" 
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
                          </div>
                        </div>
                      </div>
                    </div>
                    <el-empty 
                      v-else-if="!userPlaylists.length" 
                      description="还没有播放列表"
                    >
                      <el-button v-if="isOwnProfile" type="primary" @click="router.push('/playlists')">
                        <el-icon><FolderAdd /></el-icon>
                        创建第一个播放列表
                      </el-button>
                    </el-empty>
                    <el-empty 
                      v-else 
                      description="播放列表中还没有媒体"
                    />
                  </template>
                </el-skeleton>
              </el-tab-pane>
              
              <el-tab-pane label="关于" name="about">
                <div class="about-section">
                  <h3>关于 {{ user.name || user.username }}</h3>
                  <div v-if="user.description" class="about-description">
                    {{ user.description }}
                  </div>
                  <div v-else class="about-empty">
                    该用户还没有填写个人简介
                  </div>
                  
                  <div class="about-info">
                    <div class="info-item">
                      <span class="info-label">用户名：</span>
                      <span class="info-value">{{ user.username }}</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">加入时间：</span>
                      <span class="info-value">{{ user.date_added ? new Date(user.date_added).toLocaleDateString('zh-CN') : '未知' }}</span>
                    </div>
                  </div>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </div>
      </template>
    </el-skeleton>
    
    <!-- 添加到播放列表对话框 -->
    <el-dialog 
      v-model="addToPlaylistDialog" 
      title="添加到播放列表"
      width="500px"
    >
      <div class="playlist-dialog-content">
        <p class="dialog-hint">
          将选中的 {{ selectedMedia.length }} 个媒体添加到以下播放列表：
        </p>
        
        <el-checkbox-group v-model="selectedPlaylists" class="playlist-list">
          <el-checkbox 
            v-for="(playlist, index) in userPlaylists" 
            :key="index" 
            :label="index"
            class="playlist-item"
          >
            <div class="playlist-info">
              <span class="playlist-title">{{ playlist.title }}</span>
              <span class="playlist-count">{{ playlist.media_count || 0 }} 个视频</span>
            </div>
          </el-checkbox>
        </el-checkbox-group>
        
        <el-empty v-if="userPlaylists.length === 0" description="暂无播放列表" />
      </div>
      
      <template #footer>
        <el-button @click="addToPlaylistDialog = false">取消</el-button>
        <el-button 
          type="primary" 
          @click="handleBulkAddToPlaylist"
          :disabled="selectedPlaylists.length === 0"
        >
          <el-icon><Check /></el-icon>
          确定添加
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.user-profile {
  width: 100%;
}

.user-profile-container {
  width: 100%;
}

/* 对应后端模板的 page-profile-media 样式 */
#page-profile-media {
  width: 100%;
}

/* 页面头部 - 与其他组件保持一致 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 0 4px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 用户信息卡片 */
.profile-card {
  background: var(--mc-bg-primary, #fff);
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--mc-shadow, 0 2px 8px rgba(0, 0, 0, 0.08));
  margin-bottom: 24px;
}

[data-theme="dark"] .profile-card {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.profile-header {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 24px;
}

.profile-avatar {
  flex-shrink: 0;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 24px;
  font-weight: 600;
  color: var(--mc-text-primary, #2c3e50);
  margin: 0 0 8px 0;
}

[data-theme="dark"] .profile-name {
  color: #ffffff;
}

.profile-username {
  font-size: 16px;
  color: var(--mc-text-secondary, #666);
  margin-bottom: 12px;
}

[data-theme="dark"] .profile-username {
  color: #999;
}

.profile-description {
  font-size: 14px;
  color: var(--mc-text-secondary, #555);
  line-height: 1.6;
}

[data-theme="dark"] .profile-description {
  color: #cccccc;
}

.profile-stats {
  display: flex;
  gap: 32px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: var(--mc-text-primary, #2c3e50);
  margin-bottom: 4px;
}

[data-theme="dark"] .stat-value {
  color: #ffffff;
}

.stat-label {
  font-size: 12px;
  color: var(--mc-text-secondary, #888);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

[data-theme="dark"] .stat-label {
  color: #999;
}

/* 标签页 */
.profile-tabs {
  padding: 0 var(--mc-space-xl, 32px) var(--mc-space-xl, 32px);
}

/* 媒体网格布局 */
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 20px 0;
}

/* 播放列表头部 */
.playlist-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

[data-theme="dark"] .playlist-header {
  background: #2d2d2d;
}

/* 播放列表媒体内容区域 */
.playlist-media-content {
  min-height: 400px;
}

/* 媒体网格布局（复用历史记录样式） */
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
  height: 220px;
}

[data-theme="dark"] .item-thumb {
  background: #1a1a1a;
  border-color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

[data-theme="dark"] .item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
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

[data-theme="dark"] .thumb-image-container {
  background: #2a2a2a;
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

[data-theme="dark"] .thumb-title {
  color: #ffffff;
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

[data-theme="dark"] .thumb-meta {
  color: #999;
}

.playlist-card {
  background: var(--mc-bg-primary, #fff);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--mc-shadow, 0 2px 8px rgba(0, 0, 0, 0.08));
}

[data-theme="dark"] .playlist-card {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.playlist-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

[data-theme="dark"] .playlist-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.playlist-thumbnail {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 宽高比 */
  background: #f0f0f0;
  overflow: hidden;
}

[data-theme="dark"] .playlist-thumbnail {
  background: #2a2a2a;
}

.playlist-thumbnail img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.playlist-card:hover .playlist-thumbnail img {
  transform: scale(1.05);
}

.playlist-count-badge {
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

.playlist-info-card {
  padding: 12px;
}

.playlist-card-title {
  margin: 0 0 8px 0;
  font-size: 15px;
  font-weight: 600;
  color: #2c3e50;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

[data-theme="dark"] .playlist-card-title {
  color: #ffffff;
}

.playlist-card-description {
  margin: 0;
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

[data-theme="dark"] .playlist-card-description {
  color: #999;
}

.media-card {
  background: var(--mc-bg-primary, #fff);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: var(--mc-shadow, 0 2px 8px rgba(0, 0, 0, 0.08));
}

[data-theme="dark"] .media-card {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.media-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.media-card-thumb {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 宽高比 */
  background: #f0f0f0;
  overflow: hidden;
  cursor: pointer;
}

.media-thumbnail {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.media-card:hover .media-thumbnail {
  transform: scale(1.05);
}

/* 操作按钮 */
.media-actions {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: none;
  gap: 16px;
  z-index: 10;
}

.media-card-thumb:hover .media-actions {
  display: flex;
}

.media-card-thumb:hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  z-index: 5;
}

.media-actions .el-button {
  width: 48px;
  height: 48px;
  background: white !important;
  border: none !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  font-size: 20px;
}

.media-actions .el-button.el-button--primary {
  color: #409eff;
}

.media-actions .el-button.el-button--danger {
  color: #f56c6c;
}

.media-actions .el-button:hover {
  transform: scale(1.15);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.media-actions .el-button .el-icon {
  font-size: 20px;
}

.media-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.media-type-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(46, 204, 113, 0.9);
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.media-card-body {
  padding: 16px;
}

.media-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 12px 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 44px;
}

.media-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat-item .el-icon {
  font-size: 16px;
}

.media-date {
  font-size: 12px;
  color: #999;
}

/* 关于页面 */
.about-section {
  padding: var(--mc-space-lg, 24px) 0;
}

.about-section h3 {
  font-size: 20px;
  font-weight: var(--mc-font-medium, 600);
  margin-bottom: var(--mc-space-md, 16px);
  color: var(--mc-text, #2c3e50);
}

.about-description {
  font-size: 15px;
  color: var(--mc-text, #555);
  line-height: 1.8;
  margin-bottom: var(--mc-space-lg, 24px);
}

.about-empty {
  color: var(--mc-text-lighter, #999);
  font-style: italic;
  margin-bottom: var(--mc-space-lg, 24px);
}

.about-info {
  display: flex;
  flex-direction: column;
  gap: var(--mc-space, 12px);
}

.info-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}

.info-label {
  font-weight: var(--mc-font-medium, 600);
  color: var(--mc-text-light, #666);
  min-width: 100px;
}

.info-value {
  color: var(--mc-text, #333);
}

/* 批量操作工具栏 */
.bulk-toolbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 16px 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

[data-theme="dark"] .bulk-toolbar {
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

.bulk-toolbar-left {
  display: flex;
  align-items: center;
  color: white;
  font-size: 16px;
  font-weight: 600;
}

.bulk-toolbar-left :deep(.el-checkbox) {
  color: white;
}

.bulk-toolbar-left :deep(.el-checkbox__label) {
  color: white;
}

.bulk-toolbar-right {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.bulk-toolbar-right .el-button {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.bulk-toolbar-right .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

/* 媒体卡片选中状态 */
.media-card.is-selected {
  border: 3px solid #409eff;
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.2);
}

.media-checkbox {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 10;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px;
  padding: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

[data-theme="dark"] .media-checkbox {
  background: rgba(0, 0, 0, 0.8);
}

.media-checkbox :deep(.el-checkbox__inner) {
  width: 24px;
  height: 24px;
}

.media-checkbox :deep(.el-checkbox__inner::after) {
  width: 8px;
  height: 12px;
  left: 7px;
}

/* 播放列表对话框 */
.playlist-dialog-content {
  max-height: 400px;
  overflow-y: auto;
}

.dialog-hint {
  color: #606266;
  font-size: 14px;
  margin-bottom: 16px;
  padding: 12px;
  background: #f4f4f5;
  border-radius: 6px;
  border-left: 4px solid #409eff;
}

[data-theme="dark"] .dialog-hint {
  color: #cccccc;
  background: #2d2d2d;
}

.playlist-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.playlist-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
  background: #fafafa;
}

[data-theme="dark"] .playlist-item {
  background: #1a1a1a;
  border-color: #333;
}

.playlist-item:hover {
  border-color: #409eff;
  background: #ecf5ff;
}

[data-theme="dark"] .playlist-item:hover {
  background: #2d2d2d;
}

.playlist-item :deep(.el-checkbox__label) {
  width: 100%;
}

.playlist-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.playlist-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

[data-theme="dark"] .playlist-title {
  color: #ffffff;
}

.playlist-count {
  font-size: 13px;
  color: #909399;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
  
  .playlists-grid {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .page-header h1 {
    font-size: 24px;
  }
  
  .profile-card {
    padding: 16px;
  }
  
  .profile-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 16px;
  }
  
  .profile-stats {
    justify-content: center;
    gap: 24px;
  }
  
  .profile-tabs {
    padding: 0 16px 16px;
  }
  
  .media-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
  
  .playlists-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .profile-card {
    padding: 12px;
  }
  
  .profile-name {
    font-size: 20px;
  }
  
  .profile-stats {
    gap: 16px;
  }
  
  .stat-value {
    font-size: 18px;
  }
  
  .media-grid {
    grid-template-columns: 1fr;
  }
  
  .playlists-grid {
    grid-template-columns: 1fr;
  }
  
  .media-title {
    font-size: 14px;
  }
}
</style>
