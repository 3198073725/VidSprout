<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const saving = ref(false)
const channelForm = ref({
  name: '',
  description: '',
  thumbnail: null as File | null,
  is_public: true,
  allow_comments: true
})

const channelId = route.params.id as string

async function loadChannel() {
  if (!channelId) return
  
  loading.value = true
  try {
    // 这里应该调用频道详情API
    // const channel = await ChannelAPI.getChannel(channelId)
    
    // 模拟数据
    channelForm.value = {
      name: '我的频道',
      description: '这是一个示例频道描述',
      thumbnail: null,
      is_public: true,
      allow_comments: true
    }
  } catch (error) {
    console.error('加载频道失败:', error)
    ElMessage.error('加载频道失败')
  } finally {
    loading.value = false
  }
}

async function updateChannel() {
  saving.value = true
  try {
    // 这里应该调用更新频道API
    // await ChannelAPI.updateChannel(channelId, channelForm.value)
    
    ElMessage.success('频道更新成功')
    router.push('/channels')
  } catch (error) {
    console.error('更新频道失败:', error)
    ElMessage.error('更新频道失败')
  } finally {
    saving.value = false
  }
}

function handleThumbnailChange(file: File) {
  channelForm.value.thumbnail = file
}

onMounted(loadChannel)
</script>

<template>
  <div class="channel-edit-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>编辑频道</h1>
        
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="6" animated />
        </div>
        
        <!-- 对应后端模板的表单 -->
        <el-form 
          v-else
          :model="channelForm" 
          label-width="120px"
          @submit.prevent="updateChannel"
        >
          <el-form-item label="频道名称" required>
            <el-input
              v-model="channelForm.name"
              placeholder="输入频道名称"
              :disabled="saving"
            />
          </el-form-item>
          
          <el-form-item label="频道描述">
            <el-input
              v-model="channelForm.description"
              type="textarea"
              :rows="4"
              placeholder="输入频道描述"
              :disabled="saving"
            />
          </el-form-item>
          
          <el-form-item label="频道缩略图">
            <el-upload
              :auto-upload="false"
              :show-file-list="false"
              accept="image/*"
              :on-change="(file: any) => handleThumbnailChange(file.raw)"
            >
              <el-button :disabled="saving">
                <el-icon><Upload /></el-icon>
                选择图片
              </el-button>
            </el-upload>
            <div v-if="channelForm.thumbnail" class="upload-tip">
              已选择: {{ channelForm.thumbnail.name }}
            </div>
          </el-form-item>
          
          <el-form-item label="频道设置">
            <div class="channel-settings">
              <el-checkbox 
                v-model="channelForm.is_public"
                :disabled="saving"
              >
                公开频道
              </el-checkbox>
              
              <el-checkbox 
                v-model="channelForm.allow_comments"
                :disabled="saving"
              >
                允许评论
              </el-checkbox>
            </div>
          </el-form-item>
          
          <el-form-item>
            <!-- 对应后端模板的提交按钮 -->
            <el-button 
              type="primary" 
              :loading="saving"
              @click="updateChannel"
              size="large"
            >
              {{ saving ? '更新中...' : '更新频道' }}
            </el-button>
            
            <el-button 
              @click="router.go(-1)"
              :disabled="saving"
              size="large"
            >
              取消
            </el-button>
          </el-form-item>
        </el-form>
        
        <!-- 帮助信息 -->
        <el-card class="help-info" shadow="never">
          <template #header>
            <h3>频道编辑说明</h3>
          </template>
          
          <div class="help-content">
            <ul>
              <li><strong>频道名称</strong>：为您的频道选择一个有意义的名称</li>
              <li><strong>频道描述</strong>：简要描述您的频道内容和主题</li>
              <li><strong>缩略图</strong>：上传一张代表您频道的图片</li>
              <li><strong>公开频道</strong>：其他用户可以发现和订阅您的频道</li>
              <li><strong>允许评论</strong>：用户可以在您的频道内容下留言</li>
            </ul>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.channel-edit-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* 对应后端模板的 user-action-form-wrap 样式 */
.user-action-form-wrap {
  display: flex;
  justify-content: center;
}

.user-action-form-inner {
  width: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 32px;
}

.user-action-form-inner h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 32px 0;
}

.loading-container {
  padding: 20px;
}

.channel-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.upload-tip {
  margin-top: 8px;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
}

.help-info {
  margin-top: 24px;
}

.help-info :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.help-info :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.help-content ul {
  margin: 0;
  padding-left: 20px;
  color: var(--mc-text-secondary);
}

.help-content li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.help-content strong {
  color: var(--mc-text-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .channel-edit-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .user-action-form-inner h1 {
    font-size: 1.5rem;
  }
  
  .el-form :deep(.el-form-item__label) {
    width: 100px !important;
  }
}

@media (max-width: 480px) {
  .el-form :deep(.el-form-item) {
    flex-direction: column;
  }
  
  .el-form :deep(.el-form-item__label) {
    width: 100% !important;
    text-align: left;
    margin-bottom: 8px;
  }
}
</style>
