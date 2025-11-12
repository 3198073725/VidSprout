<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MediaAPI } from '@/api'

const router = useRouter()

const recording = ref(false)
const preparing = ref(false)
const uploading = ref(false)
const recordedBlob = ref<Blob | null>(null)
const previewUrl = ref<string>('')
const videoRef = ref<HTMLVideoElement | null>(null)
const previewRef = ref<HTMLVideoElement | null>(null)

let mediaRecorder: MediaRecorder | null = null
let stream: MediaStream | null = null
let recordedChunks: Blob[] = []

const recordOptions = ref({
  includeAudio: true,
  includeSystemAudio: false,
  quality: 'high' as 'high' | 'medium' | 'low',
  frameRate: 30
})

const recordInfo = ref({
  duration: 0,
  startTime: 0,
  fileSize: 0
})

const uploadForm = ref({
  title: '',
  description: ''
})

// 检查浏览器支持
const isSupported = ref(false)

onMounted(() => {
  checkSupport()
})

function checkSupport() {
  isSupported.value = !!(navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia)
  if (!isSupported.value) {
    ElMessage.error('您的浏览器不支持屏幕录制功能')
  }
}

async function startRecording() {
  if (!isSupported.value) return
  
  preparing.value = true
  
  try {
    // 获取屏幕录制权限
    const displayStream = await navigator.mediaDevices.getDisplayMedia({
      video: {
        frameRate: recordOptions.value.frameRate
      },
      audio: recordOptions.value.includeSystemAudio
    })

    // 如果需要麦克风音频
    let audioStream: MediaStream | null = null
    if (recordOptions.value.includeAudio) {
      try {
        audioStream = await navigator.mediaDevices.getUserMedia({ audio: true })
      } catch (error) {
        console.warn('无法获取麦克风权限:', error)
        ElMessage.warning('无法获取麦克风权限，将只录制系统音频')
      }
    }

    // 合并音视频流
    const tracks = [...displayStream.getTracks()]
    if (audioStream) {
      tracks.push(...audioStream.getAudioTracks())
    }
    
    stream = new MediaStream(tracks)
    
    // 显示预览
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }

    // 设置录制器
    const options: MediaRecorderOptions = {
      mimeType: getSupportedMimeType()
    }
    
    mediaRecorder = new MediaRecorder(stream, options)
    recordedChunks = []

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = () => {
      recordedBlob.value = new Blob(recordedChunks, { type: 'video/webm' })
      recordInfo.value.fileSize = recordedBlob.value.size
      previewUrl.value = URL.createObjectURL(recordedBlob.value)
      
      // 显示录制结果
      if (previewRef.value) {
        previewRef.value.src = previewUrl.value
      }
      
      // 生成默认标题
      const now = new Date()
      uploadForm.value.title = `屏幕录制 ${now.toLocaleString()}`
    }

    // 监听用户停止分享屏幕
    displayStream.getVideoTracks()[0].addEventListener('ended', () => {
      stopRecording()
    })

    // 开始录制
    mediaRecorder.start(1000) // 每秒收集一次数据
    recording.value = true
    recordInfo.value.startTime = Date.now()
    
    // 开始计时
    startTimer()
    
    ElMessage.success('开始录制屏幕')
  } catch (error: any) {
    console.error('录制失败:', error)
    ElMessage.error('录制失败: ' + (error.message || '未知错误'))
  } finally {
    preparing.value = false
  }
}

function stopRecording() {
  if (mediaRecorder && recording.value) {
    mediaRecorder.stop()
    recording.value = false
    
    // 停止所有轨道
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
    }
    
    // 清除预览
    if (videoRef.value) {
      videoRef.value.srcObject = null
    }
    
    ElMessage.success('录制完成')
  }
}

function getSupportedMimeType(): string {
  const types = [
    'video/webm;codecs=vp9,opus',
    'video/webm;codecs=vp8,opus',
    'video/webm',
    'video/mp4'
  ]
  
  for (const type of types) {
    if (MediaRecorder.isTypeSupported(type)) {
      return type
    }
  }
  
  return 'video/webm'
}

let timerInterval: number | null = null

