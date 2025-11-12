<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaDetail } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import http from '@/services/http'

const route = useRoute()
const router = useRouter()
const token = computed(() => String(route.params.token))
const subtitleId = computed(() => String(route.params.subtitleId))

const loading = ref(false)
const saving = ref(false)
const media = ref<MediaDetail | null>(null)
const subtitleContent = ref('')
const originalContent = ref('')

const subtitleInfo = ref({
  language: '',
  label: '',
  is_default: false,
  url: ''
})

const supportedLanguages = [
  { code: 'zh-CN', name: '中文（简体）' },
  { code: 'zh-TW', name: '中文（繁体）' },
  { code: 'en', name: 'English' },
  { code: 'ja', name: '日本語' },
  { code: 'ko', name: '한국어' },
  { code: 'fr', name: 'Français' },
  { code: 'de', name: 'Deutsch' },
  { code: 'es', name: 'Español' },
  { code: 'pt', name: 'Português' },
  { code: 'ru', name: 'Русский' },
  { code: 'ar', name: 'العربية' }
]

const hasChanges = computed(() => {
  return subtitleContent.value !== originalContent.value
})

async function loadMediaAndSubtitle() {
  loading.value = true
  try {
    // 加载媒体信息
    media.value = await MediaAPI.getMediaDetail(token.value)
    
    if (media.value.media_type !== 'video') {
      ElMessage.error('只能编辑视频字幕')
      router.back()
      return
    }
    
    // 查找字幕信息
    const subtitle = media.value.subtitles_info?.find(s => s.url.includes(subtitleId.value))
    if (!subtitle) {
      ElMessage.error('字幕不存在')
      router.back()
      return
    }
    
    subtitleInfo.value = {
      language: subtitle.language,
      label: subtitle.label,
      is_default: false, // 这个信息可能需要从API获取
      url: subtitle.url
    }
    
    // 加载字幕内容
    await loadSubtitleContent(subtitle.url)
  } catch {
    ElMessage.error('加载字幕信息失败')
    router.back()
  } finally {
    loading.value = false
  }
}

async function loadSubtitleContent(url: string) {
  try {
    const response = await fetch(url)
    const content = await response.text()
    subtitleContent.value = content
    originalContent.value = content
  } catch {
    ElMessage.error('加载字幕内容失败')
  }
}

