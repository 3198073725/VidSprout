<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaDetail } from '@/api'
import { useAuthStore } from '@/stores/auth'
import MediaNav from '@/components/media/MediaNav.vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const mediaToken = computed(() => String(route.params.token))
const loading = ref(false)
const saving = ref(false)
const media = ref<MediaDetail | null>(null)

// 发布表单数据 - 对应后端的crispy表单
const publishForm = ref({
  is_public: true,
  is_featured: false,
  is_reviewed: false,
  publish_date: '',
  categories: [] as string[],
  tags: [] as string[],
  allow_comments: true,
  allow_ratings: true,
  password_protected: false,
  access_password: '',
  download_enabled: false,
  embed_enabled: true
})

// 可用的分类和标签选项
const availableCategories = ref([
  { value: 'education', label: '教育' },
  { value: 'entertainment', label: '娱乐' },
  { value: 'news', label: '新闻' },
  { value: 'sports', label: '体育' },
  { value: 'technology', label: '科技' },
  { value: 'music', label: '音乐' }
])

const availableTags = ref([
  'tutorial', 'demo', 'presentation', 'interview', 'review', 'documentary'
])

async function loadMedia() {
  if (!mediaToken.value) return
  
  loading.value = true
  try {
    media.value = await MediaAPI.getMediaDetail(mediaToken.value)
    
    // 初始化表单数据
    if (media.value) {
      publishForm.value = {
        is_public: media.value.is_public ?? true,
        is_featured: (media.value as any).is_featured ?? false,
        is_reviewed: (media.value as any).is_reviewed ?? false,
        publish_date: media.value.add_date ? new Date(media.value.add_date).toISOString().slice(0, 16) : '',
        categories: media.value.categories?.map(cat => cat.id.toString()) || [],
        tags: media.value.tags?.map(tag => tag.id.toString()) || [],
        allow_comments: media.value.allow_comments ?? true,
        allow_ratings: (media.value as any).allow_ratings ?? true,
        password_protected: false,
        access_password: '',
        download_enabled: (media.value as any).download_enabled ?? false,
        embed_enabled: (media.value as any).embed_enabled ?? true
      }
    }
  } catch (error) {
    console.error('加载媒体失败:', error)
    ElMessage.error('加载媒体信息失败')
  } finally {
    loading.value = false
  }
}

