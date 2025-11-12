<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { MediaAPI } from '@/api'
import { listCategories, listTags } from '@/api/misc'
import type { MediaDetail, Category, Tag, UserMediaActionData } from '@/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Upload, 
  VideoCamera,
  Tools,
  Check,
  Close,
  Warning
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const token = computed(() => String(route.params.token))

const loading = ref(false)
const saving = ref(false)
const media = ref<MediaDetail | null>(null)

// 管理员权限
const isAdmin = computed(() => {
  const profile = auth.profile as {is_staff?: boolean} | null
  return profile?.is_staff || false
})

// 是否为媒体所有者或管理员
const isOwnerOrAdmin = computed(() => {
  if (!media.value || !auth.profile) return false
  return media.value.user === auth.profile.username || isAdmin.value
})

// 分类和标签数据
const allCategories = ref<Category[]>([])
const allTags = ref<Tag[]>([])

// 表单数据
const form = ref({
  title: '',
  description: '',
  media_file: null as File | null,
  uploaded_poster: null as File | null,
  state: 'public' as 'public' | 'private' | 'unlisted',
  tags: [] as string[],
  categories: [] as string[]
})

// 新增标签输入
const newTagInput = ref('')
const newTagVisible = ref(false)

// 缩略图预览
const posterPreviewUrl = ref('')

// 管理员操作相关
const reencodeDialogVisible = ref(false)
const selectedProfiles = ref<number[]>([])

interface EncodeProfile {
  id: number
  name: string
  resolution?: string
  codec?: string
  extension?: string
}

const encodeProfiles = ref<EncodeProfile[]>([])
const reencoding = ref(false)

// 举报记录
interface ReportAction extends UserMediaActionData {
  action: 'report'
  extra_info?: string
  reported_date?: string
}

const reports = ref<ReportAction[]>([])
const loadingReports = ref(false)

async function loadMedia() {
  loading.value = true
  try {
    media.value = await MediaAPI.getMediaDetail(token.value)
    
    // 填充表单
    form.value.title = media.value.title
    form.value.description = media.value.description || ''
    form.value.state = (media.value.state || 'public') as 'public' | 'private' | 'unlisted'
    
    // 填充标签（从 tags_info 中提取）
    if (media.value.tags_info) {
      form.value.tags = media.value.tags_info.map(t => t.title)
    }
    
    // 填充分类（从 categories_info 中提取）
    if (media.value.categories_info) {
      form.value.categories = media.value.categories_info.map(c => c.title)
    }
    
    // 如果是媒体所有者或管理员，加载举报记录
    if (isOwnerOrAdmin.value) {
      await loadReports()
    }
    
  } catch {
    ElMessage.error('加载媒体信息失败')
    router.push('/')
  } finally {
    loading.value = false
  }
}

// 加载分类和标签
async function loadCategoriesAndTags() {
  try {
    const [cats, tagsRes] = await Promise.all([
      listCategories(),
      listTags()
    ])
    allCategories.value = cats
    allTags.value = tagsRes.results || []
    
    // 如果是管理员，加载编码配置
    if (isAdmin.value) {
      await loadEncodeProfiles()
    }
  } catch {
    ElMessage.error('加载分类和标签失败')
  }
}

// 加载编码配置（仅管理员）
async function loadEncodeProfiles() {
  try {
    const response = await fetch('/api/v1/encode_profiles/', {
      headers: {
        'Authorization': auth.token ? `Token ${auth.token}` : ''
      }
    })
    if (response.ok) {
      encodeProfiles.value = await response.json()
    }
  } catch {
    console.error('Load encode profiles error')
  }
}

// 处理媒体文件上传
function handleFileChange(file: File) {
  form.value.media_file = file
}

// 处理缩略图上传
function handlePosterChange(file: File) {
  form.value.uploaded_poster = file
  
  // 生成预览
  const reader = new FileReader()
  reader.onload = (e) => {
    posterPreviewUrl.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

// 添加新标签
function handleNewTagInputConfirm() {
  const tag = newTagInput.value.trim()
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag)
  }
  newTagVisible.value = false
  newTagInput.value = ''
}

// 删除标签
function handleTagClose(tag: string) {
  form.value.tags = form.value.tags.filter(t => t !== tag)
}

// 显示标签输入
function showTagInput() {
  newTagVisible.value = true
}

