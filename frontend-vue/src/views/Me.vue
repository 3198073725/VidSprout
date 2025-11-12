<script setup lang="ts">
/* eslint-disable vue/multi-word-component-names */
import { onMounted, ref, onActivated } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { updateUser } from '@/api/users'
import { MediaAPI } from '@/api'
import type { MediaItem } from '@/api'
import { ElMessage } from 'element-plus'

const auth = useAuthStore()
const router = useRouter()
const form = ref<{ name: string; description: string; logo: File | null }>({ name: '', description: '', logo: null })
const loading = ref(false)
const myMedia = ref<MediaItem[]>([])
const mediaLoading = ref(false)

async function loadProfile() {
  await auth.fetchProfile()
  const p = auth.profile
  if (p) {
    form.value.name = p.name || ''
    form.value.description = p.description || ''
  }
}

async function loadMyMedia() {
  if (!auth.profile?.username) return
  mediaLoading.value = true
  try {
    console.log('🔍 开始加载我的媒体, 用户名:', auth.profile.username)
    const res = await MediaAPI.listMedia({ author: auth.profile.username })
    console.log('📦 API返回的数据:', res)
    console.log('📊 媒体数量:', res?.results?.length)
    myMedia.value = res?.results || []
    console.log('✅ 我的媒体加载成功,共', myMedia.value.length, '个')
    if (myMedia.value.length > 0) {
      console.log('📋 媒体列表:', myMedia.value.map(m => ({ title: m.title, token: m.friendly_token, state: m.state })))
    }
  } catch (error: unknown) {
    console.error('❌ 加载我的媒体失败:', error)
  } finally {
    mediaLoading.value = false
  }
}

onMounted(async () => {
  await loadProfile()
  await loadMyMedia()
})

// 当从其他页面返回时重新加载媒体列表
onActivated(async () => {
  await loadMyMedia()
})

function onFile(e: Event) {
  const files = (e.target as HTMLInputElement).files
  form.value.logo = files && files[0] ? files[0] : null
}

async function onSubmit() {
  if (!auth.profile?.username) return
  loading.value = true
  try {
    await updateUser(auth.profile.username, {
      name: form.value.name || undefined,
      description: form.value.description || undefined,
      logo: form.value.logo || undefined,
    })
    ElMessage.success('资料已更新')
    await auth.fetchProfile()
  } catch (error: unknown) {
    const errorMessage = error && typeof error === 'object' && 'message' in error
      ? (error as { message: string }).message
      : '更新失败'
    ElMessage.error(errorMessage)
  } finally {
    loading.value = false
  }
}

function openMedia(item: MediaItem) {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

function formatDate(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN')
}

function formatDuration(seconds?: number) {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="me-container">
    <!-- 个人资料卡片 -->
    <section class="home-sec" style="max-width:720px; margin-bottom: 24px;">
      <div class="home-sec-head">
        <div class="home-sec-title">个人资料</div>
      </div>
      <el-form label-width="100px" @submit.prevent>
        <el-form-item label="用户名">
          <el-input :model-value="auth.profile?.username || ''" disabled />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="头像">
          <input type="file" accept="image/*" @change="onFile" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="onSubmit">保存</el-button>
          <el-button @click="auth.logout()">退出登录</el-button>
        </el-form-item>
      </el-form>
    </section>

    <!-- 我的媒体列表 -->
    <section class="home-sec" style="max-width:1200px">
      <div class="home-sec-head">
        <div class="home-sec-title">我的媒体 ({{ myMedia.length }})</div>
      </div>

      <!-- 加载状态 -->
      <el-skeleton :loading="mediaLoading" animated>
        <template #template>
          <div class="skeleton-container">
            <el-skeleton-item 
              v-for="n in 3" 
              :key="n"
              variant="rect" 
              style="width: 100%; height: 120px; margin-bottom: 16px"
            />
          </div>
        </template>
        <template #default>
          <!-- 空状态 -->
          <el-empty v-if="!myMedia.length" description="还没有上传任何媒体">
            <el-button type="primary" @click="router.push('/upload')">开始上传</el-button>
          </el-empty>

          <!-- 媒体列表 -->
          <div v-else class="media-list">
            <div 
              v-for="item in myMedia" 
              :key="item.friendly_token"
              class="media-list-item"
              @click="openMedia(item)"
            >
              <div class="media-thumbnail">
                <img 
                  :src="item.thumbnail_url || item.poster_url || '/placeholder.jpg'"
                  :alt="item.title"
                  class="thumbnail-image"
                />
                <div v-if="item.duration" class="duration-badge">
                  {{ formatDuration(item.duration) }}
                </div>
                <div class="state-badge" :class="item.state">
                  {{ item.state === 'private' ? '私密' : item.state === 'unlisted' ? '未列出' : '公开' }}
                </div>
              </div>
              
              <div class="media-info">
                <h3 class="media-title">{{ item.title }}</h3>
                <div class="media-description" v-if="item.description">{{ item.description }}</div>
                <div class="media-stats">
                  {{ item.views || 0 }} 次观看 • {{ item.likes || 0 }} 赞 • {{ formatDate(item.add_date) }}
                </div>
              </div>
            </div>
          </div>
        </template>
      </el-skeleton>
    </section>
  </div>
</template>

<style scoped>
.me-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 媒体列表样式 - 横向列表布局 */
.media-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 0;
}

.media-list-item {
  display: flex;
  flex-direction: row;
  height: 120px;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.media-list-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.media-thumbnail {
  position: relative;
  width: 240px;
  height: 120px;
  flex-shrink: 0;
  background: #f5f5f5;
  overflow: hidden;
}

.thumbnail-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.duration-badge {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.state-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  color: white;
}

.state-badge.public {
  background: #67c23a;
}

.state-badge.private {
  background: #f56c6c;
}

.state-badge.unlisted {
  background: #e6a23c;
}

.media-info {
  flex: 1;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
}

.media-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-description {
  margin: 4px 0;
  font-size: 13px;
  color: #666;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-stats {
  font-size: 13px;
  color: #999;
}

.skeleton-container {
  padding: 16px 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .media-list-item {
    height: auto;
    min-height: 100px;
  }
  
  .media-thumbnail {
    width: 120px;
    height: 100px;
  }
  
  .media-info {
    padding: 8px 12px;
  }
  
  .media-title {
    font-size: 14px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .me-container {
  background: #0a0a0a;
}

[data-theme="dark"] .media-list-item {
  background: #1a1a1a;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .media-list-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .media-thumbnail {
  background: #2a2a2a;
}

[data-theme="dark"] .media-title {
  color: #ffffff;
}

[data-theme="dark"] .media-description {
  color: #999;
}

[data-theme="dark"] .media-stats {
  color: #888;
}

[data-theme="dark"] .duration-badge {
  background: rgba(0, 0, 0, 0.9);
}
</style>