function startTimer() {
  timerInterval = setInterval(() => {
    if (recording.value) {
      recordInfo.value.duration = Math.floor((Date.now() - recordInfo.value.startTime) / 1000)
    }
  }, 1000)
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

function formatFileSize(bytes: number): string {
  const sizes = ['B', 'KB', 'MB', 'GB']
  if (bytes === 0) return '0 B'
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
}

function resetRecording() {
  recordedBlob.value = null
  previewUrl.value = ''
  recordInfo.value = { duration: 0, startTime: 0, fileSize: 0 }
  uploadForm.value = { title: '', description: '' }
}

async function uploadRecording() {
  if (!recordedBlob.value) {
    ElMessage.warning('没有录制内容可上传')
    return
  }
  
  if (!uploadForm.value.title.trim()) {
    ElMessage.warning('请输入视频标题')
    return
  }
  
  uploading.value = true
  
  try {
    const file = new File([recordedBlob.value], `screen-record-${Date.now()}.webm`, {
      type: recordedBlob.value.type
    })
    
    await MediaAPI.createMedia({
      media_file: file,
      title: uploadForm.value.title,
      description: uploadForm.value.description
    })
    
    ElMessage.success('上传成功')
    router.push('/')
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

onBeforeUnmount(() => {
  if (timerInterval) {
    clearInterval(timerInterval)
  }
  
  if (recording.value) {
    stopRecording()
  }
  
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})
</script>

<template>
  <div class="screen-record-container">
    <el-card>
      <template #header>
        <div class="header-actions">
          <h2>屏幕录制</h2>
          <el-button @click="router.back()">返回</el-button>
        </div>
      </template>

      <div v-if="!isSupported" class="not-supported">
        <el-result
          icon="warning"
          title="不支持屏幕录制"
          sub-title="您的浏览器不支持屏幕录制功能，请使用Chrome、Firefox或Edge浏览器"
        />
      </div>

      <div v-else class="record-content">
        <!-- 录制设置 -->
        <el-card v-if="!recording && !recordedBlob" class="settings-card">
          <template #header>
            <h3>录制设置</h3>
          </template>
          
          <el-form :model="recordOptions" label-width="120px">
            <el-form-item label="录制质量">
              <el-radio-group v-model="recordOptions.quality">
                <el-radio value="high">高质量</el-radio>
                <el-radio value="medium">中等质量</el-radio>
                <el-radio value="low">低质量</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="帧率">
              <el-select v-model="recordOptions.frameRate">
                <el-option label="60 FPS" :value="60" />
                <el-option label="30 FPS" :value="30" />
                <el-option label="24 FPS" :value="24" />
                <el-option label="15 FPS" :value="15" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="音频设置">
              <el-checkbox v-model="recordOptions.includeAudio">
                录制麦克风音频
              </el-checkbox>
              <br>
              <el-checkbox v-model="recordOptions.includeSystemAudio">
                录制系统音频
              </el-checkbox>
            </el-form-item>
          </el-form>
          
          <div class="start-actions">
            <el-button
              type="primary"
              size="large"
              :loading="preparing"
              @click="startRecording"
            >
              <el-icon><VideoCamera /></el-icon>
              开始录制
            </el-button>
          </div>
        </el-card>

        <!-- 录制中 -->
        <div v-if="recording" class="recording-section">
          <div class="recording-header">
            <div class="recording-status">
              <el-icon class="recording-icon"><VideoCameraFilled /></el-icon>
              <span class="recording-text">正在录制</span>
              <span class="recording-time">{{ formatTime(recordInfo.duration) }}</span>
            </div>
            
            <el-button type="danger" @click="stopRecording">
              <el-icon><VideoCamera /></el-icon>
              停止录制
            </el-button>
          </div>
          
          <div class="preview-container">
            <video
              ref="videoRef"
              autoplay
              muted
              style="width: 100%; max-height: 400px; background: #000; border-radius: 8px"
            />
          </div>
          
          <el-alert
            title="录制提示"
            description="点击停止录制按钮或关闭屏幕分享窗口来结束录制"
            type="info"
            show-icon
          />
        </div>

        <!-- 录制完成 -->
        <div v-if="recordedBlob" class="result-section">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <h3>录制预览</h3>
                </template>
                
                <video
                  ref="previewRef"
                  controls
                  style="width: 100%; max-height: 300px; background: #000; border-radius: 8px"
                />
                
                <div class="record-stats">
                  <el-descriptions :column="1" size="small">
                    <el-descriptions-item label="录制时长">
                      {{ formatTime(recordInfo.duration) }}
                    </el-descriptions-item>
                    <el-descriptions-item label="文件大小">
                      {{ formatFileSize(recordInfo.fileSize) }}
                    </el-descriptions-item>
                  </el-descriptions>
                </div>
              </el-card>
            </el-col>
            
            <el-col :span="12">
              <el-card>
                <template #header>
                  <h3>上传设置</h3>
                </template>
                
                <el-form :model="uploadForm" label-width="80px">
                  <el-form-item label="标题" required>
                    <el-input
                      v-model="uploadForm.title"
                      placeholder="请输入视频标题"
                    />
                  </el-form-item>
                  
                  <el-form-item label="描述">
                    <el-input
                      v-model="uploadForm.description"
                      type="textarea"
                      :rows="4"
                      placeholder="请输入视频描述"
                    />
                  </el-form-item>
                </el-form>
                
                <div class="upload-actions">
                  <el-space>
                    <el-button
                      type="primary"
                      :loading="uploading"
                      @click="uploadRecording"
                    >
                      <el-icon><Upload /></el-icon>
                      上传视频
                    </el-button>
                    
                    <el-button @click="resetRecording">
                      重新录制
                    </el-button>
                  </el-space>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.screen-record-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions h2 {
  color: var(--mc-text-primary, #303133);
}

[data-theme="dark"] .header-actions h2 {
  color: #ffffff;
}

.not-supported {
  text-align: center;
  padding: 40px;
}

.settings-card {
  max-width: 600px;
  margin: 0 auto;
}

.start-actions {
  text-align: center;
  margin-top: 24px;
}

.recording-section {
  text-align: center;
}

.recording-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: var(--mc-bg-secondary, #f5f5f5);
  border-radius: 8px;
}

[data-theme="dark"] .recording-header {
  background: #2a2a2a;
}

.recording-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.recording-icon {
  color: #f56565;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.recording-text {
  font-weight: 600;
  color: #f56565;
}

.recording-time {
  font-family: monospace;
  font-size: 18px;
  font-weight: bold;
  color: var(--mc-text-primary, #333);
}

[data-theme="dark"] .recording-time {
  color: #ffffff;
}

.preview-container {
  margin-bottom: 20px;
}

.result-section {
  margin-top: 20px;
}

.record-stats {
  margin-top: 16px;
}

.upload-actions {
  margin-top: 24px;
}

@media (max-width: 768px) {
  .screen-record-container {
    padding: 12px;
  }
  
  .recording-header {
    flex-direction: column;
    gap: 12px;
  }
  
  .result-section .el-col {
    margin-bottom: 20px;
  }
}
</style>