// 保存更改
async function saveChanges() {
  if (!form.value.title.trim()) {
    ElMessage.warning('请输入标题')
    return
  }

  saving.value = true
  try {
    console.log('💾 准备保存媒体数据:', {
      title: form.value.title,
      description: form.value.description,
      state: form.value.state,
      tags: form.value.tags,
      categories: form.value.categories,
      hasMediaFile: !!form.value.media_file,
      hasPoster: !!form.value.uploaded_poster
    })
    
    await MediaAPI.updateMedia(token.value, {
      title: form.value.title,
      description: form.value.description,
      state: form.value.state,
      tags: form.value.tags,
      categories: form.value.categories,
      media_file: form.value.media_file || undefined,
      uploaded_poster: form.value.uploaded_poster || undefined
    })
    
    console.log('✅ 保存成功')
    ElMessage.success('保存成功')
    router.push({ name: 'media-detail', params: { token: token.value } })
  } catch (error: any) {
    console.error('❌ 保存失败:', error)
    console.error('错误详情:', error.response?.data)
    ElMessage.error(error.response?.data?.detail || '保存失败，请检查网络连接')
  } finally {
    saving.value = false
  }
}

// 删除媒体
async function deleteMedia() {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个媒体吗？此操作不可恢复！',
      '删除媒体',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    await MediaAPI.deleteMedia(token.value)
    ElMessage.success('删除成功')
    router.push('/')
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// ========== 管理员功能 ==========

// 打开重新编码对话框
function openReencodeDialog() {
  reencodeDialogVisible.value = true
  selectedProfiles.value = []
}

// 重新编码
async function handleReencode() {
  if (selectedProfiles.value.length === 0) {
    ElMessage.warning('请选择至少一个编码配置')
    return
  }
  
  reencoding.value = true
  try {
    await MediaAPI.manageMedia(token.value, {
      type: 'encode',
      encoding_profiles: selectedProfiles.value
    })
    
    ElMessage.success('已提交重新编码任务')
    reencodeDialogVisible.value = false
    selectedProfiles.value = []
  } catch {
    ElMessage.error('提交失败')
  } finally {
    reencoding.value = false
  }
}

// 加载举报记录
async function loadReports() {
  if (!isOwnerOrAdmin.value) return
  
  loadingReports.value = true
  try {
    const actions = await MediaAPI.getMediaActions(token.value)
    reports.value = actions.filter(a => a.action === 'report') as ReportAction[]
  } catch {
    console.error('加载举报记录失败')
  } finally {
    loadingReports.value = false
  }
}

// 清空举报记录（仅管理员）
async function clearReports() {
  if (!isAdmin.value) {
    ElMessage.warning('只有管理员可以清空举报记录')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      '确定要清空该媒体的所有举报记录吗？此操作不可撤销！',
      '警告',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await MediaAPI.deleteMediaActions(token.value)
    ElMessage.success('举报记录已清空')
    reports.value = []
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('清空失败')
    }
  }
}

// 审核媒体
async function handleReview(approved: boolean) {
  try {
    await ElMessageBox.confirm(
      `确定要${approved ? '批准' : '拒绝'}这个媒体吗？`,
      '媒体审核',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: approved ? 'success' : 'warning'
      }
    )
    
    await MediaAPI.manageMedia(token.value, {
      type: 'review',
      result: approved
    })
    
    ElMessage.success(`${approved ? '已批准' : '已拒绝'}该媒体`)
    
    // 重新加载媒体信息
    await loadMedia()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('审核失败')
    }
  }
}

onMounted(() => {
  loadMedia()
  loadCategoriesAndTags()
})
</script>

