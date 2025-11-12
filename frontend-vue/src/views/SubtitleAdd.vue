<template>
  <div class="subtitle-add">
    <div class="header">
      <h1>添加字幕</h1>
      <p class="breadcrumb">
        <router-link to="/">首页</router-link>
        <span class="separator">/</span>
        <router-link :to="`/media/${token}`">{{ mediaTitle }}</router-link>
        <span class="separator">/</span>
        <span class="current">添加字幕</span>
      </p>
    </div>

    <el-row :gutter="24">
      <!-- 手动上传字幕 -->
      <el-col :xs="24" :md="12">
        <el-card shadow="never" class="upload-card">
          <template #header>
            <div class="card-header">
              <el-icon><Upload /></el-icon>
              <span>上传字幕文件</span>
            </div>
          </template>

          <el-form
            ref="uploadFormRef"
            :model="uploadForm"
            :rules="uploadRules"
            label-width="100px"
            @submit.prevent="handleUploadSubmit"
          >
            <el-form-item label="字幕文件" prop="subtitle_file">
              <el-upload
                ref="uploadRef"
                :auto-upload="false"
                :limit="1"
                :on-change="handleFileChange"
                :on-remove="handleFileRemove"
                :file-list="fileList"
                accept=".srt,.vtt"
                drag
              >
                <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip">
                    支持 SubRip (.srt) 和 WebVTT (.vtt) 格式，文件大小不超过 2MB
                  </div>
                </template>
              </el-upload>
            </el-form-item>

            <el-form-item label="语言" prop="language">
              <el-select
                v-model="uploadForm.language"
                placeholder="请选择字幕语言"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="lang in languages"
                  :key="lang.id"
                  :label="lang.title"
                  :value="lang.id"
                />
              </el-select>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="uploadLoading"
                :disabled="!uploadForm.subtitle_file"
                @click="handleUploadSubmit"
              >
                <el-icon><Upload /></el-icon>
                上传字幕
              </el-button>
              <el-button @click="handleCancel">
                取消
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Whisper自动转录（如果启用） -->
      <el-col :xs="24" :md="12" v-if="showWhisper">
        <el-card shadow="never" class="whisper-card">
          <template #header>
            <div class="card-header">
              <el-icon><MagicStick /></el-icon>
              <span>AI自动转录</span>
            </div>
          </template>

          <el-alert
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 20px"
          >
            <template #title>
              使用Whisper AI自动生成字幕
            </template>
            Whisper AI可以自动识别视频中的语音并生成字幕文件
          </el-alert>

          <el-form
            ref="whisperFormRef"
            :model="whisperForm"
            label-width="140px"
            @submit.prevent="handleWhisperSubmit"
          >
            <el-form-item label="语音转录">
              <el-checkbox
                v-model="whisperForm.allow_whisper_transcribe"
                :disabled="whisperForm.allow_whisper_transcribe_disabled"
              >
                启用语音转录
              </el-checkbox>
              <div class="form-help" v-if="whisperForm.allow_whisper_transcribe_disabled">
                <el-icon><CircleCheck /></el-icon>
                已请求转录
              </div>
            </el-form-item>

            <el-form-item label="英文翻译">
              <el-checkbox
                v-model="whisperForm.allow_whisper_transcribe_and_translate"
                :disabled="whisperForm.allow_whisper_transcribe_and_translate_disabled"
              >
                转录并翻译成英文
              </el-checkbox>
              <div class="form-help" v-if="whisperForm.allow_whisper_transcribe_and_translate_disabled">
                <el-icon><CircleCheck /></el-icon>
                已请求翻译
              </div>
            </el-form-item>

            <el-form-item>
              <el-button
                type="success"
                :loading="whisperLoading"
                :disabled="whisperSubmitDisabled"
                @click="handleWhisperSubmit"
              >
                <el-icon><MagicStick /></el-icon>
                提交转录请求
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <!-- 已有字幕列表 -->
    <el-card v-if="subtitles.length > 0" shadow="never" class="subtitles-list">
      <template #header>
        <div class="card-header">
          <el-icon><Document /></el-icon>
          <span>已有字幕</span>
        </div>
      </template>

      <el-table :data="subtitles" style="width: 100%">
        <el-table-column label="语言" width="150">
          <template #default="{ row }">
            <el-tag>{{ row.language }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="文件名" min-width="200">
          <template #default="{ row }">
            <span class="filename">{{ getFileName(row.subtitle_file) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              link
              @click="downloadSubtitle(row)"
            >
              <el-icon><Download /></el-icon>
              下载
            </el-button>
            <el-button
              type="primary"
              size="small"
              link
              :to="`/media/${token}/subtitle/${row.id}/edit`"
            >
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type UploadFile, type UploadUserFile } from 'element-plus'
import {
  Upload,
  UploadFilled,
  MagicStick,
  Document,
  Download,
  Edit,
  CircleCheck
} from '@element-plus/icons-vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const token = ref(route.params.token as string)
const mediaTitle = ref('')

// 表单引用
const uploadFormRef = ref<FormInstance>()
const whisperFormRef = ref<FormInstance>()
const uploadRef = ref()

// 上传表单
const uploadForm = ref({
  subtitle_file: null as File | null,
  language: ''
})

const uploadRules = {
  subtitle_file: [
    { required: true, message: '请选择字幕文件', trigger: 'change' }
  ],
  language: [
    { required: true, message: '请选择语言', trigger: 'change' }
  ]
}

// Whisper表单
const whisperForm = ref({
  allow_whisper_transcribe: false,
  allow_whisper_transcribe_and_translate: false,
  allow_whisper_transcribe_disabled: false,
  allow_whisper_transcribe_and_translate_disabled: false
})

// 语言列表
const languages = ref<Array<{ id: number; code: string; title: string }>>([
  { id: 1, code: 'zh', title: '中文' },
  { id: 2, code: 'en', title: 'English' },
  { id: 3, code: 'ja', title: '日本語' },
  { id: 4, code: 'ko', title: '한국어' },
  { id: 5, code: 'fr', title: 'Français' },
  { id: 6, code: 'de', title: 'Deutsch' },
  { id: 7, code: 'es', title: 'Español' },
  { id: 8, code: 'it', title: 'Italiano' },
  { id: 9, code: 'ru', title: 'Русский' },
  { id: 10, code: 'ar', title: 'العربية' }
])

//已有字幕列表
const subtitles = ref<SubtitleItem[]>([])

// 加载状态
const uploadLoading = ref(false)
const whisperLoading = ref(false)
const showWhisper = ref(false)

// 文件列表
const fileList = ref<UploadUserFile[]>([])

// Whisper提交按钮禁用状态
const whisperSubmitDisabled = computed(() => {
  return whisperForm.value.allow_whisper_transcribe_disabled &&
         whisperForm.value.allow_whisper_transcribe_and_translate_disabled
})

// 处理文件变化
function handleFileChange(file: UploadFile) {
  const rawFile = file.raw
  if (!rawFile) return

  // 检查文件大小
  if (rawFile.size > 2 * 1024 * 1024) {
    ElMessage.error('文件大小不能超过 2MB')
    uploadRef.value?.clearFiles()
    return
  }

  // 检查文件格式
  const fileName = rawFile.name.toLowerCase()
  if (!fileName.endsWith('.srt') && !fileName.endsWith('.vtt')) {
    ElMessage.error('只支持 .srt 和 .vtt 格式的字幕文件')
    uploadRef.value?.clearFiles()
    return
  }

  uploadForm.value.subtitle_file = rawFile
}

// 处理文件移除
function handleFileRemove() {
  uploadForm.value.subtitle_file = null
}

// 上传字幕
async function handleUploadSubmit() {
  if (!uploadFormRef.value) return

  await uploadFormRef.value.validate(async (valid) => {
    if (!valid) return

    uploadLoading.value = true
    try {
      const formData = new FormData()
      formData.append('form-subtitle_file', uploadForm.value.subtitle_file!)
      formData.append('form-language', uploadForm.value.language)
      formData.append('submit', 'submit')

      // 使用传统表单提交
      await axios.post(
        `/add_subtitle?m=${token.value}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            'X-CSRFToken': getCsrfToken()
          }
        }
      )

      ElMessage.success('字幕上传成功！')
      
      // 刷新字幕列表
      await loadSubtitles()
      
      // 重置表单
      uploadFormRef.value?.resetFields()
      uploadRef.value?.clearFiles()
      uploadForm.value.subtitle_file = null

    } catch (error: unknown) {
      console.error('上传字幕失败:', error)
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { data?: { message?: string } } }
        if (axiosError.response?.data?.message) {
          ElMessage.error(axiosError.response.data.message)
        } else {
          ElMessage.error('字幕上传失败，请检查文件格式是否正确')
        }
      } else {
        ElMessage.error('字幕上传失败，请检查文件格式是否正确')
      }
    } finally {
      uploadLoading.value = false
    }
  })
}

// Whisper转录
async function handleWhisperSubmit() {
  whisperLoading.value = true
  try {
    const formData = new FormData()
    
    if (whisperForm.value.allow_whisper_transcribe) {
      formData.append('whisper_form-allow_whisper_transcribe', 'on')
    }
    if (whisperForm.value.allow_whisper_transcribe_and_translate) {
      formData.append('whisper_form-allow_whisper_transcribe_and_translate', 'on')
    }
    formData.append('submit_whisper', 'submit_whisper')

    await axios.post(
      `/add_subtitle?m=${token.value}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-CSRFToken': getCsrfToken()
        }
      }
    )

    ElMessage.success('转录请求已提交，处理完成后字幕将自动添加')
    
    // 更新禁用状态
    if (whisperForm.value.allow_whisper_transcribe) {
      whisperForm.value.allow_whisper_transcribe_disabled = true
    }
    if (whisperForm.value.allow_whisper_transcribe_and_translate) {
      whisperForm.value.allow_whisper_transcribe_and_translate_disabled = true
    }

  } catch (error) {
    console.error('提交转录请求失败:', error)
    ElMessage.error('提交转录请求失败，请稍后再试')
  } finally {
    whisperLoading.value = false
  }
}

// 取消
function handleCancel() {
  router.push(`/media/${token.value}`)
}

// 加载字幕列表
async function loadSubtitles() {
  try {
    // 这里需要从媒体详情API获取字幕信息
    // 暂时使用空数组
    // TODO: 从MediaAPI获取字幕信息
  } catch (error) {
    console.error('加载字幕列表失败:', error)
  }
}

// 下载字幕
interface SubtitleItem {
  id: number
  language: string
  subtitle_file: string
}

function downloadSubtitle(subtitle: SubtitleItem) {
  window.open(`/edit_subtitle?id=${subtitle.id}&action=download`, '_blank')
}

// 获取文件名
function getFileName(url: string): string {
  return url.split('/').pop() || url
}

// 获取CSRF Token
function getCsrfToken(): string {
  const name = 'csrftoken'
  const cookies = document.cookie.split(';')
  for (let cookie of cookies) {
    cookie = cookie.trim()
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1)
    }
  }
  return ''
}

