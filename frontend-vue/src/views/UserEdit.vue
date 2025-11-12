<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const emailNotifications = ref(true)
const form = ref({
  name: '',
  description: '',
  logo: null as File | null,
})

const logoPreview = ref<string>('')

onMounted(() => {
  if (!auth.profile) {
    ElMessage.error('请先登录')
    router.push('/login')
    return
  }
  
  // 加载当前用户信息
  form.value.name = auth.profile.name || ''
  form.value.description = auth.profile.description || ''
  logoPreview.value = auth.profile.thumbnail_url || ''
  emailNotifications.value = auth.profile.notification_on_comments !== false // 默认为 true
})

function handleLogoChange(file: any) {
  if (file.raw) {
    form.value.logo = file.raw
    // 创建预览
    const reader = new FileReader()
    reader.onload = (e) => {
      logoPreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file.raw)
  }
}

function clearLogo() {
  form.value.logo = null
  logoPreview.value = auth.profile?.thumbnail_url || ''
}

async function onSubmit() {
  if (!auth.profile) return
  
  loading.value = true
  try {
    const formData = new FormData()
    if (form.value.name) formData.append('name', form.value.name)
    if (form.value.description) formData.append('description', form.value.description)
    if (form.value.logo) formData.append('logo', form.value.logo)
    formData.append('notification_on_comments', emailNotifications.value ? 'true' : 'false')
    
    const response = await fetch(`/api/v1/users/${auth.profile.username}`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${auth.token}`
      },
      body: formData
    })
    
    if (!response.ok) {
      throw new Error('更新失败')
    }
    
    ElMessage.success('资料更新成功')
    // 刷新用户信息
    await auth.fetchProfile()
    router.push(`/user/${auth.profile.username}`)
  } catch (error: any) {
    ElMessage.error(error.message || '更新失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="user-edit">
    <div class="edit-container">
      <h1>编辑个人资料</h1>
      
      <el-form :model="form" label-position="top" @submit.prevent="onSubmit">
        <el-form-item label="姓名:">
          <el-input v-model="form.name" placeholder="" />
        </el-form-item>
        
        <el-form-item label="关于我:">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="6"
            placeholder=""
          />
        </el-form-item>
        
        <el-form-item>
          <div class="logo-wrapper">
            <div class="logo-row">
              <span class="field-label">头像:</span>
              <span class="row-label">目前:</span>
              <div class="row-content">
                <a v-if="logoPreview" :href="logoPreview" target="_blank" class="logo-link">
                  {{ logoPreview.split('/').pop() }}
                </a>
                <span v-else>无</span>
                <el-button 
                  text 
                  type="danger" 
                  size="small"
                  v-if="logoPreview && form.logo"
                  @click="clearLogo"
                  style="margin-left: 8px"
                >
                  清除
                </el-button>
              </div>
            </div>
            <div class="logo-row">
              <span class="field-label"></span>
              <span class="row-label">修改:</span>
              <div class="row-content">
                <el-upload
                  :auto-upload="false"
                  :show-file-list="false"
                  :on-change="handleLogoChange"
                  accept="image/*"
                  class="inline-upload"
                >
                  <el-button size="small">
                    选择文件
                  </el-button>
                </el-upload>
                <span v-if="form.logo" class="file-name">{{ form.logo.name }}</span>
                <span v-else class="no-file">未选择任何文件</span>
              </div>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="emailNotifications">
            是否接收评论的邮件通知:
          </el-checkbox>
        </el-form-item>
        
        <el-form-item>
          <el-button type="success" :loading="loading" @click="onSubmit">
            更新资料
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<style scoped>
.user-edit {
  padding: 32px 16px;
}

.edit-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  background: var(--mc-bg-primary, #fff);
  padding: 40px;
  border-radius: var(--mc-radius, 8px);
  box-shadow: var(--mc-shadow, 0 2px 12px rgba(0, 0, 0, 0.08));
}

[data-theme="dark"] .edit-container {
  background: #1a1a1a;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
}

.edit-container h1 {
  font-size: 28px;
  font-weight: var(--mc-font-normal, 400);
  margin-bottom: 32px;
  color: var(--mc-text-primary, #222);
  font-family: var(--mc-font-family, 'Roboto', sans-serif);
}

[data-theme="dark"] .edit-container h1 {
  color: #ffffff;
}

/* 表单样式 */
.edit-container :deep(.el-form-item__label) {
  font-weight: var(--mc-font-normal, 400);
  color: var(--mc-text-secondary, #333);
  font-size: 14px;
}

[data-theme="dark"] .edit-container :deep(.el-form-item__label) {
  color: #cccccc !important;
}

.edit-container :deep(.el-input__wrapper) {
  border-radius: var(--mc-radius-sm, 4px);
}

.edit-container :deep(.el-textarea__inner) {
  border-radius: var(--mc-radius-sm, 4px);
  font-family: var(--mc-font-family, 'Roboto', sans-serif);
}

/* Logo 部分 */
.logo-wrapper {
  font-size: 14px;
  color: var(--mc-text-secondary, #333);
}

[data-theme="dark"] .logo-wrapper {
  color: #cccccc;
}

.logo-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.logo-row:last-child {
  margin-bottom: 0;
}

.field-label {
  font-weight: var(--mc-font-medium, 500);
  min-width: 50px;
  flex-shrink: 0;
}

.row-label {
  font-weight: var(--mc-font-medium, 500);
  color: var(--mc-text-secondary, #333);
  min-width: 50px;
  flex-shrink: 0;
}

[data-theme="dark"] .row-label {
  color: #cccccc;
}

.row-content {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.logo-link {
  color: var(--mc-primary, #2ecc71);
  text-decoration: none;
}

.logo-link:hover {
  text-decoration: underline;
}

.inline-upload {
  display: inline-flex;
  align-items: center;
}

.file-name {
  color: var(--mc-text-secondary, #333);
}

[data-theme="dark"] .file-name {
  color: #cccccc;
}

.no-file {
  color: var(--mc-text-light, #666);
}

[data-theme="dark"] .no-file {
  color: #999;
}

/* Checkbox */
.edit-container :deep(.el-checkbox__label) {
  font-size: 14px;
  color: var(--mc-text-secondary, #333);
  line-height: 1.6;
}

[data-theme="dark"] .edit-container :deep(.el-checkbox__label) {
  color: #cccccc;
}
</style>
