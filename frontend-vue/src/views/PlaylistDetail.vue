<script setup lang="ts">
import { onMounted, ref, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { PlaylistsAPI } from '@/api'
import type { PlaylistDetail } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Edit, 
  Delete, 
  Share, 
  Link, 
  Plus,
  Close,
  Check,
  Rank,
  ArrowLeft
} from '@element-plus/icons-vue'
import Sortable from 'sortablejs'

const route = useRoute()
const router = useRouter()
const token = String(route.params.token || '')

const loading = ref(false)
const detail = ref<PlaylistDetail | null>(null)
const addToken = ref('')

// 拖拽排序相关
let sortableInstance: Sortable | null = null
const isDragging = ref(false)

// 编辑模式相关
const editMode = ref(false)
const editForm = ref({
  title: '',
  description: ''
})
const saving = ref(false)

// 分享对话框
const shareDialogVisible = ref(false)
const shareUrl = ref('')

// 返回上一页
const handleBack = () => {
  router.back()
}

async function load() {
  loading.value = true
  try {
    detail.value = await PlaylistsAPI.getPlaylistDetail(token)
    // 生成分享链接
    shareUrl.value = window.location.origin + (detail.value.url || '')
    
    // 加载完成后初始化拖拽
    await nextTick()
    initSortable()
  } finally {
    loading.value = false
  }
}

async function addMedia() {
  if (!addToken.value) return
  try {
    await PlaylistsAPI.playlistMediaOp(token, { type: 'add', media_friendly_token: addToken.value })
    ElMessage.success('媒体已添加')
    addToken.value = ''
    await load()
  } catch {
    ElMessage.error('添加失败，请检查 Token 是否正确')
  }
}

async function removeMedia(mediaToken: string) {
  try {
    await ElMessageBox.confirm(
      '确定要从播放列表中移除这个媒体吗？',
      '移除媒体',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await PlaylistsAPI.playlistMediaOp(token, { type: 'remove', media_friendly_token: mediaToken })
    ElMessage.success('已移除')
    await load()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('移除失败')
    }
  }
}

// 开启编辑模式
function startEdit() {
  if (!detail.value) return
  editForm.value.title = detail.value.title
  editForm.value.description = detail.value.description || ''
  editMode.value = true
}

// 取消编辑
function cancelEdit() {
  editMode.value = false
  editForm.value = { title: '', description: '' }
}

// 保存编辑
async function saveEdit() {
  if (!editForm.value.title.trim()) {
    ElMessage.warning('请输入播放列表标题')
    return
  }
  
  saving.value = true
  try {
    await PlaylistsAPI.updatePlaylist(token, {
      title: editForm.value.title,
      description: editForm.value.description
    })
    
    ElMessage.success('保存成功')
    editMode.value = false
    await load()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('保存失败')
    }
  } finally {
    saving.value = false
  }
}

