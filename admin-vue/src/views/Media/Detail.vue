<template>
  <div class="media-detail-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>媒体详情</span>
          <el-button @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
      </template>
      
      <el-form
        v-if="mediaForm"
        ref="formRef"
        :model="mediaForm"
        :rules="rules"
        label-width="120px"
        style="max-width: 100%"
      >
        <!-- 媒体播放器 -->
        <el-divider content-position="left">媒体内容</el-divider>
        
        <div class="media-player-section">
          <!-- 视频播放器 -->
          <div v-if="mediaForm.media_type === 'video'" class="video-container">
            <video
              :src="mediaForm.original_media_url || mediaForm.preview_url"
              :poster="mediaForm.poster_url || mediaForm.thumbnail_url"
              controls
              style="width: 100%; max-width: 800px; border-radius: 8px"
            >
              您的浏览器不支持视频播放
            </video>
          </div>
          
          <!-- 图片查看器 -->
          <div v-else-if="mediaForm.media_type === 'image'" class="image-container">
            <el-image
              :src="mediaForm.original_media_url || mediaForm.preview_url"
              fit="contain"
              style="max-width: 800px; max-height: 600px; border-radius: 8px"
              :preview-src-list="[mediaForm.original_media_url || mediaForm.preview_url]"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>图片加载失败</span>
                </div>
              </template>
            </el-image>
          </div>
          
          <!-- 音频播放器 -->
          <div v-else-if="mediaForm.media_type === 'audio'" class="audio-container">
            <audio
              :src="mediaForm.original_media_url || mediaForm.preview_url"
              controls
              style="width: 100%; max-width: 600px"
            >
              您的浏览器不支持音频播放
            </audio>
          </div>
          
          <!-- PDF预览 -->
          <div v-else-if="mediaForm.media_type === 'pdf'" class="pdf-container">
            <el-link
              :href="mediaForm.original_media_url"
              type="primary"
              target="_blank"
              :icon="Document"
            >
              在新标签页中打开 PDF
            </el-link>
          </div>
          
          <!-- 封面图片 -->
          <div class="thumbnail-preview" style="margin-top: 16px">
            <label style="font-weight: 500; margin-bottom: 8px; display: block">封面图片：</label>
            <el-image
              v-if="mediaForm.thumbnail_url"
              :src="mediaForm.thumbnail_url"
              fit="cover"
              style="width: 300px; height: 169px; border-radius: 8px"
            >
              <template #error>
                <div class="image-placeholder">
                  <el-icon><Picture /></el-icon>
                  <span>无封面</span>
                </div>
              </template>
            </el-image>
          </div>
        </div>

        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>

        <el-form-item label="标题" prop="title">
          <el-input v-model="mediaForm.title" placeholder="请输入标题" />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="mediaForm.description"
            type="textarea"
            :rows="6"
            placeholder="请输入描述"
          />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-tag
            v-for="cat in mediaForm.category"
            :key="cat"
            closable
            style="margin-right: 8px"
            @close="removeCategory(cat)"
          >
            {{ cat }}
          </el-tag>
          <el-input
            v-if="showCategoryInput"
            ref="categoryInputRef"
            v-model="newCategory"
            size="small"
            style="width: 120px"
            placeholder="输入分类"
            @blur="handleCategoryInputConfirm"
            @keyup.enter="handleCategoryInputConfirm"
          />
          <el-button v-else size="small" @click="showCategoryInput = true">
            + 新分类
          </el-button>
        </el-form-item>

        <el-form-item label="标签" prop="tags">
          <el-tag
            v-for="tag in mediaForm.tags"
            :key="tag"
            closable
            style="margin-right: 8px"
            @close="removeTag(tag)"
          >
            {{ tag }}
          </el-tag>
          <el-input
            v-if="showTagInput"
            ref="tagInputRef"
            v-model="newTag"
            size="small"
            style="width: 120px"
            @blur="handleTagInputConfirm"
            @keyup.enter="handleTagInputConfirm"
          />
          <el-button v-else size="small" @click="showTagInput = true">
            + 新标签
          </el-button>
        </el-form-item>

        <!-- 设置选项 -->
        <el-divider content-position="left">设置选项</el-divider>

        <el-form-item label="媒体类型">
          <el-tag :type="getMediaTypeColor(mediaForm.media_type)">
            {{ getMediaTypeName(mediaForm.media_type) }}
          </el-tag>
        </el-form-item>

        <el-form-item label="可见性">
          <el-radio-group v-model="mediaForm.state">
            <el-radio value="public">公开</el-radio>
            <el-radio value="private">私有</el-radio>
            <el-radio value="unlisted">不公开列表</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="精选">
          <el-switch
            v-model="mediaForm.featured"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>

        <el-form-item label="允许评论">
          <el-switch
            v-model="mediaForm.enable_comments"
            active-text="是"
            inactive-text="否"
          />
        </el-form-item>


        <!-- 统计信息 -->
        <el-divider content-position="left">统计信息</el-divider>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="观看次数">
              <span>{{ mediaForm.views || 0 }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="点赞数">
              <span>{{ mediaForm.likes || 0 }}</span>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="收藏数">
              <span>{{ mediaForm.reported_times || 0 }}</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="上传者">
          <span>{{ mediaForm.author_name }}</span>
        </el-form-item>

        <el-form-item label="上传时间">
          <span>{{ formatDate(mediaForm.add_date) }}</span>
        </el-form-item>

        <el-form-item label="最后编辑">
          <span>{{ formatDate(mediaForm.edit_date) }}</span>
        </el-form-item>

        <el-form-item label="编码状态">
          <el-tag :type="getEncodingStatusColor(mediaForm.encoding_status)">
            {{ getEncodingStatusText(mediaForm.encoding_status) }}
          </el-tag>
        </el-form-item>

        <!-- 操作按钮 -->
        <el-form-item>
          <el-button type="primary" @click="handleSubmit">
            <el-icon><Check /></el-icon>
            保存
          </el-button>
          <el-button @click="handleReset">
            <el-icon><RefreshLeft /></el-icon>
            重置
          </el-button>
          <el-button type="danger" @click="handleDelete">
            <el-icon><Delete /></el-icon>
            删除媒体
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type InputInstance } from 'element-plus'
import type { MediaItem } from '@/api/types'
import http from '@/api/http'
import dayjs from 'dayjs'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const formRef = ref<FormInstance>()
const tagInputRef = ref<InputInstance>()
const categoryInputRef = ref<InputInstance>()
const mediaForm = ref<MediaItem | null>(null)
const originalData = ref<MediaItem | null>(null)
const showTagInput = ref(false)
const newTag = ref('')
const showCategoryInput = ref(false)
const newCategory = ref('')