<template>
  <div class="media-edit-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <h2>编辑媒体</h2>
          <el-button @click="router.back()">返回</el-button>
        </div>
      </template>

      <el-skeleton :loading="loading" animated>
        <template #template>
          <el-skeleton-item variant="text" style="width: 60%" />
          <el-skeleton-item variant="text" />
          <el-skeleton-item variant="rect" style="width: 100%; height: 200px" />
        </template>

        <template #default>
          <el-form v-if="media" :model="form" label-width="120px" @submit.prevent>
            <!-- 基本信息 -->
            <el-divider content-position="left">基本信息</el-divider>
            
            <el-form-item label="标题" required>
              <el-input v-model="form.title" placeholder="请输入媒体标题" maxlength="100" show-word-limit />
            </el-form-item>

            <el-form-item label="描述">
              <el-input
                v-model="form.description"
                type="textarea"
                :rows="4"
                placeholder="请输入媒体描述"
                maxlength="500"
                show-word-limit
              />
            </el-form-item>

            <!-- 隐私设置 -->
            <el-form-item label="隐私设置">
              <div class="privacy-setting-wrapper">
                <el-radio-group v-model="form.state">
                  <el-radio label="public">公开</el-radio>
                  <el-radio label="unlisted">仅限链接</el-radio>
                  <el-radio label="private">私密</el-radio>
                </el-radio-group>
                <div class="form-tip">
                  <span v-if="form.state === 'public'">• 公开：任何人都可以搜索到并观看</span>
                  <span v-if="form.state === 'unlisted'">• 仅限链接：只有知道链接的人才能观看</span>
                  <span v-if="form.state === 'private'">• 私密：只有您自己可以观看</span>
                </div>
              </div>
            </el-form-item>

            <!-- 分类选择 -->
            <el-divider content-position="left">分类和标签</el-divider>
            
            <el-form-item label="分类">
              <el-select 
                v-model="form.categories" 
                multiple 
                placeholder="请选择分类"
                style="width: 100%"
                filterable
              >
                <el-option
                  v-for="cat in allCategories"
                  :key="cat.title"
                  :label="cat.title"
                  :value="cat.title"
                >
                  <span>{{ cat.title }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">
                    {{ cat.media_count || 0 }} 个媒体
                  </span>
                </el-option>
              </el-select>
            </el-form-item>

            <!-- 标签编辑 -->
            <el-form-item label="标签">
              <div class="tag-container">
                <el-tag
                  v-for="tag in form.tags"
                  :key="tag"
                  closable
                  @close="handleTagClose(tag)"
                  class="tag-item"
                >
                  {{ tag }}
                </el-tag>
                <el-input
                  v-if="newTagVisible"
                  ref="newTagInputRef"
                  v-model="newTagInput"
                  size="small"
                  class="tag-input"
                  @keyup.enter="handleNewTagInputConfirm"
                  @blur="handleNewTagInputConfirm"
                />
                <el-button
                  v-else
                  size="small"
                  @click="showTagInput"
                >
                  + 添加标签
                </el-button>
              </div>
              <div class="form-tip">
                常用标签：
                <el-tag 
                  v-for="tag in allTags.slice(0, 10)" 
                  :key="tag.title"
                  size="small"
                  class="suggested-tag"
                  @click="!form.tags.includes(tag.title) && form.tags.push(tag.title)"
                  :type="form.tags.includes(tag.title) ? 'success' : 'info'"
                >
                  {{ tag.title }}
                </el-tag>
              </div>
            </el-form-item>

            <!-- 媒体文件 -->
            <el-divider content-position="left">媒体文件</el-divider>
            
            <el-form-item label="当前媒体">
              <div class="current-media">
                <img
                  v-if="media.media_type === 'image'"
                  :src="media.thumbnail_url || media.poster_url || ''"
                  alt="当前媒体"
                  class="media-preview"
                />
                <video
                  v-else-if="media.media_type === 'video'"
                  :poster="media.poster_url || media.thumbnail_url || ''"
                  class="media-preview"
                  controls
                >
                  <source :src="media.preview_url || ''" />
                </video>
                <div v-else class="media-placeholder">
                  <el-icon size="48"><VideoCamera /></el-icon>
                  <p>{{ media.media_type || '未知类型' }}</p>
                </div>
              </div>
            </el-form-item>

            <el-form-item label="替换文件">
              <el-upload
                :auto-upload="false"
                :show-file-list="false"
                :on-change="(file: any) => handleFileChange(file.raw)"
                accept="video/*,audio/*,image/*"
              >
                <el-button type="primary">
                  <el-icon><Upload /></el-icon>
                  选择新文件
                </el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    支持视频、音频、图片格式，留空则不替换文件
                  </div>
                </template>
              </el-upload>
              <div v-if="form.media_file" class="selected-file">
                已选择: {{ form.media_file.name }}
              </div>
            </el-form-item>

            <!-- 缩略图上传 -->
            <el-form-item label="自定义缩略图">
              <el-upload
                :auto-upload="false"
                :show-file-list="false"
                :on-change="(file: any) => handlePosterChange(file.raw)"
                accept="image/*"
              >
                <el-button>
                  <el-icon><Upload /></el-icon>
                  上传缩略图
                </el-button>
                <template #tip>
                  <div class="el-upload__tip">
                    上传自定义缩略图，建议尺寸 16:9
                  </div>
                </template>
              </el-upload>
              <div v-if="posterPreviewUrl" class="poster-preview">
                <img :src="posterPreviewUrl" alt="缩略图预览" />
              </div>
            </el-form-item>

            <!-- 管理员操作区域 -->
            <el-divider v-if="isAdmin" content-position="left">
              管理员操作
            </el-divider>
            
            <el-card v-if="isAdmin" class="admin-actions-card" shadow="hover">
              <template #header>
                <div class="admin-header">
                  <el-icon><Tools /></el-icon>
                  <span>管理员功能</span>
                </div>
              </template>
              
              <el-space direction="vertical" :fill="true" style="width: 100%">
                <!-- 媒体审核 -->
                <div class="admin-section">
                  <h4>媒体审核</h4>
                  <div class="review-status">
                    <span>审核状态：</span>
                    <el-tag v-if="(media as any).is_reviewed === true" type="success">已批准</el-tag>
                    <el-tag v-else-if="(media as any).is_reviewed === false" type="danger">已拒绝</el-tag>
                    <el-tag v-else type="warning">待审核</el-tag>
                  </div>
                  <el-space class="review-actions" wrap>
                    <el-button 
                      type="success" 
                      @click="handleReview(true)"
                      :disabled="(media as any).is_reviewed === true"
                    >
                      <el-icon><Check /></el-icon>
                      批准
                    </el-button>
                    <el-button 
                      type="danger" 
                      @click="handleReview(false)"
                      :disabled="(media as any).is_reviewed === false"
                    >
                      <el-icon><Close /></el-icon>
                      拒绝
                    </el-button>
                  </el-space>
                </div>
                
                <!-- 重新编码 -->
                <el-divider />
                <div class="admin-section">
                  <h4>重新编码</h4>
                  <p class="admin-hint">为该媒体创建新的编码任务</p>
                  <el-button 
                    type="primary" 
                    @click="openReencodeDialog"
                  >
                    <el-icon><Tools /></el-icon>
                    重新编码
                  </el-button>
                </div>
              </el-space>
            </el-card>

            <!-- 举报记录区域（媒体所有者或管理员可见） -->
            <el-divider v-if="isOwnerOrAdmin && reports.length > 0" content-position="left">
              举报信息
            </el-divider>
            
            <el-card v-if="isOwnerOrAdmin && reports.length > 0" class="reports-card" shadow="hover">
              <template #header>
                <div class="reports-header">
                  <div class="reports-title">
                    <el-icon><Warning /></el-icon>
                    <span>举报记录（{{ reports.length }}）</span>
                  </div>
                  <el-button 
                    v-if="isAdmin" 
                    type="danger" 
                    size="small" 
                    @click="clearReports"
                  >
                    清空记录
                  </el-button>
                </div>
              </template>
              
              <el-alert 
                :title="`该媒体已被举报 ${reports.length} 次`"
                type="warning"
                :closable="false"
                style="margin-bottom: 20px;"
              />
              
              <el-skeleton :loading="loadingReports" animated>
                <template #template>
                  <el-skeleton-item variant="text" />
                  <el-skeleton-item variant="text" />
                </template>
                
                <template #default>
                  <el-timeline>
                    <el-timeline-item 
                      v-for="(report, index) in reports" 
                      :key="index"
                      :timestamp="report.reported_date ? new Date(report.reported_date).toLocaleString('zh-CN') : report.timestamp ? new Date(report.timestamp).toLocaleString('zh-CN') : '未知时间'"
                      placement="top"
                    >
                      <el-card>
                        <p class="report-reason">{{ report.extra_info || '未提供原因' }}</p>
                      </el-card>
                    </el-timeline-item>
                  </el-timeline>
                </template>
              </el-skeleton>
            </el-card>

            <!-- 操作按钮 -->
            <el-form-item>
              <el-space>
                <el-button type="primary" :loading="saving" @click="saveChanges">
                  保存更改
                </el-button>
                <el-button @click="router.back()">取消</el-button>
                <el-button type="danger" @click="deleteMedia">
                  删除媒体
                </el-button>
              </el-space>
            </el-form-item>
          </el-form>
        </template>
      </el-skeleton>
    </el-card>
    
    <!-- 重新编码对话框 -->
    <el-dialog 
      v-model="reencodeDialogVisible" 
      title="选择编码配置"
      width="600px"
    >
      <div class="reencode-dialog-content">
        <p class="dialog-hint">
          选择要使用的编码配置，系统将为此媒体创建新的编码任务。
        </p>
        
        <el-checkbox-group v-model="selectedProfiles" class="profile-list">
          <el-checkbox 
            v-for="profile in encodeProfiles" 
            :key="profile.id" 
            :label="profile.id"
            class="profile-item"
          >
            <div class="profile-info">
              <span class="profile-name">{{ profile.name }}</span>
              <span class="profile-details">
                {{ profile.resolution || 'N/A' }} | 
                {{ profile.codec || 'N/A' }} | 
                .{{ profile.extension || 'mp4' }}
              </span>
            </div>
          </el-checkbox>
        </el-checkbox-group>
        
        <el-empty v-if="encodeProfiles.length === 0" description="暂无编码配置" />
      </div>
      
      <template #footer>
        <el-button @click="reencodeDialogVisible = false">取消</el-button>
        <el-button 
          type="primary" 
          :loading="reencoding"
          @click="handleReencode"
          :disabled="selectedProfiles.length === 0"
        >
          <el-icon><Tools /></el-icon>
          确定编码
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.media-edit-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.current-media {
  display: flex;
  align-items: center;
  gap: 12px;
}

.media-preview {
  max-width: 300px;
  max-height: 200px;
  border-radius: 8px;
  border: 2px solid #dcdfe6;
}

.media-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 2px dashed #dcdfe6;
  border-radius: 6px;
  color: #909399;
}

