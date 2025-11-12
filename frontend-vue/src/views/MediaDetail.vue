<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { MediaAPI, CommentsAPI, PlaylistsAPI } from '@/api'
import type { MediaDetail, Paginated, CommentItem, UserActionStatus, PlaylistDetail } from '@/api'
import VideoPlayer from '@/components/VideoPlayer.vue'
import CommentSection from '@/components/CommentSection.vue'
import PdfViewer from '@/components/media/PdfViewer.vue'
import ImageViewer from '@/components/media/ImageViewer.vue'
import MediaRating from '@/components/media/MediaRating.vue'
import ReportDialog from '@/components/media/ReportDialog.vue'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Star, 
  StarFilled,
  Share, 
  Download, 
  Document,
  Warning,
  FolderAdd
} from '@element-plus/icons-vue'

const route = useRoute()
const auth = useAuthStore()
const token = computed(() => String(route.params.token))

const loading = ref(false)
const detail = ref<MediaDetail | null>(null)
const isMediaAllowedType = ref(true)

const commentsLoading = ref(false)
const comments = ref<Paginated<CommentItem> | null>(null)
const newComment = ref('')

// 用户操作状态
const userLiked = ref(false)
const userDisliked = ref(false)
const actionLoading = ref(false)
const hasRecordedWatch = ref(false)  // 标记是否已记录观看
const showReportDialog = ref(false)  // 举报对话框显示状态

// 播放列表相关
const showPlaylistDialog = ref(false)  // 播放列表对话框显示状态
const userPlaylists = ref<PlaylistDetail[]>([])  // 用户的播放列表
const selectedPlaylists = ref<string[]>([])  // 选中的播放列表tokens
const loadingPlaylists = ref(false)  // 加载播放列表状态

// 支持的媒体类型
const allowedMediaTypes = ['video', 'audio', 'image', 'pdf']

// 加载用户的点赞状态
// 注意：后端GET /api/v1/media/{token}/actions 接口只返回举报记录（仅媒体所有者/编辑可访问）
// 不是用户的点赞/不喜欢状态，所以我们不调用该接口
async function loadUserActions() {
  // 加载用户的点赞状态 - 现在后端提供了获取用户操作状态的接口
  if (!auth.isLoggedIn) return
  
  try {
    const response: UserActionStatus = await MediaAPI.getMediaActions(token.value)
    userLiked.value = response.user_liked
    userDisliked.value = response.user_disliked
  } catch (error) {
    console.error('加载用户操作状态失败:', error)
    // 静默失败，不影响页面功能
  }
}

