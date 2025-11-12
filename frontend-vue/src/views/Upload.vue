<script setup lang="ts">
/* eslint-disable vue/multi-word-component-names */
import { ref, computed } from 'vue'
import { MediaAPI } from '@/api'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled, VideoPlay, Picture, Headset } from '@element-plus/icons-vue'

const router = useRouter()
const form = ref<{ file: File | null; title: string; description: string }>({ file: null, title: '', description: '' })
const loading = ref(false)
const progress = ref(0)
const uploadStatus = ref<'ready' | 'uploading' | 'processing' | 'success' | 'error'>('ready')

// 防止重复提交的标记
const isSubmitting = ref(false)

// 文件预览URL
const previewUrl = ref<string>('')

// 文件类型
const fileType = computed(() => {
  if (!form.value.file) return null
  const type = form.value.file.type
  if (type.startsWith('video/')) return 'video'
  if (type.startsWith('image/')) return 'image'
  if (type.startsWith('audio/')) return 'audio'
  return 'other'
})

async function submit() {
  // 防止重复提交
  if (isSubmitting.value || loading.value) {
    ElMessage.warning('正在上传中，请勿重复提交')
    return
  }
  
  if (!form.value.file) {
    ElMessage.warning('请选择文件')
    return
  }
  
  isSubmitting.value = true
  loading.value = true
  uploadStatus.value = 'uploading'
  progress.value = 0
  
  try {
    // 模拟上传进度
    const progressInterval = setInterval(() => {
      if (progress.value < 90) {
        progress.value += 10
      }
    }, 200)
    
    // 上传媒体并获取返回的媒体详情
    const uploadedMedia = await MediaAPI.createMedia({
      media_file: form.value.file,
      title: form.value.title || undefined,
      description: form.value.description || undefined,
    })
    
    clearInterval(progressInterval)
    progress.value = 100
    uploadStatus.value = 'success'
    
    ElMessage.success('上传成功！正在跳转到视频页面...')
    
    // 跳转到刚上传的视频详情页
    setTimeout(() => {
      if (uploadedMedia?.friendly_token) {
        router.push({ name: 'media-detail', params: { token: uploadedMedia.friendly_token } })
      } else {
        // 如果没有返回token，跳转到用户主页
        router.push('/me')
      }
    }, 1500)
  } catch (error: unknown) {
    uploadStatus.value = 'error'
    const errorMessage = error && typeof error === 'object' && 'message' in error
      ? (error as { message: string }).message
      : '上传失败'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
    isSubmitting.value = false
  }
}

function resetForm() {
  form.value = { file: null, title: '', description: '' }
  progress.value = 0
  uploadStatus.value = 'ready'
  loading.value = false
  isSubmitting.value = false
  
  // 清除预览URL
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = ''
  }
  
  // 清空文件输入
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
  if (fileInput) {
    fileInput.value = ''
  }
}

// 处理文件选择
function handleFileChange(file: any) {
  form.value.file = file.raw
  
  // 自动填充标题
  if (!form.value.title) {
    form.value.title = file.name.replace(/\.[^/.]+$/, '')
  }
  
  // 生成预览URL
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
  previewUrl.value = URL.createObjectURL(file.raw)
  
  console.log('文件已选择:', file.name, '类型:', fileType.value)
}
</script>