// 初始化
onMounted(async () => {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }

  // 加载字幕列表
  await loadSubtitles()

  // 检查是否显示Whisper功能
  // TODO: 从用户权限或系统配置中获取
  showWhisper.value = false
})
</script>

<style scoped lang="scss">
.subtitle-add {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;

  .header {
    margin-bottom: 24px;

    h1 {
      font-size: 28px;
      font-weight: 600;
      color: #1f2937;
      margin: 0 0 8px 0;
    }

    .breadcrumb {
      font-size: 14px;
      color: #6b7280;
      margin: 0;

      a {
        color: #3b82f6;
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }

      .separator {
        margin: 0 8px;
        color: #9ca3af;
      }

      .current {
        color: #374151;
      }
    }
  }

  .upload-card,
  .whisper-card {
    margin-bottom: 24px;

    .card-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      font-weight: 600;
      color: #1f2937;
    }

    :deep(.el-upload-dragger) {
      padding: 40px;
    }

    .el-icon--upload {
      font-size: 48px;
      color: #409eff;
      margin-bottom: 16px;
    }
  }

  .whisper-card {
    .form-help {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 6px;
      font-size: 13px;
      color: #10b981;

      .el-icon {
        font-size: 16px;
      }
    }
  }

  .subtitles-list {
    .filename {
      font-family: 'Courier New', monospace;
      font-size: 13px;
      color: #374151;
    }
  }
}

@media (max-width: 768px) {
  .subtitle-add {
    padding: 16px;

    .header h1 {
      font-size: 24px;
    }
  }
}
</style>