async function loadDetail() {
  loading.value = true
  try {
    console.log('📥 开始加载媒体详情, token:', token.value)
    detail.value = await MediaAPI.getMediaDetail(token.value)
    console.log('✅ 媒体详情加载成功:', detail.value)
    console.log('  - 标题:', detail.value.title)
    console.log('  - 类型:', detail.value.media_type)
    console.log('  - HLS URL:', detail.value.hls_info?.playlist_url)
    console.log('  - 预览URL:', detail.value.preview_url)
    console.log('  - 原始URL:', detail.value.original_media_url)
    console.log('  - 海报URL:', detail.value.poster_url)
    console.log('  - 缩略图URL:', detail.value.thumbnail_url)
    
    // 检查媒体类型是否支持 - 对应后端的 is_media_allowed_type
    if (detail.value?.media_type) {
      isMediaAllowedType.value = allowedMediaTypes.includes(detail.value.media_type)
      console.log('  - 是否支持该类型:', isMediaAllowedType.value)
    }
    
    // 添加SEO元数据 - 对应后端模板的headermeta部分
    if (detail.value && detail.value.state !== 'private') {
      addSEOMetadata(detail.value)
    }
    
    // 加载用户操作状态
    await loadUserActions()
  } catch (error) {
    console.error('❌ 加载媒体详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 添加SEO元数据 - 对应后端模板的结构化数据
function addSEOMetadata(media: MediaDetail) {
  // 设置页面标题
  document.title = `${media.title} - MediaCMS`
  
  // 添加meta描述
  const description = media.description || ''
  let metaDesc = document.querySelector('meta[name="description"]')
  if (!metaDesc) {
    metaDesc = document.createElement('meta')
    metaDesc.setAttribute('name', 'description')
    document.head.appendChild(metaDesc)
  }
  metaDesc.setAttribute('content', description)
  
  // 添加Open Graph标签
  const ogTags = [
    { property: 'og:title', content: `${media.title} - MediaCMS` },
    { property: 'og:url', content: window.location.href },
    { property: 'og:description', content: description },
    { property: 'og:updated_time', content: media.edit_date || '' }
  ]
  
  if (media.media_type === 'video') {
    ogTags.push({ property: 'og:type', content: 'video.other' })
    ogTags.push({ property: 'og:image', content: media.poster_url || '' })
  } else if (media.media_type === 'audio') {
    ogTags.push({ property: 'og:type', content: 'website' })
    ogTags.push({ property: 'og:image', content: media.poster_url || '' })
  } else if (media.media_type === 'image') {
    ogTags.push({ property: 'og:type', content: 'website' })
    ogTags.push({ property: 'og:image', content: media.original_media_url || '' })
  } else {
    ogTags.push({ property: 'og:type', content: 'website' })
  }
  
  // 添加或更新OG标签
  ogTags.forEach(tag => {
    let metaTag = document.querySelector(`meta[property="${tag.property}"]`)
    if (!metaTag) {
      metaTag = document.createElement('meta')
      metaTag.setAttribute('property', tag.property)
      document.head.appendChild(metaTag)
    }
    metaTag.setAttribute('content', tag.content)
  })
  
  // 添加结构化数据 - 对应后端模板的JSON-LD
  const existingScript = document.querySelector('script[type="application/ld+json"]')
  if (existingScript) {
    existingScript.remove()
  }
  
  const script = document.createElement('script')
  script.type = 'application/ld+json'
  
  const structuredData: Record<string, any> = {
    "@context": "http://schema.org",
    "name": `${media.title} - MediaCMS`,
    "url": window.location.href,
    "description": description,
    "uploadDate": media.add_date,
    "dateModified": media.edit_date,
    "potentialAction": {
      "@type": "ViewAction",
      "target": window.location.href
    }
  }
  
  if (media.media_type === 'video') {
    structuredData["@type"] = "VideoObject"
    structuredData.thumbnailUrl = [media.poster_url || '']
    structuredData.embedUrl = `${window.location.origin}/embed?m=${token.value}`
    structuredData.duration = `T${media.duration || 0}S`
  } else if (media.media_type === 'audio') {
    structuredData["@type"] = "AudioObject"
    structuredData.duration = `T${media.duration || 0}S`
  } else if (media.media_type === 'image') {
    structuredData["@type"] = "ImageObject"
  } else {
    structuredData["@type"] = "MediaObject"
  }
  
  script.textContent = JSON.stringify(structuredData)
  document.head.appendChild(script)
}

// 原有的评论加载函数现在由CommentSection组件内部管理
// 保持向后兼容性
async function loadComments() {
  commentsLoading.value = true
  try {
    comments.value = await CommentsAPI.listMediaComments(token.value)
  } finally {
    commentsLoading.value = false
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return
  await CommentsAPI.createMediaComment(token.value, { text: newComment.value })
  newComment.value = ''
  await loadComments()
}

// 格式化日期函数
function formatDate(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 格式化时长函数
function formatDuration(seconds?: number) {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 获取视频源URL（处理GIF预览问题）
function getVideoSource(media: MediaDetail): string | null {
  // 检查preview_url是否是GIF文件（后端转码问题）
  const previewUrl = media.preview_url
  const isGif = previewUrl?.toLowerCase().endsWith('.gif')
  
  if (isGif) {
    console.warn('⚠️ 预览URL是GIF文件，将使用原始视频文件')
    return media.original_media_url || null
  }
  
  // 优先使用预览URL（转码后的视频），否则使用原始URL
  return previewUrl || media.original_media_url || null
}

// 点赞功能（支持切换）
// 后端设计：like和dislike支持切换操作，可以点赞/取消点赞
async function handleLike() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  actionLoading.value = true
  try {
    // 执行点赞操作（后端会自动处理切换逻辑）
    const response = await MediaAPI.createUserMediaAction(token.value, 'like')
    
    if (response.action_type === 'unlike') {
      // 取消点赞
      userLiked.value = false
      if (detail.value && detail.value.likes !== undefined && detail.value.likes > 0) {
        detail.value.likes = detail.value.likes - 1
      }
      ElMessage.success('已取消点赞')
    } else {
      // 点赞
      userLiked.value = true
      if (detail.value) {
        detail.value.likes = (detail.value.likes || 0) + 1
      }
      // 如果之前有点击过不喜欢，需要取消不喜欢状态
      if (userDisliked.value) {
        userDisliked.value = false
        if (detail.value && detail.value.dislikes !== undefined && detail.value.dislikes > 0) {
          detail.value.dislikes = detail.value.dislikes - 1
        }
      }
      ElMessage.success('点赞成功！')
    }
  } catch (error) {
    console.error('点赞失败:', error)
    ElMessage.error('点赞失败，请稍后再试')
  } finally {
    actionLoading.value = false
  }
}

// 不喜欢功能（支持切换）
// 后端设计：dislike支持切换操作，可以标记不喜欢/取消不喜欢
async function handleDislike() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  actionLoading.value = true
  try {
    // 执行不喜欢操作（后端会自动处理切换逻辑）
    const response = await MediaAPI.createUserMediaAction(token.value, 'dislike')
    
    if (response.action_type === 'undislike') {
      // 取消不喜欢
      userDisliked.value = false
      if (detail.value && detail.value.dislikes !== undefined && detail.value.dislikes > 0) {
        detail.value.dislikes = detail.value.dislikes - 1
      }
      ElMessage.success('已取消不喜欢标记')
    } else {
      // 标记为不喜欢
      userDisliked.value = true
      if (detail.value) {
        detail.value.dislikes = (detail.value.dislikes || 0) + 1
      }
      // 如果之前有点击过点赞，需要取消点赞状态
      if (userLiked.value) {
        userLiked.value = false
        if (detail.value && detail.value.likes !== undefined && detail.value.likes > 0) {
          detail.value.likes = detail.value.likes - 1
        }
      }
      ElMessage.success('已标记为不喜欢')
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败，请稍后再试')
  } finally {
    actionLoading.value = false
  }
}

// 记录音频观看历史
const recordAudioWatch = async () => {
  if (hasRecordedWatch.value) {
    return  // 已记录过，不重复记录
  }
  
  try {
    hasRecordedWatch.value = true
    await MediaAPI.createUserMediaAction(token.value, 'watch')
    console.log('✅ 已记录音频观看历史')
  } catch (error) {
    console.error('❌ 记录音频观看历史失败:', error)
    hasRecordedWatch.value = false  // 失败时重置，允许重试
  }
}

// 记录图片观看历史
const recordImageWatch = async () => {
  if (hasRecordedWatch.value) {
    return  // 已记录过，不重复记录
  }
  
  try {
    hasRecordedWatch.value = true
    await MediaAPI.createUserMediaAction(token.value, 'watch')
    console.log('✅ 已记录图片观看历史')
  } catch (error) {
    console.error('❌ 记录图片观看历史失败:', error)
    hasRecordedWatch.value = false  // 失败时重置，允许重试
  }
}

// 分享功能
function handleShare() {
  const url = window.location.href
  if (navigator.share) {
    navigator.share({
      title: detail.value?.title || '',
      text: detail.value?.description || '',
      url: url
    }).then(() => {
      ElMessage.success('分享成功')
    }).catch(() => {
      copyToClipboard(url)
    })
  } else {
    copyToClipboard(url)
  }
}

// 复制到剪贴板
function copyToClipboard(text: string) {
  if (navigator.clipboard) {
    navigator.clipboard.writeText(text).then(() => {
      ElMessage.success('链接已复制到剪贴板')
    })
  } else {
    // 降级方案
    const textarea = document.createElement('textarea')
    textarea.value = text
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    document.body.removeChild(textarea)
    ElMessage.success('链接已复制到剪贴板')
  }
}

// 下载功能
function handleDownload() {
  if (!detail.value?.original_media_url) {
    ElMessage.error('下载链接不可用')
    return
  }
  
  const link = document.createElement('a')
  link.href = detail.value.original_media_url
  link.download = detail.value.title || 'media'
  link.target = '_blank'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  ElMessage.success('开始下载')
}

// 举报功能
function handleReport() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  showReportDialog.value = true
}

// 举报成功回调
function handleReported() {
  console.log('✅ 举报已提交')
  // 可以在这里添加额外的处理逻辑
}

// 加载用户的播放列表
async function loadUserPlaylists() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  loadingPlaylists.value = true
  try {
    const res = await PlaylistsAPI.listPlaylists()
    const allPlaylists = (res?.results || []) as PlaylistDetail[]
    // 只显示当前用户的播放列表
    userPlaylists.value = allPlaylists.filter(
      playlist => playlist.user === auth.profile?.username
    )
    console.log(`加载了 ${userPlaylists.value.length} 个播放列表`)
  } catch (error) {
    console.error('加载播放列表失败:', error)
    ElMessage.error('加载播放列表失败')
  } finally {
    loadingPlaylists.value = false
  }
}

// 打开添加到播放列表对话框
async function handleAddToPlaylist() {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }
  
  await loadUserPlaylists()
  
  if (userPlaylists.value.length === 0) {
    ElMessageBox.confirm(
      '您还没有创建播放列表，是否现在创建？',
      '提示',
      {
        confirmButtonText: '去创建',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).then(() => {
      // 跳转到播放列表页面
      window.open('/playlists', '_blank')
    }).catch(() => {
      // 用户取消
    })
    return
  }
  
  selectedPlaylists.value = []
  showPlaylistDialog.value = true
}

// 从播放列表URL中提取token
function extractPlaylistToken(url: string): string {
  const parts = url.split('/')
  return parts[parts.length - 1] || parts[parts.length - 2]
}

// 确认添加到播放列表
async function confirmAddToPlaylist() {
  if (selectedPlaylists.value.length === 0) {
    ElMessage.warning('请选择至少一个播放列表')
    return
  }
  
  if (!detail.value) return
  
  // 使用路由中的token或detail中的friendly_token
  const mediaToken = token.value || detail.value.friendly_token
  
  console.log('📤 开始添加媒体到播放列表')
  console.log('  - 媒体Token:', mediaToken)
  console.log('  - 选中的播放列表:', selectedPlaylists.value)
  
  try {
    let successCount = 0
    let failCount = 0
    
    for (const playlistUrl of selectedPlaylists.value) {
      try {
        const playlistToken = extractPlaylistToken(playlistUrl)
        console.log('  - 播放列表Token:', playlistToken)
        console.log('  - 完整URL:', playlistUrl)
        
        // 调用后端API添加媒体到播放列表
        const result = await PlaylistsAPI.addMediaToPlaylist(playlistToken, mediaToken)
        console.log('✅ 添加成功:', result)
        successCount++
      } catch (error: any) {
        console.error('❌ 添加到播放列表失败:', error)
        console.error('  - 错误详情:', error.response?.data)
        failCount++
      }
    }
    
    if (successCount > 0) {
      ElMessage.success(`成功添加到 ${successCount} 个播放列表`)
    }
    if (failCount > 0) {
      ElMessage.warning(`${failCount} 个播放列表添加失败`)
    }
    
    showPlaylistDialog.value = false
    selectedPlaylists.value = []
  } catch (error) {
    console.error('添加到播放列表失败:', error)
    ElMessage.error('添加失败，请稍后重试')
  }
}

// 跳转创建播放列表
function handleCreatePlaylist() {
  showPlaylistDialog.value = false
  window.open('/playlists', '_blank')
}

onMounted(async () => {
  await loadDetail()
  await loadComments()
  await loadUserActions()  // 加载用户的点赞/不喜欢状态
})
</script>

<template>
  <!-- 对应后端模板的条件检查 {% if is_media_allowed_type %} -->
  <div v-if="isMediaAllowedType">
    <!-- 对应后端模板的 <div id="page-media"></div> -->
    <div id="page-media">
      <el-skeleton :loading="loading" animated>
        <template #template>
          <div class="media-skeleton">
            <el-skeleton-item variant="rect" style="width: 100%; height: 400px; margin-bottom: 16px;" />
            <el-skeleton-item variant="h1" style="width: 80%; margin-bottom: 8px;" />
            <el-skeleton-item variant="text" style="width: 60%; margin-bottom: 16px;" />
            <el-skeleton-item variant="text" style="width: 100%;" />
          </div>
        </template>
        
        <template #default>
          <div v-if="detail" class="media-detail-container">
            <!-- 媒体播放器区域 -->
            <div class="media-player-section">
              <div class="player-wrapper" :class="{ 'image-wrapper': detail.media_type === 'image' }">
                <VideoPlayer
                  v-if="detail.media_type === 'video'"
                  :hls="detail.hls_info?.playlist_url || null"
                  :src="getVideoSource(detail)"
                  :poster="detail.poster_url || detail.thumbnail_url || null"
                  :controls="true"
                  :autoplay="true"
                  :media-token="token"
                />
                
                <audio 
                  v-else-if="detail.media_type === 'audio'"
                  :src="detail.original_media_url || detail.preview_url || ''"
                  :poster="detail.poster_url || detail.thumbnail_url || ''"
                  controls
                  autoplay
                  class="audio-player"
                  @play="recordAudioWatch"
                />
                
                <ImageViewer
                  v-else-if="detail.media_type === 'image'"
                  :src="detail.original_media_url || detail.preview_url || ''"
                  :alt="detail.title"
                  :filename="detail.title"
                  @load="recordImageWatch"
                />
                
                <PdfViewer
                  v-else-if="detail.media_type === 'pdf'"
                  :src="detail.original_media_url || detail.preview_url || ''"
                  :filename="detail.title + '.pdf'"
                />
                
                <div v-else class="unsupported-media">
                  <el-icon size="48"><Document /></el-icon>
                  <p>{{ detail.title }}</p>
                  <el-button 
                    v-if="detail?.original_media_url" 
                    type="primary"
                    @click="handleDownload"
                  >
                    下载文件
                  </el-button>
                </div>
              </div>
            </div>
            
            <!-- 媒体信息区域 -->
            <div class="media-info-section">
              <h1 class="media-title">{{ detail.title }}</h1>
              
              <div class="media-meta">
                <div class="author-info">
                  <img 
                    v-if="detail.author_thumbnail" 
                    :src="detail.author_thumbnail" 
                    :alt="detail.author_name"
                    class="author-avatar"
                  />
                  <div class="author-details">
                    <div class="author-name">{{ detail.author_name }}</div>
                    <div class="media-stats">
                      {{ detail.views || 0 }} 次观看 · 
                      {{ formatDate(detail.add_date) }}
                      <span v-if="detail.duration"> · {{ formatDuration(detail.duration) }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="media-actions">
                  <el-button-group>
                    <el-button 
                      :type="userLiked ? 'primary' : 'default'"
                      :loading="actionLoading"
                      @click="handleLike"
                    >
                      <el-icon v-if="userLiked"><StarFilled /></el-icon>
                      <el-icon v-else><Star /></el-icon>
                      {{ detail.likes || 0 }}
                    </el-button>
                    <el-button 
                      :type="userDisliked ? 'danger' : 'default'"
                      :loading="actionLoading"
                      @click="handleDislike"
                    >
                      👎
                      {{ detail.dislikes || 0 }}
                    </el-button>
                  </el-button-group>
                  
                  <el-button @click="handleShare">
                    <el-icon><Share /></el-icon>
                    分享
                  </el-button>
                  
                  <el-button 
                    v-if="detail.original_media_url" 
                    @click="handleDownload"
                  >
                    <el-icon><Download /></el-icon>
                    下载
                  </el-button>
                  
                  <el-button 
                    @click="handleAddToPlaylist"
                    type="success"
                    plain
                  >
                    <el-icon><FolderAdd /></el-icon>
                    添加到播放列表
                  </el-button>
                  
                  <el-button 
                    @click="handleReport"
                    type="warning"
                    plain
                  >
                    <el-icon><Warning /></el-icon>
                    举报
                  </el-button>
                </div>
              </div>
              
              <div v-if="detail.description" class="media-description">
                <div class="description-content">{{ detail.description }}</div>
              </div>
              
              <!-- 分类和标签 -->
              <div v-if="detail.categories_info?.length || detail.tags_info?.length" class="media-taxonomy">
                <div v-if="detail.categories_info?.length" class="categories">
                  <strong>分类：</strong>
                  <el-tag 
                    v-for="category in detail.categories_info" 
                    :key="category.title"
                    type="primary"
                    class="taxonomy-tag"
                  >
                    {{ category.title }}
                  </el-tag>
                </div>
                
                <div v-if="detail.tags_info?.length" class="tags">
                  <strong>标签：</strong>
                  <el-tag 
                    v-for="tag in detail.tags_info" 
                    :key="tag.title"
                    class="taxonomy-tag"
                  >
                    {{ tag.title }}
                  </el-tag>
                </div>
              </div>
            </div>
            
            <!-- 评分区域 -->
            <MediaRating :media-token="token" />
            
            <!-- 增强的评论区域 -->
            <CommentSection :media-token="token" />
          </div>
        </template>
      </el-skeleton>
    </div>
    
    <!-- 举报对话框 -->
    <ReportDialog 
      v-model="showReportDialog"
      :media-token="token"
      @reported="handleReported"
    />
    
    <!-- 添加到播放列表对话框 -->
    <el-dialog
      v-model="showPlaylistDialog"
      title="添加到播放列表"
      width="420px"
    >
      <div v-loading="loadingPlaylists" class="playlist-dialog-body">
        <div v-if="userPlaylists.length > 0">
          <el-checkbox-group v-model="selectedPlaylists" class="playlist-list">
            <div 
              v-for="playlist in userPlaylists" 
              :key="playlist.url"
              class="playlist-option"
            >
              <el-checkbox :label="playlist.url">
                <span class="option-title">{{ playlist.title }}</span>
              </el-checkbox>
              <span class="option-badge">{{ playlist.media_count }}</span>
            </div>
          </el-checkbox-group>
        </div>
        
        <el-empty 
          v-else-if="!loadingPlaylists"
          description="还没有播放列表"
          :image-size="100"
        >
          <el-button type="primary" size="small" @click="handleCreatePlaylist">
            创建播放列表
          </el-button>
        </el-empty>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPlaylistDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="confirmAddToPlaylist"
            :disabled="selectedPlaylists.length === 0"
          >
            添加 ({{ selectedPlaylists.length }})
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
  
  <!-- 对应后端模板的不支持媒体类型提示 -->
  <div v-else class="user-action-form-wrap">
    <div class="user-action-form-inner">
      <el-result
        icon="warning"
        title="不支持的媒体类型"
        sub-title="This media type is not supported."
      >
        <template #extra>
          <el-button type="primary" @click="$router.go(-1)">返回</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style scoped>
/* 对应后端模板引入的 media.css 样式 */
#page-media {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.media-detail-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.media-player-section {
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.player-wrapper {
  position: relative;
  width: 100%;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  max-height: 85vh;
}

/* 图片查看器专用样式 */
.player-wrapper.image-wrapper {
  min-height: 400px;
  background: #0a0a0a;
}

.audio-player {
  width: 100%;
  height: 60px;
}

.unsupported-media {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  color: white;
  padding: 40px;
}

.media-info-section {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.media-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 16px 0;
  line-height: 1.3;
}

.media-meta {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.author-name {
  font-weight: 600;
  color: var(--mc-text-primary);
  margin-bottom: 4px;
}

.media-stats {
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
}

.media-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.media-description {
  margin: 20px 0;
  padding: 16px;
  background: var(--mc-bg-secondary);
  border-radius: 8px;
}

.description-content {
  white-space: pre-wrap;
  line-height: 1.6;
  color: var(--mc-text-primary);
}

.media-taxonomy {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 16px;
}

.categories, .tags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.taxonomy-tag {
  margin-right: 4px;
}

.comments-section {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comments-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin: 0 0 20px 0;
}

.comments-count {
  color: var(--mc-text-secondary);
  font-weight: normal;
}

.comment-form {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.comments-list {
  margin-top: 24px;
}

.comment-skeleton {
  display: flex;
  margin-bottom: 20px;
}

.comments-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  background: var(--mc-bg-secondary);
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.comment-author {
  font-weight: 600;
  color: var(--mc-text-primary);
}

.comment-date {
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
}

.comment-text {
  white-space: pre-wrap;
  line-height: 1.5;
  color: var(--mc-text-primary);
}

/* 对应后端模板的 user-action-form-wrap 样式 */
.user-action-form-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  padding: 40px 20px;
}

.user-action-form-inner {
  background: white;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  #page-media {
    padding: 12px;
  }
  
  .media-info-section,
  .comments-section {
    padding: 16px;
  }
  
  .media-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .media-actions {
    width: 100%;
    justify-content: flex-start;
  }
  
  .comment-item {
    padding: 12px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] #page-media {
  background: #0a0a0a;
}

[data-theme="dark"] .media-player-section {
  background: #0a0a0a;
}

[data-theme="dark"] .player-wrapper.image-wrapper {
  background: #0a0a0a;
}

[data-theme="dark"] .media-info-section {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .media-title {
  color: #ffffff;
}

[data-theme="dark"] .author-name {
  color: #ffffff;
}

[data-theme="dark"] .media-stats {
  color: #999;
}

[data-theme="dark"] .media-description {
  background: #2a2a2a;
}

[data-theme="dark"] .description-content {
  color: #cccccc;
}

[data-theme="dark"] .media-taxonomy strong {
  color: #ffffff;
}

[data-theme="dark"] .comments-section {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .comments-title {
  color: #ffffff;
}

[data-theme="dark"] .comments-count {
  color: #999;
}

[data-theme="dark"] .comment-item {
  background: #2a2a2a;
}

[data-theme="dark"] .comment-author {
  color: #ffffff;
}

[data-theme="dark"] .comment-date {
  color: #888;
}

[data-theme="dark"] .comment-text {
  color: #cccccc;
}

[data-theme="dark"] .user-action-form-inner {
  background: #1a1a1a;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
  color: #ffffff;
}

/* 播放列表对话框样式 */
.playlist-dialog-body {
  padding: 8px 0;
}

.playlist-list {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.playlist-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.2s;
  cursor: pointer;
  background-color: #fafafa;
}

.playlist-option:last-child {
  margin-bottom: 0;
}

.playlist-option:hover {
  background-color: #f0f2f5;
}

.playlist-option :deep(.el-checkbox) {
  flex: 1;
  margin: 0;
}

.playlist-option :deep(.el-checkbox__label) {
  padding-left: 8px;
}

.option-title {
  font-size: 14px;
  color: #303133;
}

.option-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 22px;
  padding: 0 8px;
  font-size: 12px;
  color: #606266;
  background-color: #e4e7ed;
  border-radius: 11px;
  margin-left: 12px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 暗黑模式 */
[data-theme="dark"] .playlist-option {
  background-color: #2a2a2a;
}

[data-theme="dark"] .playlist-option:hover {
  background-color: #333;
}

[data-theme="dark"] .option-title {
  color: #e5e5e5;
}

[data-theme="dark"] .option-badge {
  background-color: #4a4a4a;
  color: #b0b0b0;
}
</style>