async function saveSubtitle() {
  if (!hasChanges.value) {
    ElMessage.info('没有修改内容')
    return
  }
  
  saving.value = true
  try {
    const blob = new Blob([subtitleContent.value], { type: 'text/plain;charset=utf-8' })
    const file = new File([blob], 'subtitle.srt', { type: 'text/plain' })
    
    const formData = new FormData()
    formData.append('subtitle_file', file)
    formData.append('language', subtitleInfo.value.language)
    formData.append('label', subtitleInfo.value.label)
    formData.append('is_default', String(subtitleInfo.value.is_default))
    
    await http.put(`/v1/media/${token.value}/subtitles/${subtitleId.value}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    originalContent.value = subtitleContent.value
    ElMessage.success('字幕保存成功')
  } catch (error: any) {
    ElMessage.error('字幕保存失败: ' + (error.message || '未知错误'))
  } finally {
    saving.value = false
  }
}

async function deleteSubtitle() {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个字幕吗？此操作不可撤销！',
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await http.delete(`/v1/media/${token.value}/subtitles/${subtitleId.value}`)
    ElMessage.success('字幕删除成功')
    router.push({ name: 'media-detail', params: { token: token.value } })
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('字幕删除失败')
    }
  }
}

function formatSubtitle() {
  // 简单的SRT格式化
  const lines = subtitleContent.value.split('\n')
  const formatted: string[] = []
  let index = 1
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    if (line && !line.match(/^\d+$/) && !line.match(/\d{2}:\d{2}:\d{2}/)) {
      // 这是字幕文本行
      formatted.push(String(index))
      formatted.push('00:00:00,000 --> 00:00:05,000') // 默认时间
      formatted.push(line)
      formatted.push('')
      index++
    }
  }
  
  subtitleContent.value = formatted.join('\n')
  ElMessage.success('字幕格式化完成')
}

function insertTimestamp() {
  const timestamp = '00:00:00,000 --> 00:00:05,000'
  const textarea = document.querySelector('.subtitle-editor') as HTMLTextAreaElement
  if (textarea) {
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const text = subtitleContent.value
    subtitleContent.value = text.substring(0, start) + timestamp + text.substring(end)
  }
}

function validateSubtitle() {
  const lines = subtitleContent.value.split('\n')
  const errors: string[] = []
  let subtitleCount = 0
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()
    
    // 检查序号
    if (line.match(/^\d+$/)) {
      subtitleCount++
      const expectedIndex = subtitleCount
      if (parseInt(line) !== expectedIndex) {
        errors.push(`第 ${i + 1} 行：序号不连续，期望 ${expectedIndex}，实际 ${line}`)
      }
    }
    
    // 检查时间格式
    if (line.match(/\d{2}:\d{2}:\d{2}/)) {
      if (!line.match(/^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$/)) {
        errors.push(`第 ${i + 1} 行：时间格式错误`)
      }
    }
  }
  
  if (errors.length > 0) {
    ElMessage.error(`发现 ${errors.length} 个错误：\n${errors.slice(0, 5).join('\n')}${errors.length > 5 ? '\n...' : ''}`)
  } else {
    ElMessage.success(`字幕验证通过，共 ${subtitleCount} 条字幕`)
  }
}

async function beforeLeave() {
  if (hasChanges.value) {
    try {
      await ElMessageBox.confirm(
        '您有未保存的修改，确定要离开吗？',
        '确认离开',
        {
          confirmButtonText: '离开',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      return true
    } catch {
      return false
    }
  }
  return true
}

// 监听页面离开
window.addEventListener('beforeunload', (e) => {
  if (hasChanges.value) {
    e.preventDefault()
    e.returnValue = ''
  }
})

onMounted(loadMediaAndSubtitle)
</script>

<template>
  <div class="subtitle-edit-container">
    <el-card>
      <template #header>
        <div class="header-actions">
          <h2>编辑字幕</h2>
          <el-space>
            <el-tag v-if="hasChanges" type="warning">未保存</el-tag>
            <el-button @click="beforeLeave() && router.back()">返回</el-button>
          </el-space>
        </div>
      </template>

      <el-skeleton :loading="loading" animated>
        <template #template>
          <el-skeleton-item variant="text" style="width: 60%" />
          <el-skeleton-item variant="rect" style="width: 100%; height: 400px" />
        </template>

        <template #default>
          <div v-if="media" class="subtitle-editor-container">
            <!-- 媒体信息 -->
            <el-card class="media-info-card">
              <div class="media-preview">
                <img
                  :src="media.thumbnail_url || media.poster_url"
                  :alt="media.title"
                  style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px"
                />
                <div class="media-details">
                  <h4>{{ media.title }}</h4>
                  <div class="subtitle-meta">
                    <el-tag size="small">{{ subtitleInfo.language }}</el-tag>
                    <span>{{ subtitleInfo.label }}</span>
                  </div>
                </div>
              </div>
            </el-card>

            <!-- 编辑工具栏 -->
            <div class="editor-toolbar">
              <el-space>
                <el-button type="primary" :loading="saving" @click="saveSubtitle">
                  <el-icon><DocumentChecked /></el-icon>
                  保存字幕
                </el-button>
                
                <el-button @click="validateSubtitle">
                  <el-icon><CircleCheck /></el-icon>
                  验证格式
                </el-button>
                
                <el-button @click="formatSubtitle">
                  <el-icon><Sort /></el-icon>
                  格式化
                </el-button>
                
                <el-button @click="insertTimestamp">
                  <el-icon><Timer /></el-icon>
                  插入时间戳
                </el-button>
                
                <el-popconfirm
                  title="确定要删除这个字幕吗？"
                  @confirm="deleteSubtitle"
                >
                  <template #reference>
                    <el-button type="danger">
                      <el-icon><Delete /></el-icon>
                      删除字幕
                    </el-button>
                  </template>
                </el-popconfirm>
              </el-space>
            </div>

            <!-- 字幕编辑器 -->
            <div class="editor-main">
              <el-row :gutter="20">
                <el-col :span="16">
                  <el-card>
                    <template #header>
                      <div class="editor-header">
                        <h3>字幕内容编辑</h3>
                        <el-text type="info" size="small">
                          行数: {{ subtitleContent.split('\n').length }} | 
                          字符数: {{ subtitleContent.length }}
                        </el-text>
                      </div>
                    </template>
                    
                    <el-input
                      v-model="subtitleContent"
                      type="textarea"
                      class="subtitle-editor"
                      :rows="20"
                      placeholder="请输入字幕内容..."
                      show-word-limit
                      :maxlength="50000"
                    />
                  </el-card>
                </el-col>
                
                <el-col :span="8">
                  <el-card>
                    <template #header>
                      <h3>字幕设置</h3>
                    </template>
                    
                    <el-form :model="subtitleInfo" label-width="80px">
                      <el-form-item label="语言">
                        <el-select v-model="subtitleInfo.language" style="width: 100%">
                          <el-option
                            v-for="lang in supportedLanguages"
                            :key="lang.code"
                            :label="lang.name"
                            :value="lang.code"
                          />
                        </el-select>
                      </el-form-item>
                      
                      <el-form-item label="标签">
                        <el-input v-model="subtitleInfo.label" />
                      </el-form-item>
                      
                      <el-form-item label="默认字幕">
                        <el-checkbox v-model="subtitleInfo.is_default">
                          设为默认字幕
                        </el-checkbox>
                      </el-form-item>
                    </el-form>
                  </el-card>
                  
                  <!-- 编辑帮助 -->
                  <el-card style="margin-top: 16px">
                    <template #header>
                      <h3>编辑帮助</h3>
                    </template>
                    
                    <div class="help-content">
                      <h4>SRT 格式示例：</h4>
                      <pre class="format-example">1
00:00:01,000 --> 00:00:05,000
这是第一条字幕

2
00:00:06,000 --> 00:00:10,000
这是第二条字幕</pre>
                      
                      <h4>快捷操作：</h4>
                      <ul class="help-list">
                        <li>Ctrl+S: 保存字幕</li>
                        <li>Ctrl+F: 查找文本</li>
                        <li>Ctrl+Z: 撤销操作</li>
                        <li>Ctrl+Y: 重做操作</li>
                      </ul>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>
          </div>
        </template>
      </el-skeleton>
    </el-card>
  </div>
</template>

<style scoped>
.subtitle-edit-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subtitle-editor-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.media-info-card {
  margin-bottom: 0;
}

.media-preview {
  display: flex;
  gap: 12px;
  align-items: center;
}

.media-details h4 {
  margin: 0 0 8px 0;
  color: #303133;
}

.subtitle-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.editor-toolbar {
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
}

.editor-main {
  flex: 1;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subtitle-editor {
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
}

.help-content h4 {
  margin: 0 0 8px 0;
  color: #303133;
  font-size: 14px;
}

.format-example {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  font-size: 12px;
  margin: 8px 0 16px 0;
  white-space: pre-wrap;
}

.help-list {
  margin: 8px 0 0 0;
  padding-left: 16px;
  font-size: 12px;
  color: #606266;
}

.help-list li {
  margin-bottom: 4px;
}

@media (max-width: 768px) {
  .subtitle-edit-container {
    padding: 12px;
  }
  
  .editor-main .el-col {
    margin-bottom: 16px;
  }
  
  .media-preview {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
