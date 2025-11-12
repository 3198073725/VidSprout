<template>
  <div class="manage-users">
    <div class="header">
      <h1>用户管理</h1>
      <p class="description">管理所有用户，支持按角色筛选</p>
      <div class="header-actions">
        <el-button-group>
          <el-button
            type="primary"
            @click="showStats = !showStats"
            :icon="TrendCharts"
          >
            {{ showStats ? '隐藏统计' : '显示统计' }}
          </el-button>
          <el-button
            type="success"
            @click="handleExport"
            :icon="Download"
          >
            导出数据
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 数据统计图表 -->
    <AdminStatsCharts
      v-if="showStats"
      :stats-data="statsData"
      @refresh="loadStats"
      @export="handleExport"
    />

    <!-- 批量操作 -->
    <BatchOperations
      :selected-ids="selectedUsers"
      operation-type="users"
      @batch-operation="handleBatchOperation"
      @completed="handleBatchCompleted"
    />

    <!-- 筛选工具栏 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="排序字段">
          <el-select v-model="filters.sort_by" placeholder="选择排序字段" @change="loadUsers">
            <el-option label="用户名" value="username" />
            <el-option label="姓名" value="name" />
            <el-option label="注册时间" value="date_joined" />
            <el-option label="最后登录" value="last_login" />
          </el-select>
        </el-form-item>

        <el-form-item label="排序方式">
          <el-select v-model="filters.ordering" placeholder="选择排序方式" @change="loadUsers">
            <el-option label="升序" value="asc" />
            <el-option label="降序" value="desc" />
          </el-select>
        </el-form-item>

        <el-form-item label="角色筛选">
          <el-select v-model="filters.role" placeholder="选择角色" @change="loadUsers">
            <el-option label="全部" value="all" />
            <el-option label="普通用户" value="user" />
            <el-option label="编辑者" value="editor" />
            <el-option label="管理者" value="manager" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="loadUsers">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="userList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="序号" type="index" width="60" />

        <el-table-column label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="40" :src="row.thumbnail_url || undefined">
              {{ row.username?.charAt(0).toUpperCase() }}
            </el-avatar>
          </template>
        </el-table-column>

        <el-table-column label="用户名" width="150">
          <template #default="{ row }">
            <div class="username-cell">
              <span class="username">{{ row.username }}</span>
              <el-tag v-if="row.email_is_verified" type="success" size="small">
                <el-icon><Check /></el-icon>
                已验证
              </el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="姓名" width="120">
          <template #default="{ row }">
            {{ row.name || '-' }}
          </template>
        </el-table-column>

        <el-table-column label="角色" width="150">
          <template #default="{ row }">
            <div class="roles">
              <el-tag v-if="row.is_staff" type="danger" size="small">管理员</el-tag>
              <el-tag v-if="row.is_manager" type="warning" size="small">管理者</el-tag>
              <el-tag v-if="row.is_editor" type="primary" size="small">编辑者</el-tag>
              <el-tag v-if="!row.is_staff && !row.is_manager && !row.is_editor" type="info" size="small">用户</el-tag>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="邮箱" min-width="200">
          <template #default="{ row }">
            {{ row.email || '-' }}
          </template>
        </el-table-column>

        <el-table-column label="描述" min-width="200">
          <template #default="{ row }">
            {{ row.description || '-' }}
          </template>
        </el-table-column>

        <el-table-column label="注册时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.date_added) }}
          </template>
        </el-table-column>

        <el-table-column label="最后登录" width="160">
          <template #default="{ row }">
            {{ formatDate(row.last_login) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              link
              @click="viewUser(row)"
            >
              <el-icon><View /></el-icon>
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadUsers"
          @current-change="loadUsers"
        />
      </div>
    </el-card>

    <!-- 用户详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="用户详情"
      width="700px"
    >
      <div v-if="currentUser" class="user-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="头像" :span="2">
            <el-avatar :size="80" :src="currentUser.thumbnail_url || undefined">
              {{ currentUser.username?.charAt(0).toUpperCase() }}
            </el-avatar>
          </el-descriptions-item>

          <el-descriptions-item label="用户名">
            {{ currentUser.username }}
          </el-descriptions-item>

          <el-descriptions-item label="姓名">
            {{ currentUser.name || '-' }}
          </el-descriptions-item>

          <el-descriptions-item label="邮箱" :span="2">
            {{ currentUser.email || '-' }}
            <el-tag v-if="currentUser.email_is_verified" type="success" size="small" style="margin-left: 8px">
              <el-icon><Check /></el-icon>
              已验证
            </el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="角色" :span="2">
            <div class="roles">
              <el-tag v-if="currentUser.is_staff" type="danger" size="small">管理员</el-tag>
              <el-tag v-if="currentUser.is_manager" type="warning" size="small">管理者</el-tag>
              <el-tag v-if="currentUser.is_editor" type="primary" size="small">编辑者</el-tag>
              <el-tag v-if="!currentUser.is_staff && !currentUser.is_manager && !currentUser.is_editor" type="info" size="small">普通用户</el-tag>
            </div>
          </el-descriptions-item>

          <el-descriptions-item label="描述" :span="2">
            {{ currentUser.description || '-' }}
          </el-descriptions-item>

          <el-descriptions-item label="注册时间">
            {{ formatDate(currentUser.date_added) }}
          </el-descriptions-item>

          <el-descriptions-item label="最后登录">
            {{ formatDate(currentUser.last_login) }}
          </el-descriptions-item>

          <el-descriptions-item label="个人主页" :span="2" v-if="currentUser.url">
            <a :href="currentUser.url" target="_blank">{{ currentUser.url }}</a>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Refresh, View, Check, TrendCharts, Download } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import * as AdminAPI from '@/api/admin'
import type { UserProfile } from '@/api/users'
import AdminStatsCharts from '@/components/AdminStatsCharts.vue'
import BatchOperations from '@/components/BatchOperations.vue'

const router = useRouter()
const auth = useAuthStore()

// 权限检查
const isAdmin = computed(() => {
  const profile = auth.profile as {is_staff?: boolean} | null
  return profile?.is_staff || false
})

// 数据状态
const loading = ref(false)
const userList = ref<UserProfile[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const detailDialogVisible = ref(false)
const currentUser = ref<UserProfile | null>(null)
const selectedUsers = ref<string[]>([])
const statsData = ref<any>(null)
const showStats = ref(false)

// 筛选条件
const filters = ref<{
  sort_by: 'username' | 'name' | 'date_joined' | 'last_login'
  ordering: 'asc' | 'desc'
  role: 'all' | 'user' | 'editor' | 'manager' | 'admin'
}>({
  sort_by: 'date_joined',
  ordering: 'desc',
  role: 'all'
})

// 加载用户列表
async function loadUsers() {
  if (!isAdmin.value) {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
    return
  }

  loading.value = true
  try {
    const params: AdminAPI.ManageUsersParams = {
      page: currentPage.value,
      sort_by: filters.value.sort_by,
      ordering: filters.value.ordering
    }

    if (filters.value.role !== 'all') {
      params.role = filters.value.role
    }

    const response = await AdminAPI.getManageUsers(params)
    userList.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载用户列表失败:', error)
    ElMessage.error('加载失败，请稍后再试')
  } finally {
    loading.value = false
  }
}

// 查看用户详情
function viewUser(user: UserProfile) {
  currentUser.value = user
  detailDialogVisible.value = true
}

// 格式化日期
function formatDate(dateString: string | undefined): string {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载统计数据
async function loadStats() {
  try {
    const response = await AdminAPI.getAdminStats({ date_range: '30d' })
    statsData.value = response
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

// 批量操作处理
async function handleBatchOperation(operation: string, data: any) {
  try {
    const result = await AdminAPI.executeBatchOperation(data)
    if (result.success) {
      ElMessage.success(`批量操作成功，处理了 ${result.processed} 个用户`)
      loadUsers() // 重新加载数据
    } else {
      ElMessage.error(`批量操作失败: ${result.errors?.join(', ')}`)
    }
  } catch (error) {
    ElMessage.error('批量操作失败')
    throw error
  }
}

// 数据导出
async function handleExport() {
  try {
    const result = await AdminAPI.exportData({
      type: 'users',
      format: 'excel',
      filters: {
        role: filters.value.role
      }
    })
    
    // 下载文件
    const link = document.createElement('a')
    link.href = result.download_url
    link.download = result.filename
    link.click()
    
    ElMessage.success('数据导出成功')
  } catch (error) {
    ElMessage.error('数据导出失败')
  }
}

// 表格选择变化
function handleSelectionChange(selection: UserProfile[]) {
  selectedUsers.value = selection.map(item => item.username)
}

// 批量操作完成处理
function handleBatchCompleted(results: any) {
  // 清空选择
  selectedUsers.value = []
  ElMessage.success(`批量操作完成：成功 ${results.success} 个，失败 ${results.failed} 个`)
}

// 初始化
onMounted(() => {
  if (isAdmin.value) {
    loadUsers()
    loadStats()
  } else {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
  }
})
</script>

<style scoped lang="scss">
.manage-users {
  padding: 24px;
  max-width: 1600px;
  margin: 0 auto;

  .header {
    margin-bottom: 24px;

    h1 {
      font-size: 28px;
      font-weight: 600;
      color: #1f2937;
      margin: 0 0 8px 0;
    }

    .description {
      font-size: 14px;
      color: #6b7280;
      margin: 0;
    }
  }

  .filter-card {
    margin-bottom: 16px;

    .filter-form {
      margin: 0;

      :deep(.el-form-item) {
        margin-bottom: 0;
      }
    }
  }

  .table-card {
    .username-cell {
      display: flex;
      flex-direction: column;
      gap: 6px;

      .username {
        font-weight: 500;
        color: #374151;
      }
    }

    .roles {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .pagination-container {
      display: flex;
      justify-content: flex-end;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #e5e7eb;
    }
  }

  .user-detail {
    .roles {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    a {
      color: #3b82f6;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .manage-users {
    padding: 16px;

    .header h1 {
      font-size: 24px;
    }

    .filter-card {
      :deep(.el-form--inline) {
        .el-form-item {
          display: block;
          margin-right: 0;
          margin-bottom: 12px;
        }
      }
    }

    .table-card {
      :deep(.el-table) {
        font-size: 12px;
      }

      .pagination-container {
        :deep(.el-pagination) {
          justify-content: center;

          .el-pagination__sizes,
          .el-pagination__jump {
            display: none;
          }
        }
      }
    }
  }
}
</style>