async function savePublishSettings() {
  if (!media.value) return
  
  saving.value = true
  try {
    // 这里应该调用发布设置的API
    // await MediaAPI.updatePublishSettings(mediaToken.value, publishForm.value)
    
    ElMessage.success('发布设置已保存')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

function previewMedia() {
  if (media.value) {
    const url = router.resolve({ 
      name: 'media-detail', 
      params: { token: media.value.friendly_token } 
    }).href
    window.open(url, '_blank')
  }
}

function generateEmbedCode() {
  if (media.value) {
    const embedUrl = `${window.location.origin}/embed?m=${media.value.friendly_token}`
    const embedCode = `<iframe src="${embedUrl}" width="640" height="360" frameborder="0" allowfullscreen></iframe>`
    
    navigator.clipboard.writeText(embedCode).then(() => {
      ElMessage.success('嵌入代码已复制到剪贴板')
    }).catch(() => {
      ElMessage.error('复制失败，请手动复制')
    })
  }
}

onMounted(loadMedia)
</script>

<template>
  <div class="media-publish-container">
    <!-- 对应后端模板的头部标题 -->
    <div class="page-header">
      <h1>发布媒体</h1>
      <p v-if="media">{{ media.title }}</p>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <div v-else-if="media" class="user-action-form-wrap">
      <!-- 对应后端模板的 media_nav.html 包含 -->
      <MediaNav :media="media" active-tab="publish" />
      
      <!-- 对应后端模板的表单容器样式 -->
      <div class="user-action-form-inner">
        <el-form 
          :model="publishForm" 
          label-width="120px"
          size="large"
        >
          <!-- 基本发布设置 -->
          <el-card class="form-section" shadow="never">
            <template #header>
              <h3>基本设置</h3>
            </template>
            
            <el-form-item label="公开状态">
              <el-switch
                v-model="publishForm.is_public"
                active-text="公开"
                inactive-text="私有"
              />
              <div class="form-help">
                公开的媒体可以被所有用户查看和搜索
              </div>
            </el-form-item>

            <el-form-item label="精选媒体">
              <el-switch
                v-model="publishForm.is_featured"
                active-text="是"
                inactive-text="否"
              />
              <div class="form-help">
                精选媒体将在精选页面中优先展示
              </div>
            </el-form-item>

            <el-form-item label="审核状态">
              <el-switch
                v-model="publishForm.is_reviewed"
                active-text="已审核"
                inactive-text="待审核"
              />
              <div class="form-help">
                已审核的媒体可以正常显示
              </div>
            </el-form-item>

            <el-form-item label="发布时间">
              <el-date-picker
                v-model="publishForm.publish_date"
                type="datetime"
                placeholder="选择发布时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DDTHH:mm"
                style="width: 100%"
              />
              <div class="form-help">
                留空表示立即发布
              </div>
            </el-form-item>
          </el-card>

          <!-- 分类和标签 -->
          <el-card class="form-section" shadow="never">
            <template #header>
              <h3>分类和标签</h3>
            </template>
            
            <el-form-item label="分类">
              <el-select
                v-model="publishForm.categories"
                multiple
                placeholder="选择分类"
                style="width: 100%"
              >
                <el-option
                  v-for="category in availableCategories"
                  :key="category.value"
                  :label="category.label"
                  :value="category.value"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="标签">
              <el-select
                v-model="publishForm.tags"
                multiple
                filterable
                allow-create
                placeholder="选择或输入标签"
                style="width: 100%"
              >
                <el-option
                  v-for="tag in availableTags"
                  :key="tag"
                  :label="tag"
                  :value="tag"
                />
              </el-select>
              <div class="form-help">
                可以选择现有标签或输入新标签
              </div>
            </el-form-item>
          </el-card>

          <!-- 互动设置 -->
          <el-card class="form-section" shadow="never">
            <template #header>
              <h3>互动设置</h3>
            </template>
            
            <el-form-item label="允许评论">
              <el-switch
                v-model="publishForm.allow_comments"
                active-text="允许"
                inactive-text="禁止"
              />
            </el-form-item>

            <el-form-item label="允许评分">
              <el-switch
                v-model="publishForm.allow_ratings"
                active-text="允许"
                inactive-text="禁止"
              />
            </el-form-item>
          </el-card>

          <!-- 访问控制 -->
          <el-card class="form-section" shadow="never">
            <template #header>
              <h3>访问控制</h3>
            </template>
            
            <el-form-item label="密码保护">
              <el-switch
                v-model="publishForm.password_protected"
                active-text="启用"
                inactive-text="禁用"
              />
            </el-form-item>

            <el-form-item 
              v-if="publishForm.password_protected"
              label="访问密码"
            >
              <el-input
                v-model="publishForm.access_password"
                type="password"
                placeholder="输入访问密码"
                show-password
              />
            </el-form-item>
          </el-card>

          <!-- 功能设置 -->
          <el-card class="form-section" shadow="never">
            <template #header>
              <h3>功能设置</h3>
            </template>
            
            <el-form-item label="允许下载">
              <el-switch
                v-model="publishForm.download_enabled"
                active-text="允许"
                inactive-text="禁止"
              />
            </el-form-item>

            <el-form-item label="允许嵌入">
              <el-switch
                v-model="publishForm.embed_enabled"
                active-text="允许"
                inactive-text="禁止"
              />
            </el-form-item>
          </el-card>

          <!-- 操作按钮 -->
          <el-card class="form-section" shadow="never">
            <div class="action-buttons">
              <el-button 
                type="primary" 
                size="large"
                :loading="saving"
                @click="savePublishSettings"
              >
                保存设置
              </el-button>
              
              <el-button 
                size="large"
                @click="previewMedia"
              >
                预览媒体
              </el-button>
              
              <el-button 
                v-if="publishForm.embed_enabled"
                size="large"
                @click="generateEmbedCode"
              >
                获取嵌入代码
              </el-button>
            </div>
          </el-card>
        </el-form>
      </div>
    </div>

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
/* 对应后端模板的样式结构 */
.media-publish-container {
  max-width: 1200px;
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
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
  background: white;
}

.form-section {
  margin-bottom: 24px;
}

.form-section :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.form-section :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.form-section :deep(.el-card__body) {
  padding: 20px;
}

.form-help {
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
  margin-top: 4px;
  line-height: 1.4;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .media-publish-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .user-action-form-inner {
    padding: 16px;
    margin: 0 -4px;
  }
  
  .form-section :deep(.el-card__body) {
    padding: 16px;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .form-section :deep(.el-form-item__label) {
    width: 100px !important;
    font-size: 14px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .publish-container {
  background: #0a0a0a;
}

[data-theme="dark"] .page-header h1 {
  color: #ffffff;
}

[data-theme="dark"] .user-action-form-inner {
  background: #1a1a1a;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .form-section {
  background: #1a1a1a;
  border-color: #333;
}
</style>