<template>
  <section class="home-sec" style="max-width:720px">
    <div class="home-sec-head">
      <div class="home-sec-title">上传媒体</div>
    </div>
    
    <el-card>
      <el-form label-width="80px" @submit.prevent>
        <!-- 文件选择 -->
        <el-form-item label="选择文件">
          <el-upload
            class="upload-demo"
            drag
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            accept="video/*,image/*,audio/*,application/pdf"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持视频、音频和图片文件
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <!-- 文件预览 -->
        <el-form-item v-if="form.file" label="文件预览">
          <div class="file-preview">
            <!-- 视频预览 -->
            <div v-if="fileType === 'video'" class="preview-container">
              <video 
                :src="previewUrl" 
                controls 
                class="preview-video"
                preload="metadata"
              />
              <div class="file-info">
                <el-icon><VideoPlay /></el-icon>
                <span class="file-name">{{ form.file.name }}</span>
                <el-tag type="success" size="small">{{ (form.file.size / 1024 / 1024).toFixed(2) }} MB</el-tag>
              </div>
            </div>
            
            <!-- 图片预览 -->
            <div v-else-if="fileType === 'image'" class="preview-container">
              <img 
                :src="previewUrl" 
                :alt="form.file.name"
                class="preview-image"
              />
              <div class="file-info">
                <el-icon><Picture /></el-icon>
                <span class="file-name">{{ form.file.name }}</span>
                <el-tag type="success" size="small">{{ (form.file.size / 1024 / 1024).toFixed(2) }} MB</el-tag>
              </div>
            </div>
            
            <!-- 音频预览 -->
            <div v-else-if="fileType === 'audio'" class="preview-container">
              <div class="audio-preview">
                <el-icon class="audio-icon"><Headset /></el-icon>
                <audio 
                  :src="previewUrl" 
                  controls 
                  class="preview-audio"
                />
              </div>
              <div class="file-info">
                <el-icon><Headset /></el-icon>
                <span class="file-name">{{ form.file.name }}</span>
                <el-tag type="success" size="small">{{ (form.file.size / 1024 / 1024).toFixed(2) }} MB</el-tag>
              </div>
            </div>
            
            <!-- 其他文件 -->
            <div v-else class="preview-container">
              <div class="file-info">
                <el-icon><UploadFilled /></el-icon>
                <span class="file-name">{{ form.file.name }}</span>
                <el-tag type="success" size="small">{{ (form.file.size / 1024 / 1024).toFixed(2) }} MB</el-tag>
              </div>
            </div>
          </div>
        </el-form-item>
        
        <!-- 标题 -->
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="输入媒体标题" maxlength="200" show-word-limit />
        </el-form-item>
        
        <!-- 描述 -->
        <el-form-item label="描述">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="4" 
            placeholder="输入媒体描述"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>
        
        <!-- 上传进度 -->
        <el-form-item v-if="uploadStatus !== 'ready'" label="上传进度">
          <el-progress 
            :percentage="progress" 
            :status="uploadStatus === 'success' ? 'success' : uploadStatus === 'error' ? 'exception' : undefined"
          />
          <div style="margin-top: 8px; font-size: 14px; color: #909399;">
            <span v-if="uploadStatus === 'uploading'">正在上传...</span>
            <span v-else-if="uploadStatus === 'processing'">正在处理...</span>
            <span v-else-if="uploadStatus === 'success'" style="color: #67c23a;">上传成功！</span>
            <span v-else-if="uploadStatus === 'error'" style="color: #f56c6c;">上传失败</span>
          </div>
        </el-form-item>
        
        <!-- 按钮 -->
        <el-form-item>
          <el-button 
            type="success" 
            :disabled="!form.file || loading || isSubmitting" 
            :loading="loading" 
            @click="submit"
            size="large"
          >
            <el-icon v-if="!loading"><UploadFilled /></el-icon>
            {{ loading ? '上传中...' : '开始上传' }}
          </el-button>
          <el-button 
            v-if="uploadStatus === 'error' || uploadStatus === 'success'" 
            @click="resetForm"
          >
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </section>
</template>

<style scoped>
.file-preview {
  width: 100%;
  margin-top: 16px;
}

.preview-container {
  border-radius: 8px;
  overflow: hidden;
  background: var(--el-fill-color-light);
}

.preview-video,
.preview-image {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  background: #000;
  display: block;
}

.audio-preview {
  padding: 40px 20px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.audio-icon {
  font-size: 64px;
  color: white;
  margin-bottom: 20px;
}

.preview-audio {
  width: 100%;
  max-width: 400px;
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color-lighter);
}

.file-info .el-icon {
  font-size: 20px;
  color: var(--el-color-primary);
}

.file-name {
  flex: 1;
  font-size: 14px;
  color: var(--el-text-color-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 暗色模式支持 */
[data-theme="dark"] .preview-container {
  background: #1a1a1a;
}

[data-theme="dark"] .file-info {
  background: #262626;
  border-top-color: #333;
}

[data-theme="dark"] .file-name {
  color: #ffffff;
}
</style>
