<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { UserAPI } from '@/api'
import type { UserProfile, Paginated } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()

const loading = ref(false)
const membersList = ref<Paginated<UserProfile> | null>(null)
const currentPage = ref(1)
const pageSize = ref(20)
const searchKeyword = ref('')
const sortBy = ref('date_added')
const sortOrder = ref<'asc' | 'desc'>('desc')
const errorMessage = ref('')

// 后端API支持的排序字段映射
const sortFieldMapping = {
  'date_joined': 'date_added',
  'last_login': 'date_added', // 后端暂不支持最后登录排序，使用注册时间
  'username': 'username',
  'name': 'name'
}

async function loadMembers() {
  loading.value = true
  errorMessage.value = ''
  
  try {
    // 构建API参数
    const params: any = {
      page: currentPage.value
    }
    
    // 搜索参数 - 后端使用name参数进行用户名和姓名搜索
    if (searchKeyword.value) {
      params.name = searchKeyword.value
    }
    
    // 排序参数 - 映射到后端支持的字段
    const backendSortField = (sortFieldMapping as Record<string, string>)[sortBy.value] || 'date_added'
    params.ordering = sortOrder.value === 'desc' ? `-${backendSortField}` : backendSortField
    
    // 调用真实的用户列表API
    const response = await UserAPI.getMembers(params)
    membersList.value = response
    
  } catch (error: any) {
    console.error('加载成员列表失败:', error)
    errorMessage.value = error.response?.data?.detail || '加载成员列表失败，请稍后重试'
    
    // 显示错误消息
    ElMessage.error({
      message: errorMessage.value,
      duration: 5000,
      showClose: true
    })
    
    // 如果是权限错误，显示友好提示
    if (error.response?.status === 403) {
      ElMessage.warning({
        message: '您没有权限查看成员列表',
        duration: 5000,
        showClose: true
      })
    }
  } finally {
    loading.value = false
  }
}

function openUserProfile(member: UserProfile) {
  router.push({ name: 'user-profile', params: { username: member.username } })
}

function formatDate(dateString?: string) {
  if (!dateString) return '从未'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

function formatDateTime(dateString?: string) {
  if (!dateString) return '从未'
  return new Date(dateString).toLocaleString('zh-CN')
}

function getUserRole(member: UserProfile): string {
  if (member.is_manager) return '管理员'
  if (member.is_editor) return '编辑者'
  return '用户'
}

function getUserRoleType(member: UserProfile): 'danger' | 'warning' | 'info' {
  if (member.is_manager) return 'danger'
  if (member.is_editor) return 'warning'
  return 'info'
}

function onSearch() {
  currentPage.value = 1
  loadMembers()
}

function onSortChange() {
  currentPage.value = 1
  loadMembers()
}

function onPageChange(page: number) {
  currentPage.value = page
  loadMembers()
}

function handleSizeChange(size: number) {
  pageSize.value = size
  currentPage.value = 1 // 重置到第一页
  loadMembers()
}

// 监听搜索关键词变化，实现防抖搜索
let searchTimer: NodeJSTimeout | null = null
watch(searchKeyword, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    onSearch()
  }, 500) // 500ms防抖
})

// 头像加载失败处理
function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = '/placeholder-avatar.jpg'
}

onMounted(loadMembers)
</script>

