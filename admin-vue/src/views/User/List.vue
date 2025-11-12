<template>
  <div class="user-list-container">
    <el-card>
      <!-- 搜索和筛选 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户名或邮箱..."
            clearable
            style="width: 300px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <el-select v-model="filters.role" placeholder="角色" clearable style="width: 140px" @change="handleSearch">
            <el-option label="全部用户" value="all" />
            <el-option label="超级管理员" value="admin" />
            <el-option label="管理员" value="manager" />
            <el-option label="编辑" value="editor" />
            <el-option label="普通用户" value="user" />
          </el-select>

          <el-select v-model="filters.is_active" placeholder="状态" clearable style="width: 120px" @change="handleSearch">
            <el-option label="活跃" :value="true" />
            <el-option label="已封禁" :value="false" />
          </el-select>
        </div>

        <div class="toolbar-right">
          <el-dropdown :disabled="selectedUsers.length === 0" @command="handleBatchAction">
            <el-button type="primary">
              批量操作 ({{ selectedUsers.length }})
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="block">
                  <el-icon><Lock /></el-icon>
                  批量封禁
                </el-dropdown-item>
                <el-dropdown-item command="unblock">
                  <el-icon><Unlock /></el-icon>
                  批量解封
                </el-dropdown-item>
                <el-dropdown-item divided command="set_manager">
                  <el-icon><Setting /></el-icon>
                  设为管理者
                </el-dropdown-item>
                <el-dropdown-item command="set_editor">
                  <el-icon><Edit /></el-icon>
                  设为编辑者
                </el-dropdown-item>
                <el-dropdown-item command="remove_role">
                  <el-icon><Close /></el-icon>
                  移除角色
                </el-dropdown-item>
                <el-dropdown-item divided command="delete" style="color: var(--el-color-danger)">
                  <el-icon><Delete /></el-icon>
                  批量删除
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <el-button @click="handleRefresh">
            <el-icon><RefreshRight /></el-icon>
            刷新
          </el-button>
        </div>
      </div>

      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="userList"
        style="width: 100%; margin-top: 20px"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="头像" width="80">
          <template #default="{ row }">
            <el-avatar :size="40" :src="row.logo">
              <el-icon><User /></el-icon>
            </el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" min-width="120" show-overflow-tooltip />
        <el-table-column prop="name" label="姓名" min-width="120" show-overflow-tooltip />
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column label="角色" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.is_superuser" type="danger" size="small">超级管理员</el-tag>
            <el-tag v-else-if="row.is_staff" type="warning" size="small">管理员</el-tag>
            <el-tag v-else type="info" size="small">普通用户</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '活跃' : '已封禁' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.date_joined) }}
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="最后登录" width="160">
          <template #default="{ row }">
            {{ formatDate(row.last_login) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewUser(row)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button type="warning" link @click="editUser(row)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button 
              :type="row.is_active ? 'danger' : 'success'" 
              link 
              @click="toggleUserStatus(row)"
            >
              <el-icon v-if="row.is_active"><Lock /></el-icon>
              <el-icon v-else><Unlock /></el-icon>
              {{ row.is_active ? '封禁' : '解封' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; justify-content: flex-end"
        @size-change="handleSearch"
        @current-change="handleSearch"
      />
    </el-card>

    <!-- 用户详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`用户详情 - ${currentUser?.username}`"
      width="800px"
    >
      <el-descriptions v-if="currentUser" :column="2" border>
        <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentUser.name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentUser.email }}</el-descriptions-item>
        <el-descriptions-item label="角色">
          <el-tag v-if="currentUser.is_superuser" type="danger">超级管理员</el-tag>
          <el-tag v-else-if="currentUser.is_staff" type="warning">管理员</el-tag>
          <el-tag v-else type="info">普通用户</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentUser.is_active ? 'success' : 'danger'">
            {{ currentUser.is_active ? '活跃' : '已封禁' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间">
          {{ formatDate(currentUser.date_joined) }}
        </el-descriptions-item>
        <el-descriptions-item label="最后登录">
          {{ formatDate(currentUser.last_login) }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="editUser(currentUser)">编辑</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  getManageUsers, 
  blockUser, 
  unblockUser,
  batchBlockUsers,
  batchUnblockUsers,
  batchDeleteUsers,
  batchSetEditor,
  batchSetManager,
  batchRemoveRole
} from '@/api/admin'
import type { UserProfile } from '@/api/types'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const userList = ref<UserProfile[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')
const selectedUsers = ref<UserProfile[]>([])
const detailDialogVisible = ref(false)
const currentUser = ref<UserProfile | null>(null)

const filters = ref({
  role: 'all' as string,
  is_active: undefined as undefined | boolean
})

// 加载用户列表
const loadUsers = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value,
      role: filters.value.role,
      is_active: filters.value.is_active
    }
    
    const response = await getManageUsers(params)
    userList.value = response.results
    total.value = response.count
  } catch (error) {
    ElMessage.error('加载用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadUsers()
}

const handleRefresh = () => {
  loadUsers()
}

const handleSelectionChange = (selection: UserProfile[]) => {
  selectedUsers.value = selection
}

const viewUser = (user: UserProfile) => {
  currentUser.value = user
  detailDialogVisible.value = true
}

const editUser = (user: UserProfile | null) => {
  if (!user) return
  router.push(`/users/detail/${user.id}`)
}

const toggleUserStatus = async (user: UserProfile) => {
  const action = user.is_active ? '封禁' : '解封'
  try {
    await ElMessageBox.confirm(`确定要${action}用户"${user.username}"吗？`, '提示', {
      type: 'warning'
    })
    
    loading.value = true
    
    // 调用封禁/解封API
    if (user.is_active) {
      await blockUser(user.id)
    } else {
      await unblockUser(user.id)
    }
    
    ElMessage.success(`${action}成功`)
    loadUsers() // 重新加载列表
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error(`${action}用户失败:`, error)
      ElMessage.error(`${action}失败`)
    }
  } finally {
    loading.value = false
  }
}

const handleBatchAction = async (action: string) => {
  const actionNames: Record<string, string> = {
    delete: '删除',
    block: '封禁',
    unblock: '解封',
    set_manager: '设为管理者',
    set_editor: '设为编辑者',
    remove_role: '移除角色'
  }
  
  const actionName = actionNames[action] || action
  const count = selectedUsers.value.length
  
  try {
    await ElMessageBox.confirm(
      `确定要${actionName}选中的 ${count} 个用户吗？${action === 'delete' ? '此操作不可撤销！' : ''}`,
      '提示',
      { type: action === 'delete' ? 'error' : 'warning' }
    )
    
    loading.value = true
    
    const userIds = selectedUsers.value.map(u => String(u.id))
    
    // 根据不同的操作调用对应的 API 函数
    switch (action) {
      case 'delete':
        await batchDeleteUsers(userIds)
        break
      case 'block':
        await batchBlockUsers(userIds)
        break
      case 'unblock':
        await batchUnblockUsers(userIds)
        break
      case 'set_manager':
        await batchSetManager(userIds)
        break
      case 'set_editor':
        await batchSetEditor(userIds)
        break
      case 'remove_role':
        await batchRemoveRole(userIds)
        break
      default:
        throw new Error(`未知操作: ${action}`)
    }
    
    ElMessage.success(`${actionName}成功`)
    selectedUsers.value = []
    loadUsers()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error(`批量${actionName}失败:`, error)
      ElMessage.error(`批量${actionName}失败`)
    }
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string | undefined) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped lang="scss">
.user-list-container {
  height: 100%;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.toolbar-left,
.toolbar-right {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

:deep(.el-descriptions__label) {
  width: 120px;
}
</style>