.selected-file {
  margin-top: 8px;
  color: #67c23a;
  font-size: 14px;
}

/* 隐私设置容器 */
.privacy-setting-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

/* 隐私设置提示 */
.form-tip {
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
  padding-left: 0;
}

/* 标签样式 */
.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tag-item {
  cursor: pointer;
}

.tag-input {
  width: 120px;
}

.suggested-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.suggested-tag:hover {
  transform: scale(1.05);
}

/* 缩略图预览 */
.poster-preview {
  margin-top: 12px;
}

.poster-preview img {
  max-width: 400px;
  max-height: 225px;
  border-radius: 8px;
  border: 2px solid #dcdfe6;
}

/* 暗色模式 */
[data-theme="dark"] .media-preview,
[data-theme="dark"] .poster-preview img {
  border-color: #4c4d4f;
}

[data-theme="dark"] .media-placeholder {
  border-color: #4c4d4f;
  color: #a8abb2;
}

[data-theme="dark"] .form-tip {
  color: #a8abb2;
}

/* 管理员操作区域 */
.admin-actions-card {
  margin-top: 24px;
  border: 2px solid #409eff;
}

.admin-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #409eff;
}

.admin-section {
  padding: 12px 0;
}

.admin-section h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

[data-theme="dark"] .admin-section h4 {
  color: #ffffff;
}

