<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { UserAPI } from '@/api'
import type { UserProfile } from '@/api'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const username = computed(() => String(route.params.username))
const loading = ref(false)
const user = ref<UserProfile | null>(null)

// 根据后端模板逻辑，检查用户是否存在
const userExists = computed(() => !!user.value)

async function loadUserProfile() {
  if (!username.value) return
  
  loading.value = true
  try {
    // 这里应该调用用户详情API
    // user.value = await UserAPI.getUserProfile(username.value)
    
    // 模拟用户数据
    user.value = {
      id: 1,
      username: username.value,
      name: username.value,
      email: `${username.value}@example.com`,
      description: '这是一个用户的详细介绍...',
      thumbnail_url: null,
      date_joined: '2024-01-01T00:00:00Z',
      last_login: '2024-10-20T12:00:00Z',
      is_active: true,
      is_editor: false,
      is_manager: false
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
    user.value = null
  } finally {
    loading.value = false
  }
}

function formatDate(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function formatDateTime(dateString?: string) {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString('zh-CN')
}

onMounted(loadUserProfile)
</script>

<template>
  <div class="user-about-container">
    <!-- 对应后端模板的头部信息 -->
    <div class="page-header">
      <h1>
        <span v-if="user?.name">{{ user.name }} - </span>
        关于
      </h1>
    </div>

    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="6" animated />
    </div>

    <!-- 对应后端模板的 {% if user %} 条件检查 -->
    <div v-else-if="userExists">
      <!-- 对应后端的 <div id="page-profile-about"></div> -->
      <div id="page-profile-about" class="profile-about-content">
        
        <!-- 用户基本信息卡片 -->
        <el-card class="user-info-card" shadow="hover">
          <div class="user-profile-header">
            <img 
              :src="user?.thumbnail_url || '/placeholder-avatar.jpg'"
              :alt="user?.username"
              class="user-avatar-large"
            />
            <div class="user-basic-info">
              <h2 class="user-display-name">{{ user?.name || user?.username }}</h2>
              <p class="username">@{{ user?.username }}</p>
              <div class="user-status">
                <el-tag 
                  v-if="user?.is_manager" 
                  type="danger" 
                  size="small"
                >
                  管理员
                </el-tag>
                <el-tag 
                  v-else-if="user?.is_editor" 
                  type="warning" 
                  size="small"
                >
                  编辑者
                </el-tag>
                <el-tag 
                  v-else 
                  type="info" 
                  size="small"
                >
                  用户
                </el-tag>
                <el-tag 
                  :type="user?.is_active ? 'success' : 'danger'" 
                  size="small"
                >
                  {{ user?.is_active ? '活跃' : '非活跃' }}
                </el-tag>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 用户详细信息 -->
        <el-row :gutter="20">
          <el-col :xs="24" :md="12">
            <el-card class="info-section" shadow="never">
              <template #header>
                <h3>基本信息</h3>
              </template>
              
              <div class="info-list">
                <div class="info-item">
                  <label>用户名</label>
                  <span>{{ user?.username }}</span>
                </div>
                
                <div v-if="user?.name" class="info-item">
                  <label>显示名称</label>
                  <span>{{ user.name }}</span>
                </div>
                
                <div v-if="user?.email" class="info-item">
                  <label>邮箱</label>
                  <span>{{ user.email }}</span>
                </div>
                
                <div class="info-item">
                  <label>注册时间</label>
                  <span>{{ formatDate(user?.date_joined) }}</span>
                </div>
                
                <div v-if="user?.last_login" class="info-item">
                  <label>最后登录</label>
                  <span>{{ formatDateTime(user.last_login) }}</span>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <el-col :xs="24" :md="12">
            <el-card class="info-section" shadow="never">
              <template #header>
                <h3>权限信息</h3>
              </template>
              
              <div class="permissions-list">
                <div class="permission-item">
                  <el-icon class="permission-icon">
                    <User />
                  </el-icon>
                  <div class="permission-info">
                    <span class="permission-name">普通用户</span>
                    <span class="permission-desc">基础功能权限</span>
                  </div>
                  <el-icon class="permission-status success">
                    <Check />
                  </el-icon>
                </div>
                
                <div class="permission-item">
                  <el-icon class="permission-icon">
                    <Edit />
                  </el-icon>
                  <div class="permission-info">
                    <span class="permission-name">编辑权限</span>
                    <span class="permission-desc">可以编辑媒体内容</span>
                  </div>
                  <el-icon :class="['permission-status', user?.is_editor ? 'success' : 'disabled']">
                    <component :is="user?.is_editor ? 'Check' : 'Close'" />
                  </el-icon>
                </div>
                
                <div class="permission-item">
                  <el-icon class="permission-icon">
                    <Setting />
                  </el-icon>
                  <div class="permission-info">
                    <span class="permission-name">管理权限</span>
                    <span class="permission-desc">系统管理功能</span>
                  </div>
                  <el-icon :class="['permission-status', user?.is_manager ? 'success' : 'disabled']">
                    <component :is="user?.is_manager ? 'Check' : 'Close'" />
                  </el-icon>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 用户描述 -->
        <el-card v-if="user?.description" class="description-section" shadow="never">
          <template #header>
            <h3>个人介绍</h3>
          </template>
          
          <div class="user-description">
            <p>{{ user.description }}</p>
          </div>
        </el-card>

        <!-- 操作按钮 -->
        <div class="action-buttons">
          <el-button 
            type="primary" 
            @click="router.push(`/user/${username}`)"
          >
            查看媒体
          </el-button>
          
          <el-button 
            @click="router.push(`/user/${username}/playlists`)"
          >
            查看播放列表
          </el-button>
          
          <el-button 
            v-if="auth.profile?.username === username"
            @click="router.push(`/user/${username}/edit`)"
          >
            编辑资料
          </el-button>
        </div>
      </div>
    </div>

    <!-- 对应后端模板的 {% else %} 用户不存在 -->
    <div v-else class="user-not-found">
      <el-result
        icon="warning"
        title="用户不存在"
        sub-title="找不到指定的用户"
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
/* 对应后端的 profile-about.css 样式 */
.user-about-container {
  max-width: 1000px;
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
  margin: 0;
}

.loading-container {
  padding: 40px;
}

.profile-about-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.user-info-card {
  margin-bottom: 8px;
}

.user-profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--el-border-color-light);
}