// 删除播放列表
async function deletePlaylist() {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个播放列表吗？此操作不可恢复！',
      '删除播放列表',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    await PlaylistsAPI.deletePlaylist(token)
    ElMessage.success('删除成功')
    router.push('/')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 分享功能
function openShareDialog() {
  shareDialogVisible.value = true
}

// 复制链接
function copyShareLink() {
  navigator.clipboard.writeText(shareUrl.value).then(() => {
    ElMessage.success('链接已复制到剪贴板')
  }).catch(() => {
    ElMessage.error('复制失败，请手动复制')
  })
}

// 分享到社交媒体
function shareToSocial(platform: string) {
  const title = detail.value?.title || '播放列表'
  const url = encodeURIComponent(shareUrl.value)
  const text = encodeURIComponent(title)
  
  let shareLink = ''
  
  switch (platform) {
    case 'twitter':
      shareLink = `https://twitter.com/intent/tweet?text=${text}&url=${url}`
      break
    case 'facebook':
      shareLink = `https://www.facebook.com/sharer/sharer.php?u=${url}`
      break
    case 'weibo':
      shareLink = `https://service.weibo.com/share/share.php?title=${text}&url=${url}`
      break
    case 'wechat':
      ElMessage.info('请使用微信扫一扫功能分享')
      return
  }
  
  if (shareLink) {
    window.open(shareLink, '_blank', 'width=600,height=400')
  }
}

// 格式化时长
function formatDuration(seconds: number): string {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`
}

// 格式化日期
function formatDate(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days} 天前`
  if (days < 30) return `${Math.floor(days / 7)} 周前`
  if (days < 365) return `${Math.floor(days / 30)} 个月前`
  return date.toLocaleDateString()
}

// 初始化拖拽排序
function initSortable() {
  // 销毁旧实例
  if (sortableInstance) {
    sortableInstance.destroy()
    sortableInstance = null
  }
  
  // 获取媒体列表容器
  const el = document.querySelector('.media-list')
  if (!el || !detail.value || !detail.value.playlist_media || detail.value.playlist_media.length === 0) {
    return
  }
  
  // 创建拖拽实例
  sortableInstance = new Sortable(el as HTMLElement, {
    animation: 150,
    handle: '.drag-handle',  // 只能通过拖拽图标拖动
    ghostClass: 'sortable-ghost',
    dragClass: 'sortable-drag',
    onStart: () => {
      isDragging.value = true
    },
    onEnd: async (evt) => {
      isDragging.value = false
      
      const oldIndex = evt.oldIndex
      const newIndex = evt.newIndex
      
      if (oldIndex === undefined || newIndex === undefined || oldIndex === newIndex) {
        return
      }
      
      if (!detail.value || !detail.value.playlist_media) return
      
      // 获取被移动的媒体
      const movedMedia = detail.value.playlist_media[oldIndex]
      if (!movedMedia) return  // 类型安全检查
      
      const newOrder = newIndex + 1  // 后端序号从1开始
      
      try {
        // 调用API更新顺序
        await PlaylistsAPI.playlistMediaOp(token, {
          type: 'ordering',
          media_friendly_token: movedMedia.friendly_token,
          ordering: newOrder
        })
        
        // 更新本地数据（已经由sortable自动更新了DOM顺序）
        const items = detail.value.playlist_media.splice(oldIndex, 1)
        if (items[0]) {
          detail.value.playlist_media.splice(newIndex, 0, items[0])
        }
        
        ElMessage.success('排序已更新')
      } catch {
        ElMessage.error('排序更新失败')
        // 失败时重新加载列表
        await load()
      }
    }
  })
}

onMounted(load)
</script>

<template>
  <section class="home-sec playlist-detail-page">
    <div class="home-sec-head">
      <div class="home-sec-left">
        <el-button 
          :icon="ArrowLeft" 
          circle 
          @click="handleBack"
          class="back-button"
          title="返回"
        />
        <div class="home-sec-title">播放列表详情</div>
      </div>
      <div class="action-buttons" v-if="detail && !editMode">
        <el-button type="primary" @click="startEdit">
          <el-icon><Edit /></el-icon>
          编辑
        </el-button>
        <el-button type="info" @click="openShareDialog">
          <el-icon><Share /></el-icon>
          分享
        </el-button>
        <el-button type="danger" @click="deletePlaylist">
          <el-icon><Delete /></el-icon>
          删除
        </el-button>
      </div>
    </div>

    <el-card v-if="detail" class="playlist-card">
      <!-- 编辑模式 -->
      <div v-if="editMode" class="edit-mode">
        <h3 class="edit-title">编辑播放列表信息</h3>
        <el-form :model="editForm" label-position="top">
          <el-form-item label="标题" required>
            <el-input 
              v-model="editForm.title" 
              placeholder="请输入播放列表标题"
              maxlength="100"
              show-word-limit
            />
          </el-form-item>
          <el-form-item label="描述">
            <el-input 
              v-model="editForm.description" 
              type="textarea"
              :rows="4"
              placeholder="请输入播放列表描述"
              maxlength="500"
              show-word-limit
            />
          </el-form-item>
          <el-form-item>
            <el-space>
              <el-button type="primary" :loading="saving" @click="saveEdit">
                <el-icon><Check /></el-icon>
                保存
              </el-button>
              <el-button @click="cancelEdit">
                <el-icon><Close /></el-icon>
                取消
              </el-button>
            </el-space>
          </el-form-item>
        </el-form>
      </div>

      <!-- 查看模式 -->
      <div v-else>
        <div class="playlist-header">
          <div class="playlist-info">
            <h2 class="playlist-title">{{ detail.title }}</h2>
            <p class="playlist-description" v-if="detail.description">
              {{ detail.description }}
            </p>
            <div class="playlist-meta">
              <span>创建者：{{ detail.user }}</span>
              <span class="separator">•</span>
              <span>{{ detail.media_count }} 个视频</span>
              <span class="separator" v-if="detail.add_date">•</span>
              <span v-if="detail.add_date">创建于 {{ new Date(detail.add_date).toLocaleDateString() }}</span>
            </div>
          </div>
          <div class="add-media-section">
            <el-input 
              v-model="addToken" 
              placeholder="输入媒体 Token"
              class="add-input"
            >
              <template #append>
                <el-button 
                  type="primary" 
                  :disabled="!addToken" 
                  @click="addMedia"
                  :icon="Plus"
                >
                  添加媒体
                </el-button>
              </template>
            </el-input>
          </div>
        </div>

        <el-divider />

        <!-- 媒体列表 -->
        <div v-if="detail.playlist_media && detail.playlist_media.length > 0" class="media-list">
          <div 
            v-for="(m, index) in detail.playlist_media" 
            :key="m.friendly_token" 
            class="media-item"
            :class="{ 'is-dragging': isDragging }"
          >
            <!-- 拖拽图标 -->
            <div class="drag-handle" title="拖拽排序">
              <el-icon><Rank /></el-icon>
            </div>
            <div class="media-index">{{ index + 1 }}</div>
            <div class="media-thumbnail">
              <img 
                :src="m.thumbnail_url || '/placeholder.jpg'" 
                :alt="m.title"
                @error="(e) => (e.target as HTMLImageElement).src = '/placeholder.jpg'"
              />
              <div class="media-duration" v-if="m.duration">
                {{ formatDuration(m.duration) }}
              </div>
            </div>
            <div class="media-info">
              <h4 class="media-title">{{ m.title }}</h4>
              <div class="media-meta">
                <span>{{ m.views || 0 }} 次观看</span>
                <span class="separator">•</span>
                <span>{{ m.media_type || '视频' }}</span>
                <span class="separator" v-if="m.add_date">•</span>
                <span v-if="m.add_date">{{ formatDate(m.add_date) }}</span>
              </div>
            </div>
            <div class="media-actions">
              <el-button 
                type="danger" 
                size="small" 
                @click="removeMedia(m.friendly_token)"
                :icon="Delete"
              >
                移除
              </el-button>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <el-empty 
          v-else 
          description="播放列表为空，请添加媒体"
          :image-size="120"
        />
      </div>
    </el-card>

    <!-- 分享对话框 -->
    <el-dialog 
      v-model="shareDialogVisible" 
      title="分享播放列表"
      width="500px"
      class="share-dialog"
    >
      <div class="share-content">
        <div class="share-link-section">
          <el-input 
            v-model="shareUrl" 
            readonly
            class="share-link-input"
          >
            <template #append>
              <el-button @click="copyShareLink" :icon="Link">
                复制链接
              </el-button>
            </template>
          </el-input>
        </div>

        <el-divider>分享到社交媒体</el-divider>

        <div class="social-share-buttons">
          <el-button @click="shareToSocial('twitter')" class="share-btn twitter">
            <span class="social-icon">𝕏</span>
            Twitter
          </el-button>
          <el-button @click="shareToSocial('facebook')" class="share-btn facebook">
            <span class="social-icon">f</span>
            Facebook
          </el-button>
          <el-button @click="shareToSocial('weibo')" class="share-btn weibo">
            <span class="social-icon">微</span>
            微博
          </el-button>
          <el-button @click="shareToSocial('wechat')" class="share-btn wechat">
            <span class="social-icon">微</span>
            微信
          </el-button>
        </div>
      </div>
    </el-dialog>
  </section>
</template>

<style scoped>
.playlist-detail-page {
  max-width: 1200px;
  margin: 0 auto;
}

.home-sec-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.home-sec-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-button {
  flex-shrink: 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
}

.playlist-card {
  margin-bottom: 20px;
}

/* 编辑模式样式 */
.edit-mode {
  padding: 20px;
}

.edit-title {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #303133;
}

/* 播放列表头部 */
.playlist-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
  padding: 20px;
  background: #f9fafc;
  border-radius: 8px;
  margin-bottom: 20px;
}