.admin-hint {
  margin: 8px 0;
  font-size: 14px;
  color: #909399;
}

.review-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
}

.review-actions {
  margin-top: 12px;
}

/* 重新编码对话框 */
.reencode-dialog-content {
  max-height: 500px;
  overflow-y: auto;
}

.dialog-hint {
  margin-bottom: 16px;
  padding: 12px;
  background: #ecf5ff;
  border-left: 4px solid #409eff;
  border-radius: 4px;
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

[data-theme="dark"] .dialog-hint {
  background: #1a3a52;
  color: #cccccc;
}

.profile-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.profile-item {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
  background: #fafafa;
}

[data-theme="dark"] .profile-item {
  background: #1a1a1a;
  border-color: #333;
}

.profile-item:hover {
  border-color: #409eff;
  background: #ecf5ff;
}

[data-theme="dark"] .profile-item:hover {
  background: #2d2d2d;
}

.profile-item :deep(.el-checkbox__label) {
  width: 100%;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.profile-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

[data-theme="dark"] .profile-name {
  color: #ffffff;
}

.profile-details {
  font-size: 13px;
  color: #909399;
}

/* 举报记录区域 */
.reports-card {
  margin-top: 24px;
  border: 2px solid #f56c6c;
}

.reports-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.reports-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #f56c6c;
}

.report-reason {
  margin: 0;
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}

[data-theme="dark"] .report-reason {
  color: #cccccc;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .media-edit-container {
    padding: 12px;
  }

  .media-preview,
  .poster-preview img {
    max-width: 100%;
  }

  .tag-container {
    width: 100%;
  }
}
</style>