.user-basic-info {
  flex: 1;
}

.user-display-name {
  margin: 0 0 8px 0;
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
}

.username {
  margin: 0 0 12px 0;
  font-size: 1.1rem;
  color: var(--mc-text-secondary);
}

.user-status {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.info-section {
  height: 100%;
}

.info-section :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.info-section :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.info-item:last-child {
  border-bottom: none;
}

.info-item label {
  font-weight: 600;
  color: var(--mc-text-secondary);
  min-width: 80px;
}

.info-item span {
  color: var(--mc-text-primary);
  text-align: right;
}

.permissions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--mc-bg-secondary);
  border-radius: 8px;
}

.permission-icon {
  font-size: 20px;
  color: var(--el-color-primary);
}

.permission-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.permission-name {
  font-weight: 600;
  color: var(--mc-text-primary);
}

.permission-desc {
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
}

.permission-status {
  font-size: 18px;
}

.permission-status.success {
  color: var(--el-color-success);
}

.permission-status.disabled {
  color: var(--el-color-info);
}

.description-section {
  margin-top: 8px;
}

.user-description p {
  line-height: 1.6;
  color: var(--mc-text-primary);
  margin: 0;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 8px;
}

.user-not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-about-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .user-profile-header {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .user-avatar-large {
    width: 100px;
    height: 100px;
  }
  
  .user-display-name {
    font-size: 1.5rem;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .info-item span {
    text-align: left;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .user-status {
    justify-content: center;
  }
  
  .permission-item {
    padding: 8px;
  }
  
  .permission-icon {
    font-size: 18px;
  }
}
</style>