.playlist-info {
  flex: 1;
}

.playlist-title {
  margin: 0 0 12px 0;
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.playlist-description {
  margin: 0 0 12px 0;
  color: #606266;
  line-height: 1.6;
}

.playlist-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
}

.separator {
  color: #dcdfe6;
}

.add-media-section {
  min-width: 350px;
}

.add-input {
  width: 100%;
}

/* 媒体列表样式 */
.media-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.media-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s;
}

.media-item:hover {
  background: #e9ecef;
  transform: translateX(4px);
}

.media-item.is-dragging {
  cursor: move;
}

/* 拖拽手柄样式 */
.drag-handle {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  color: #909399;
  transition: color 0.3s;
  flex-shrink: 0;
}

.drag-handle:hover {
  color: #409eff;
}

.drag-handle:active {
  cursor: grabbing;
}

/* Sortable拖拽样式 */
.sortable-ghost {
  opacity: 0.4;
  background: #ecf5ff;
  border: 2px dashed #409eff;
}

.sortable-drag {
  opacity: 1;
  background: #ffffff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: rotate(2deg);
}

.media-index {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #409eff;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  flex-shrink: 0;
}

.media-thumbnail {
  position: relative;
  width: 160px;
  height: 90px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
  background: #dcdfe6;
}

.media-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.media-duration {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
}

