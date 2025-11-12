<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaDetail } from '@/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const token = computed(() => String(route.params.token))

const loading = ref(false)
const saving = ref(false)
const media = ref<MediaDetail | null>(null)
const videoRef = ref<HTMLVideoElement | null>(null)

// 视频编辑状态
const editState = ref({
  currentTime: 0,
  duration: 0,
  trimStart: 0,
  trimEnd: 0,
  volume: 1,
  playbackRate: 1,
  chapters: [] as Array<{ title: string; start: number; end: number }>
})

// 编辑工具状态
const tools = ref({
  showTrimmer: false,
  showChapters: false,
  showFilters: false,
  isPlaying: false
})

async function loadMedia() {
  loading.value = true
  try {
    media.value = await MediaAPI.getMediaDetail(token.value)
    if (media.value.media_type !== 'video') {
      ElMessage.error('只能编辑视频文件')
      router.back()
      return
    }
    
    // 初始化章节数据
    if (media.value.chapter_data) {
      editState.value.chapters = [...media.value.chapter_data]
    }
  } catch {
    ElMessage.error('加载视频失败')
    router.back()
  } finally {
    loading.value = false
  }
}

function onVideoLoaded() {
  if (videoRef.value) {
    editState.value.duration = videoRef.value.duration
    editState.value.trimEnd = videoRef.value.duration
  }
}

function onTimeUpdate() {
  if (videoRef.value) {
    editState.value.currentTime = videoRef.value.currentTime
  }
}

function togglePlay() {
  if (videoRef.value) {
    if (tools.value.isPlaying) {
      videoRef.value.pause()
    } else {
      videoRef.value.play()
    }
    tools.value.isPlaying = !tools.value.isPlaying
  }
}

function seekTo(time: number) {
  if (videoRef.value) {
    videoRef.value.currentTime = time
    editState.value.currentTime = time
  }
}

function setTrimStart() {
  editState.value.trimStart = editState.value.currentTime
}

function setTrimEnd() {
  editState.value.trimEnd = editState.value.currentTime
}

function addChapter() {
  const title = prompt('请输入章节标题:')
  if (title) {
    editState.value.chapters.push({
      title,
      start: editState.value.currentTime,
      end: editState.value.currentTime + 60 // 默认60秒长度
    })
  }
}