const rules = {
  title: [
    { required: true, message: '请输入标题', trigger: 'blur' },
    { max: 200, message: '标题不能超过200个字符', trigger: 'blur' }
  ]
}

// 加载媒体详情
const loadMediaDetail = async () => {
  const token = route.params.token
  if (!token) {
    ElMessage.error('媒体Token缺失')
    router.back()
    return
  }

  loading.value = true
  try {
    const response = await http.get(`/v1/media/${token}`)
    const mediaData = response
    
    console.log('✅ 媒体详情加载成功:', mediaData)
    console.log('  - 标题:', mediaData.title)
    console.log('  - 类型:', mediaData.media_type)
    console.log('  - 精选:', mediaData.featured)
    console.log('  - 允许评论:', mediaData.enable_comments)
    console.log('  - 原始URL:', mediaData.original_media_url)
    console.log('  - 预览URL:', mediaData.preview_url)
    console.log('  - 封面URL:', mediaData.thumbnail_url)
    console.log('  - 标签:', mediaData.tags_info)
    console.log('  - 分类:', mediaData.categories_info)
    
    // 处理标签格式：如果是tags_info数组，转换为字符串数组
    if (mediaData.tags_info && Array.isArray(mediaData.tags_info)) {
      mediaData.tags = mediaData.tags_info.map((tag: any) => tag.title || tag)
    } else if (!Array.isArray(mediaData.tags)) {
      mediaData.tags = []
    }
    
    // 处理分类格式：如果是categories_info数组，转换为字符串数组
    if (mediaData.categories_info && Array.isArray(mediaData.categories_info)) {
      mediaData.category = mediaData.categories_info.map((cat: any) => cat.title || cat)
    } else if (!Array.isArray(mediaData.category)) {
      mediaData.category = []
    }
    
    mediaForm.value = mediaData
    originalData.value = { ...mediaData }
  } catch (error) {
    console.error('❌ 加载媒体详情失败:', error)
    ElMessage.error('加载媒体详情失败')
    router.back()
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string | undefined) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const getMediaTypeColor = (type: string) => {
  const map: Record<string, string> = {
    video: '',
    image: 'success',
    audio: 'warning',
    pdf: 'danger'
  }
  return map[type] || 'info'
}

const getMediaTypeName = (type: string) => {
  const map: Record<string, string> = {
    video: '视频',
    image: '图片',
    audio: '音频',
    pdf: 'PDF'
  }
  return map[type] || type
}

const getEncodingStatusColor = (status: string) => {
  const map: Record<string, string> = {
    success: 'success',
    running: 'warning',
    pending: 'info',
    fail: 'danger'
  }
  return map[status] || 'info'
}

const getEncodingStatusText = (status: string) => {
  const map: Record<string, string> = {
    success: '成功',
    running: '处理中',
    pending: '等待中',
    fail: '失败'
  }
  return map[status] || status
}

const removeTag = (tag: string) => {
  if (mediaForm.value && mediaForm.value.tags) {
    mediaForm.value.tags = mediaForm.value.tags.filter(t => t !== tag)
  }
}

const handleTagInputConfirm = () => {
  if (newTag.value && mediaForm.value) {
    if (!mediaForm.value.tags) {
      mediaForm.value.tags = []
    }
    if (!mediaForm.value.tags.includes(newTag.value)) {
      mediaForm.value.tags.push(newTag.value)
    }
  }
  showTagInput.value = false
  newTag.value = ''
}

const handleCategoryInputConfirm = () => {
  if (newCategory.value && mediaForm.value) {
    if (!mediaForm.value.category) {
      mediaForm.value.category = []
    }
    if (!mediaForm.value.category.includes(newCategory.value)) {
      mediaForm.value.category.push(newCategory.value)
    }
  }
  showCategoryInput.value = false
  newCategory.value = ''
}

const removeCategory = (cat: string) => {
  if (mediaForm.value && mediaForm.value.category) {
    mediaForm.value.category = mediaForm.value.category.filter(c => c !== cat)
  }
}

const handleSubmit = async () => {
  if (!formRef.value || !mediaForm.value) return

  try {
    await formRef.value.validate()
    
    loading.value = true
    
    // 使用路由中的token参数
    const token = route.params.token
    
    // 准备更新数据
    const updateData: any = {
      title: mediaForm.value.title,
      description: mediaForm.value.description || '',
      state: mediaForm.value.state,
    }
    
    // 添加可选字段（如果存在）
    if (mediaForm.value.featured !== undefined) {
      updateData.featured = mediaForm.value.featured
    }
    
    if (mediaForm.value.enable_comments !== undefined) {
      updateData.enable_comments = mediaForm.value.enable_comments
    }
    
    // 处理标签（需要是字符串数组）
    if (Array.isArray(mediaForm.value.tags)) {
      updateData.tags = mediaForm.value.tags
    } else if (mediaForm.value.tags_info && Array.isArray(mediaForm.value.tags_info)) {
      // 如果tags是对象数组，提取title
      updateData.tags = mediaForm.value.tags_info.map((tag: any) => tag.title || tag)
    }
    
    // 处理分类（需要是字符串数组）
    if (Array.isArray(mediaForm.value.category)) {
      updateData.category = mediaForm.value.category
    } else if (mediaForm.value.categories_info && Array.isArray(mediaForm.value.categories_info)) {
      // 如果category是对象数组，提取title
      updateData.category = mediaForm.value.categories_info.map((cat: any) => cat.title || cat)
    }
    
    console.log('📤 保存媒体信息:', {
      token,
      updateData
    })
    
    // 使用PUT方法更新媒体
    const response = await http.put(`/v1/media/${token}`, updateData)
    
    console.log('✅ 保存成功:', response)
    ElMessage.success('保存成功')
    
    // 重新加载媒体详情以获取最新数据
    await loadMediaDetail()
  } catch (error: any) {
    console.error('❌ 保存媒体失败:', error)
    console.error('  - 状态码:', error.response?.status)
    console.error('  - 错误详情:', error.response?.data)
    console.error('  - 完整错误:', JSON.stringify(error.response?.data, null, 2))
    
    // 显示详细的错误信息
    let errorMsg = '保存失败'
    
    if (error.response?.data) {
      const data = error.response.data
      
      // 如果是验证错误（对象形式）
      if (typeof data === 'object' && !data.detail) {
        const errors = []
        for (const [field, messages] of Object.entries(data)) {
          if (Array.isArray(messages)) {
            errors.push(`${field}: ${messages.join(', ')}`)
          } else {
            errors.push(`${field}: ${messages}`)
          }
        }
        errorMsg = errors.join('\n')
      } else if (data.detail) {
        errorMsg = data.detail
      } else if (typeof data === 'string') {
        errorMsg = data
      }
    }
    
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  if (originalData.value) {
    mediaForm.value = { ...originalData.value }
    ElMessage.info('已重置为原始数据')
  }
}

const handleDelete = async () => {
  if (!mediaForm.value) return

  try {
    await ElMessageBox.confirm(
      `确定要删除媒体"${mediaForm.value.title}"吗？此操作不可撤销！`,
      '危险操作',
      {
        type: 'error',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消'
      }
    )

    loading.value = true
    
    // 使用路由中的token参数
    const token = route.params.token
    
    console.log('📤 删除媒体:', token)
    await http.delete(`/v1/media/${token}`)
    
    console.log('✅ 删除成功')
    ElMessage.success('删除成功')
    router.push('/media/list')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('❌ 删除媒体失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMediaDetail()
})
</script>

<style scoped lang="scss">
.media-detail-container {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-lighter);
  color: var(--el-text-color-secondary);

  .el-icon {
    font-size: 48px;
    margin-bottom: 8px;
  }
}

:deep(.el-divider__text) {
  font-size: 16px;
  font-weight: 600;
}

/* 媒体播放器样式 */
.media-player-section {
  margin-bottom: 32px;
}

.video-container,
.image-container,
.audio-container,
.pdf-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  min-height: 200px;
}

.video-container video,
.image-container :deep(.el-image) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.thumbnail-preview {
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
}

[data-theme="dark"] .video-container,
[data-theme="dark"] .image-container,
[data-theme="dark"] .audio-container,
[data-theme="dark"] .pdf-container,
[data-theme="dark"] .thumbnail-preview {
  background: #2d2d2d;
}
</style>