.media-info {
  flex: 1;
  min-width: 0;
}

.media-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 13px;
}

.media-actions {
  flex-shrink: 0;
}

/* 分享对话框样式 */
.share-content {
  padding: 20px 0;
}

.share-link-section {
  margin-bottom: 24px;
}

.share-link-input {
  width: 100%;
}

.social-share-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  font-size: 14px;
  border-radius: 6px;
}

.social-icon {
  font-size: 18px;
  font-weight: 700;
}

.share-btn.twitter {
  background: #1da1f2;
  color: white;
  border-color: #1da1f2;
}

.share-btn.twitter:hover {
  background: #1a8cd8;
  border-color: #1a8cd8;
}

.share-btn.facebook {
  background: #1877f2;
  color: white;
  border-color: #1877f2;
}

.share-btn.facebook:hover {
  background: #1664d8;
  border-color: #1664d8;
}

.share-btn.weibo {
  background: #e6162d;
  color: white;
  border-color: #e6162d;
}

.share-btn.weibo:hover {
  background: #c61428;
  border-color: #c61428;
}

.share-btn.wechat {
  background: #07c160;
  color: white;
  border-color: #07c160;
}

.share-btn.wechat:hover {
  background: #06a552;
  border-color: #06a552;
}

/* 暗色模式 */
[data-theme="dark"] .edit-title,
[data-theme="dark"] .playlist-title,
[data-theme="dark"] .media-title {
  color: #e5e7eb;
}

[data-theme="dark"] .playlist-description {
  color: #a8abb2;
}

[data-theme="dark"] .playlist-meta,
[data-theme="dark"] .media-meta {
  color: #909399;
}

[data-theme="dark"] .media-item {
  background: #1a1a1a;
}

[data-theme="dark"] .media-item:hover {
  background: #262626;
}

[data-theme="dark"] .media-thumbnail {
  background: #333;
}

[data-theme="dark"] .drag-handle {
  color: #a8abb2;
}

[data-theme="dark"] .drag-handle:hover {
  color: #409eff;
}

[data-theme="dark"] .sortable-ghost {
  background: #1a3a52;
  border-color: #409eff;
}

[data-theme="dark"] .sortable-drag {
  background: #1a1a1a;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-sec-head {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .action-buttons {
    justify-content: stretch;
  }

  .action-buttons .el-button {
    flex: 1;
  }

  .playlist-header {
    flex-direction: column;
  }

  .add-media-section {
    width: 100%;
    min-width: auto;
  }

  .media-item {
    flex-direction: column;
    align-items: stretch;
  }

  .media-index {
    align-self: flex-start;
  }

  .media-thumbnail {
    width: 100%;
    height: 180px;
  }

  .social-share-buttons {
    grid-template-columns: 1fr;
  }
}
</style>