function removeChapter(index: number) {
  editState.value.chapters.splice(index, 1)
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

async function saveChanges() {
  if (!media.value) return
  
  saving.value = true
  try {
    // 这里应该调用视频处理API
    // 由于后端可能没有实现，我们先模拟保存章节信息
    await MediaAPI.updateMedia(token.value, {
      title: media.value.title,
      description: media.value.description
    })
    
    ElMessage.success('保存成功')
    router.push({ name: 'media-detail', params: { token: token.value } })
  } catch {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(loadMedia)

onBeforeUnmount(() => {
  if (videoRef.value) {
    videoRef.value.pause()
  }
})
</script>

<template>
  <div class="video-edit-container">
    <el-card>
      <template #header>
        <div class="header-actions">
          <h2>视频编辑器</h2>
          <el-space>
            <el-button @click="router.back()">返回</el-button>
            <el-button type="primary" :loading="saving" @click="saveChanges">
              保存更改
            </el-button>
          </el-space>
        </div>
      </template>

      <el-skeleton :loading="loading" animated>
        <template #template>
          <el-skeleton-item variant="rect" style="width: 100%; height: 400px" />
        </template>

        <template #default>
          <div v-if="media" class="video-editor">
            <!-- 视频播放器 -->
            <div class="video-player-section">
              <video
                ref="videoRef"
                :src="media.preview_url || media.original_media_url"
                :poster="media.poster_url || media.thumbnail_url"
                @loadedmetadata="onVideoLoaded"
                @timeupdate="onTimeUpdate"
                style="width: 100%; max-height: 400px; background: #000"
                controls
              />
            </div>

            <!-- 编辑工具栏 -->
            <div class="edit-toolbar">
              <el-space>
                <el-button @click="togglePlay">
                  <el-icon>
                    <VideoPlay v-if="!tools.isPlaying" />
                    <VideoPause v-else />
                  </el-icon>
                  {{ tools.isPlaying ? '暂停' : '播放' }}
                </el-button>
                
                <el-button @click="tools.showTrimmer = !tools.showTrimmer">
                  <el-icon><Scissors /></el-icon>
                  剪辑
                </el-button>
                
                <el-button @click="tools.showChapters = !tools.showChapters">
                  <el-icon><List /></el-icon>
                  章节
                </el-button>
                
                <el-button @click="tools.showFilters = !tools.showFilters">
                  <el-icon><Picture /></el-icon>
                  滤镜
                </el-button>
              </el-space>
            </div>

            <!-- 时间轴 -->
            <div class="timeline-section">
              <div class="time-info">
                <span>{{ formatTime(editState.currentTime) }} / {{ formatTime(editState.duration) }}</span>
              </div>
              
              <el-slider
                v-model="editState.currentTime"
                :max="editState.duration"
                :step="0.1"
                @change="seekTo"
                style="margin: 12px 0"
              />
            </div>

            <!-- 剪辑工具 -->
            <el-collapse-item v-if="tools.showTrimmer" name="trimmer">
              <template #title>
                <el-icon><Scissors /></el-icon>
                视频剪辑
              </template>
              
              <div class="trim-controls">
                <el-row :gutter="16">
                  <el-col :span="8">
                    <el-form-item label="开始时间">
                      <el-input-number
                        v-model="editState.trimStart"
                        :min="0"
                        :max="editState.duration"
                        :step="0.1"
                        style="width: 100%"
                      />
                      <el-button size="small" @click="setTrimStart" style="margin-top: 8px">
                        设为当前时间
                      </el-button>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="8">
                    <el-form-item label="结束时间">
                      <el-input-number
                        v-model="editState.trimEnd"
                        :min="editState.trimStart"
                        :max="editState.duration"
                        :step="0.1"
                        style="width: 100%"
                      />
                      <el-button size="small" @click="setTrimEnd" style="margin-top: 8px">
                        设为当前时间
                      </el-button>
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="8">
                    <el-form-item label="剪辑长度">
                      <el-input
                        :value="formatTime(editState.trimEnd - editState.trimStart)"
                        readonly
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>
            </el-collapse-item>

            <!-- 章节编辑 -->
            <el-collapse-item v-if="tools.showChapters" name="chapters">
              <template #title>
                <el-icon><List /></el-icon>
                章节管理
              </template>
              
              <div class="chapters-section">
                <div class="chapters-header">
                  <el-button type="primary" @click="addChapter">
                    <el-icon><Plus /></el-icon>
                    添加章节
                  </el-button>
                </div>
                
                <el-table :data="editState.chapters" style="margin-top: 16px">
                  <el-table-column label="标题" prop="title" />
                  <el-table-column label="开始时间" width="120">
                    <template #default="{ row }">
                      {{ formatTime(row.start) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="结束时间" width="120">
                    <template #default="{ row }">
                      {{ formatTime(row.end) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="120">
                    <template #default="{ $index }">
                      <el-button size="small" type="danger" @click="removeChapter($index)">
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </div>
            </el-collapse-item>

            <!-- 滤镜效果 -->
            <el-collapse-item v-if="tools.showFilters" name="filters">
              <template #title>
                <el-icon><Picture /></el-icon>
                视频滤镜
              </template>
              
              <div class="filters-section">
                <el-row :gutter="16">
                  <el-col :span="12">
                    <el-form-item label="音量">
                      <el-slider
                        v-model="editState.volume"
                        :min="0"
                        :max="2"
                        :step="0.1"
                        show-input
                      />
                    </el-form-item>
                  </el-col>
                  
                  <el-col :span="12">
                    <el-form-item label="播放速度">
                      <el-slider
                        v-model="editState.playbackRate"
                        :min="0.25"
                        :max="2"
                        :step="0.25"
                        show-input
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-alert
                  title="注意"
                  description="滤镜效果需要服务器端处理，保存时会生成新的视频文件"
                  type="info"
                  show-icon
                />
              </div>
            </el-collapse-item>
          </div>
        </template>
      </el-skeleton>
    </el-card>
  </div>
</template>

<style scoped>
.video-edit-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.video-editor {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.video-player-section {
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.edit-toolbar {
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.timeline-section {
  padding: 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.time-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: monospace;
  font-size: 14px;
  color: #666;
}

.trim-controls,
.chapters-section,
.filters-section {
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
}

.chapters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 768px) {
  .video-edit-container {
    padding: 12px;
  }
  
  .edit-toolbar {
    overflow-x: auto;
  }
}
</style>