<template>
  <div class="members-container">
    <div class="page-header">
      <h1>社区成员</h1>
      <p>探索我们活跃的社区成员</p>
    </div>

    <!-- 对应后端模板的 <div id="page-members"></div> -->
    <div id="page-members">
      <!-- 搜索和筛选 -->
      <el-card class="filter-card" shadow="never">
        <div class="filter-controls">
          <div class="search-section">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索用户名或姓名"
              clearable
              @keyup.enter="onSearch"
              @clear="onSearch"
              :disabled="loading"
            >
              <template #append>
                <el-button @click="onSearch" :loading="loading">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>
          
          <div class="sort-section">
            <el-select
              v-model="sortBy"
              placeholder="排序字段"
              @change="onSortChange"
              :disabled="loading"
            >
              <el-option label="注册时间" value="date_joined" />
              <el-option label="用户名" value="username" />
              <el-option label="姓名" value="name" />
            </el-select>
            
            <el-select
              v-model="sortOrder"
              placeholder="排序方式"
              @change="onSortChange"
              :disabled="loading"
            >
              <el-option label="降序" value="desc" />
              <el-option label="升序" value="asc" />
            </el-select>
          </div>
        </div>
      </el-card>

      <!-- 错误提示 -->
      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        closable
        @close="errorMessage = ''"
        style="margin-bottom: 16px;"
      />

      <el-skeleton :loading="loading" animated>
        <template #template>
          <div class="members-skeleton">
            <el-skeleton-item 
              v-for="n in 8" 
              :key="n"
              variant="rect" 
              style="width: 100%; height: 120px; margin-bottom: 16px"
            />
          </div>
        </template>

        <template #default>
          <div v-if="membersList?.results?.length" class="members-content">
            <!-- 统计信息 -->
            <el-card class="stats-card" shadow="never">
              <el-statistic 
                title="社区成员总数" 
                :value="membersList.count" 
                suffix="人"
              />
            </el-card>

            <!-- 成员列表 -->
            <div class="members-grid">
              <el-card 
                v-for="member in membersList.results" 
                :key="member.id"
                class="member-card"
                shadow="hover"
                @click="openUserProfile(member)"
              >
                <div class="member-header">
                  <img
                    :src="member.thumbnail_url || '/placeholder-avatar.jpg'"
                    :alt="member.username"
                    class="member-avatar"
                    @error="handleAvatarError"
                  />
                  <div class="member-basic-info">
                    <h3 class="member-name">{{ member.name || member.username }}</h3>
                    <p class="member-username">@{{ member.username }}</p>
                    <el-tag
                      :type="getUserRoleType(member)"
                      size="small"
                    >
                      {{ getUserRole(member) }}
                    </el-tag>
                  </div>
                  <div class="member-status">
                    <el-tag
                      :type="member.is_active ? 'success' : 'info'"
                      size="small"
                    >
                      {{ member.is_active ? '活跃' : '非活跃' }}
                    </el-tag>
                  </div>
                </div>
                
                <div v-if="member.description" class="member-description">
                  <p>{{ member.description }}</p>
                </div>
                
                <div class="member-meta">
                  <div class="meta-item">
                    <span class="meta-label">注册时间:</span>
                    <span class="meta-value">{{ formatDate(member.date_joined) }}</span>
                  </div>
                  <div class="meta-item">
                    <span class="meta-label">最后登录:</span>
                    <span class="meta-value">{{ formatDateTime(member.last_login) }}</span>
                  </div>
                  <div v-if="member.email" class="meta-item">
                    <span class="meta-label">邮箱:</span>
                    <span class="meta-value">{{ member.email }}</span>
                  </div>
                </div>
              </el-card>
            </div>

            <!-- 分页 -->
            <div v-if="membersList.count > pageSize" class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize"
                :total="membersList.count"
                layout="prev, pager, next, jumper, sizes"
                :page-sizes="[10, 20, 50, 100]"
                @current-change="onPageChange"
                @size-change="handleSizeChange"
              />
            </div>
          </div>

          <!-- 空状态 -->
          <el-empty 
            v-else 
            description="没有找到匹配的成员"
            :image-size="120"
          >
            <el-button @click="searchKeyword = ''; onSearch()">
              清除搜索条件
            </el-button>
          </el-empty>
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<style scoped>
.members-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin-bottom: 8px;
}

.page-header p {
  font-size: 1.1rem;
  color: var(--mc-text-secondary);
  margin: 0;
}

.filter-card {
  margin-bottom: 24px;
}

.filter-controls {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.search-section {
  flex: 1;
  min-width: 300px;
}

.sort-section {
  display: flex;
  gap: 8px;
}

.members-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 16px;
}

.members-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.stats-card {
  text-align: center;
  margin-bottom: 8px;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.member-card {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.member-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.member-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.member-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.member-basic-info {
  flex: 1;
}

.member-name {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.member-username {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
}

.member-status {
  flex-shrink: 0;
}

.member-description {
  margin-bottom: 12px;
}

.member-description p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.member-meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.85rem;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.meta-label {
  color: var(--mc-text-secondary);
}

.meta-value {
  color: var(--mc-text-primary);
  font-weight: 500;
}

.pagination-container {
  display: flex;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .members-container {
    padding: 12px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-section {
    min-width: auto;
  }
  
  .sort-section {
    justify-content: center;
  }
  
  .members-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .members-skeleton {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .member-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .member-status {
    align-self: center;
  }
  
  .meta-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 2px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .members-container {
  background: #0a0a0a;
}

[data-theme="dark"] .page-header h1 {
  color: #ffffff;
}

[data-theme="dark"] .page-header p {
  color: #999;
}

[data-theme="dark"] .member-card {
  background: #1a1a1a;
  border-color: #333;
}

[data-theme="dark"] .member-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

[data-theme="dark"] .member-name {
  color: #ffffff;
}

[data-theme="dark"] .member-username {
  color: #4a9eff;
}

[data-theme="dark"] .member-description {
  color: #cccccc;
}

[data-theme="dark"] .meta-label {
  color: #999;
}

[data-theme="dark"] .meta-value {
  color: #ffffff;
}
</style>
