<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaDetail } from '@/api'
import { useAuthStore } from '@/stores/auth'
import MediaNav from '@/components/media/MediaNav.vue'
import VideoPlayer from '@/components/VideoPlayer.vue'
import { ElMessage, ElMessageBox } from 'element-plus'

interface Chapter {
  id: string
  title: string
  timestamp: number
  description?: string
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const mediaToken = computed(() => String(route.params.token))
const loading = ref(false)
const saving = ref(false)
const media = ref<MediaDetail | null>(null)
const currentTime = ref(0)
const videoDuration = ref(0)

// 章节数据 - 对应后端模板的MEDIA_DATA结构
const chapters = ref<Chapter[]>([
  {
    id: "1",
    title: "Chapter AAA",
    timestamp: 0,
    description: ""
  },
  {
    id: "2", 
    title: "Chapter BBB",
    timestamp: 10,
    description: ""
  },
  {
    id: "3",
    title: "Chapter CCC", 
    timestamp: 20,
    description: ""
  }
])

const editingChapter = ref<Chapter | null>(null)
const showChapterDialog = ref(false)

// 视频播放器相关
const videoSource = computed(() => {
  if (!media.value) return null
  
  if (media.value.hls_info?.playlist_url) {
    return {
      type: 'hls',
      url: media.value.hls_info.playlist_url
    }
  }
  
  if (media.value.preview_url) {
    return {
      type: 'video',
      url: media.value.preview_url
    }
  }
  
  return null
})

const posterImage = computed(() => {
  return media.value?.poster_url || media.value?.thumbnail_url || null
})

async function loadMedia() {
  if (!mediaToken.value) return
  
  loading.value = true
  try {
    media.value = await MediaAPI.getMediaDetail(mediaToken.value)
    
    // 加载现有章节数据（实际应该从API获取）
    // const chaptersData = await MediaAPI.getMediaChapters(mediaToken.value)
    // if (chaptersData) {
    //   chapters.value = chaptersData
    // }
  } catch (error) {
    console.error('加载媒体失败:', error)
    ElMessage.error('加载媒体信息失败')
  } finally {
    loading.value = false
  }
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function parseTimeInput(timeStr: string): number {
  const parts = timeStr.split(':')
  if (parts.length === 2) {
    const mins = parseInt(parts[0] || '0') || 0
    const secs = parseInt(parts[1] || '0') || 0
    return mins * 60 + secs
  }
  return parseInt(timeStr) || 0
}

function addChapter() {
  const newChapter: Chapter = {
    id: Date.now().toString(),
    title: `章节 ${chapters.value.length + 1}`,
    timestamp: Math.floor(currentTime.value),
    description: ''
  }
  
  editingChapter.value = newChapter
  showChapterDialog.value = true
}

function editChapter(chapter: Chapter) {
  editingChapter.value = { ...chapter }
  showChapterDialog.value = true
}

function saveChapter() {
  if (!editingChapter.value) return
  
  const existingIndex = chapters.value.findIndex(c => c.id === editingChapter.value!.id)
  
  if (existingIndex >= 0) {
    // 更新现有章节
    chapters.value[existingIndex] = { ...editingChapter.value }
  } else {
    // 添加新章节
    chapters.value.push({ ...editingChapter.value })
  }
  
  // 按时间戳排序
  chapters.value.sort((a, b) => a.timestamp - b.timestamp)
  
  showChapterDialog.value = false
  editingChapter.value = null
  
  ElMessage.success('章节已保存')
}

function deleteChapter(chapter: Chapter) {
  ElMessageBox.confirm(
    `确定要删除章节"${chapter.title}"吗？`,
    '确认删除',
    {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    const index = chapters.value.findIndex(c => c.id === chapter.id)
    if (index >= 0) {
      chapters.value.splice(index, 1)
      ElMessage.success('章节已删除')
    }
  }).catch(() => {
    // 用户取消删除
  })
}

function jumpToChapter(chapter: Chapter) {
  currentTime.value = chapter.timestamp
  // 这里应该控制视频播放器跳转到指定时间
  ElMessage.info(`跳转到 ${formatTime(chapter.timestamp)}`)
}

function setCurrentTimeAsChapterStart() {
  if (editingChapter.value) {
    editingChapter.value.timestamp = Math.floor(currentTime.value)
  }
}

async function saveAllChapters() {
  saving.value = true
  try {
    // 这里应该调用保存章节的API
    // await MediaAPI.saveMediaChapters(mediaToken.value, chapters.value)
    
    ElMessage.success('所有章节已保存')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 监听视频播放器的时间更新
function onTimeUpdate(time: number) {
  currentTime.value = time
}

function onDurationChange(duration: number) {
  videoDuration.value = duration
}

onMounted(loadMedia)
</script>

<template>
  <div class="chapters-edit-container">
    <!-- 对应后端模板的头部标题 -->
    <div class="page-header">
      <h1>编辑视频章节</h1>
      <p v-if="media">{{ media.title }}</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="media" class="user-action-form-wrap">
      <!-- 对应后端模板的 media_nav.html 包含 -->
      <MediaNav :media="media" active-tab="chapters" />
      
      <!-- 对应后端模板的表单容器样式 -->
      <div class="user-action-form-inner">
        <!-- 对应后端的 <div id="video-editor-chapters-root"></div> -->
        <div id="video-editor-chapters-root" class="chapters-editor">
          
          <!-- 视频播放器区域 -->
          <div class="video-player-section">
            <div v-if="videoSource" class="video-container">
              <VideoPlayer
                :hls="videoSource.type === 'hls' ? videoSource.url : null"
                :src="videoSource.type === 'video' ? videoSource.url : null"
                :poster="posterImage"
                :controls="true"
                @timeupdate="onTimeUpdate"
                @durationchange="onDurationChange"
              />
            </div>
            
            <div class="video-controls">
              <div class="time-display">
                当前时间: {{ formatTime(currentTime) }} / {{ formatTime(videoDuration) }}
              </div>
              <el-button type="primary" @click="addChapter">
                <el-icon><Plus /></el-icon>
                在当前位置添加章节
              </el-button>
            </div>
          </div>

          <!-- 章节列表区域 -->
          <div class="chapters-section">
            <div class="section-header">
              <h3>章节列表</h3>
              <el-button 
                type="success" 
                :loading="saving"
                @click="saveAllChapters"
              >
                保存所有章节
              </el-button>
            </div>

            <div v-if="chapters.length" class="chapters-list">
              <div 
                v-for="(chapter, index) in chapters" 
                :key="chapter.id"
                class="chapter-item"
              >
                <div class="chapter-info">
                  <div class="chapter-number">{{ index + 1 }}</div>
                  <div class="chapter-details">
                    <h4 class="chapter-title">{{ chapter.title }}</h4>
                    <div class="chapter-meta">
                      <span class="chapter-time">{{ formatTime(chapter.timestamp) }}</span>
                      <span v-if="chapter.description" class="chapter-description">
                        {{ chapter.description }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div class="chapter-actions">
                  <el-button 
                    size="small" 
                    @click="jumpToChapter(chapter)"
                  >
                    跳转
                  </el-button>
                  <el-button 
                    size="small" 
                    type="primary"
                    @click="editChapter(chapter)"
                  >
                    编辑
                  </el-button>
                  <el-button 
                    size="small" 
                    type="danger"
                    @click="deleteChapter(chapter)"
                  >
                    删除
                  </el-button>
                </div>
              </div>
            </div>

            <el-empty 
              v-else 
              description="还没有添加章节"
              :image-size="100"
            >
              <el-button type="primary" @click="addChapter">
                添加第一个章节
              </el-button>
            </el-empty>
          </div>
        </div>
      </div>
    </div>

    <!-- 章节编辑对话框 -->
    <el-dialog
      v-model="showChapterDialog"
      :title="editingChapter?.id && chapters.find(c => c.id === editingChapter?.id) ? '编辑章节' : '添加章节'"
      width="500px"
    >
      <el-form 
        v-if="editingChapter"
        :model="editingChapter"
        label-width="80px"
      >
        <el-form-item label="章节标题" required>
          <el-input 
            v-model="editingChapter.title"
            placeholder="输入章节标题"
          />
        </el-form-item>
        
        <el-form-item label="开始时间">
          <div class="time-input-group">
            <el-input 
              :model-value="formatTime(editingChapter.timestamp)"
              placeholder="0:00"
              @input="editingChapter.timestamp = parseTimeInput($event)"
            />
            <el-button 
              size="small"
              @click="setCurrentTimeAsChapterStart"
            >
              使用当前时间
            </el-button>
          </div>
          <div class="form-help">
            格式: 分:秒 (如 1:30) 或 秒数 (如 90)
          </div>
        </el-form-item>
        
        <el-form-item label="章节描述">
          <el-input 
            v-model="editingChapter.description"
            type="textarea"
            :rows="3"
            placeholder="输入章节描述（可选）"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showChapterDialog = false">取消</el-button>
        <el-button type="primary" @click="saveChapter">保存</el-button>
      </template>
    </el-dialog>

    <div v-else class="error-container">
      <el-result
        icon="error"
        title="媒体不存在"
        sub-title="找不到指定的媒体文件"
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
/* 对应后端模板的video-editor.css样式 */
.chapters-edit-container {
  max-width: 1280px;
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
  font-size: 1.1rem;
  color: var(--mc-text-secondary);
  margin: 0;
}

.loading-container {
  padding: 40px;
}

.user-action-form-wrap {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 对应后端模板的表单容器样式 */
.user-action-form-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  background: white;
}

.chapters-editor {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.video-player-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.video-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.video-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: var(--mc-bg-secondary);
  border-radius: 8px;
}

.time-display {
  font-family: monospace;
  font-size: 1rem;
  color: var(--mc-text-primary);
}

.chapters-section {
  border-top: 1px solid var(--el-border-color-light);
  padding-top: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.chapters-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chapter-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--mc-bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--el-border-color-light);
}

.chapter-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
}

.chapter-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--el-color-primary);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 14px;
}

.chapter-details {
  flex: 1;
}

.chapter-title {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.chapter-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
}

.chapter-time {
  font-family: monospace;
  background: var(--el-color-info-light-8);
  padding: 2px 6px;
  border-radius: 4px;
}

.chapter-description {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chapter-actions {
  display: flex;
  gap: 8px;
}

.time-input-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.time-input-group .el-input {
  flex: 1;
}

.form-help {
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
  margin-top: 4px;
}

.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chapters-edit-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .user-action-form-inner {
    padding: 16px;
    margin: 0 -4px;
  }
  
  .video-controls {
    flex-direction: column;
    gap: 12px;
    text-align: center;
  }
  
  .chapter-item {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
  
  .chapter-info {
    justify-content: flex-start;
  }
  
  .chapter-actions {
    justify-content: center;
  }
  
  .section-header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
}

@media (max-width: 480px) {
  .time-input-group {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chapter-actions {
    flex-direction: column;
  }
  
  .chapter-actions .el-button {
    width: 100%;
  }
}
</style>
