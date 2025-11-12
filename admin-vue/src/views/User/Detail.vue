<template>
  <div class="user-detail-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>用户详情</span>
          <el-button @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
      </template>
      
      <el-form
        v-if="userForm"
        ref="formRef"
        :model="userForm"
        :rules="rules"
        label-width="120px"
        style="max-width: 800px"
      >
        <!-- 基本信息 -->
        <el-divider content-position="left">基本信息</el-divider>
        
        <el-form-item label="用户头像">
          <el-avatar :size="80" :src="userForm.logo">
            <el-icon :size="40"><User /></el-icon>
          </el-avatar>
        </el-form-item>

        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" disabled />
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input v-model="userForm.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" disabled />
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input 
            v-model="userForm.description"
            type="textarea"
            :rows="4"
            placeholder="请输入用户描述"
          />
        </el-form-item>

        <!-- 权限设置 -->
        <el-divider content-position="left">权限设置</el-divider>

        <el-form-item label="账号状态">
          <el-switch
            v-model="userForm.is_active"
            active-text="正常"
            inactive-text="已封禁"
          />
        </el-form-item>

        <el-form-item label="超级管理员">
          <el-switch v-model="userForm.is_superuser" />
          <span class="hint">拥有所有权限</span>
        </el-form-item>

        <el-form-item label="管理员">
          <el-switch v-model="userForm.is_staff" />
          <span class="hint">可以访问管理后台</span>
        </el-form-item>

        <el-form-item label="管理者角色">
          <el-switch v-model="userForm.is_manager" />
          <span class="hint">MediaCMS管理者</span>
        </el-form-item>

        <el-form-item label="编辑者角色">
          <el-switch v-model="userForm.is_editor" />
          <span class="hint">MediaCMS编辑者</span>
        </el-form-item>

        <!-- 统计信息 -->
        <el-divider content-position="left">统计信息</el-divider>

        <el-form-item label="注册时间">
          <span>{{ formatDate(userForm.date_joined) }}</span>
        </el-form-item>

        <el-form-item label="最后登录">
          <span>{{ formatDate(userForm.last_login) }}</span>
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
            删除用户
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import type { UserProfile } from '@/api/types'
import dayjs from 'dayjs'
import http from '@/api/http'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const formRef = ref<FormInstance>()
const userForm = ref<UserProfile | null>(null)
const originalData = ref<UserProfile | null>(null)

const rules = {
  name: [
    { max: 100, message: '姓名不能超过100个字符', trigger: 'blur' }
  ]
}

// 加载用户详情
const loadUserDetail = async () => {
  const userId = route.params.id
  if (!userId) {
    ElMessage.error('用户ID缺失')
    router.back()
    return
  }

  loading.value = true
  try {
    // 使用专门的用户详情API
    const user = await http.get(`/v1/admin/users/${userId}`)
    
    userForm.value = { ...user }
    originalData.value = { ...user }
  } catch (error: any) {
    console.error('加载用户详情失败:', error)
    if (error.response?.status === 404) {
      ElMessage.error('用户不存在')
    } else {
      ElMessage.error(error.response?.data?.detail || '加载用户详情失败')
    }
    router.back()
  } finally {
    loading.value = false
  }
}

const formatDate = (date: string | undefined) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const handleSubmit = async () => {
  if (!formRef.value || !userForm.value) return

  try {
    await formRef.value.validate()
    
    loading.value = true
    
    // 调用更新用户API
    await http.patch(`/v1/admin/users/${userForm.value.id}`, {
      name: userForm.value.name,
      description: userForm.value.description,
      is_active: userForm.value.is_active,
      is_superuser: userForm.value.is_superuser,
      is_staff: userForm.value.is_staff,
      is_manager: userForm.value.is_manager,
      is_editor: userForm.value.is_editor
    })

    ElMessage.success('保存成功')
    originalData.value = { ...userForm.value }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('保存用户失败:', error)
      ElMessage.error('保存失败')
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  if (originalData.value) {
    userForm.value = { ...originalData.value }
    ElMessage.info('已重置为原始数据')
  }
}

const handleDelete = async () => {
  if (!userForm.value) return

  try {
    await ElMessageBox.confirm(
      `确定要删除用户"${userForm.value.username}"吗？此操作不可撤销！`,
      '危险操作',
      {
        type: 'error',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消'
      }
    )

    loading.value = true
    
    // 调用删除用户API
    await http.delete(`/v1/admin/users/${userForm.value.id}`)
    
    ElMessage.success('删除成功')
    router.push('/users/list')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUserDetail()
})
</script>

<style scoped lang="scss">
.user-detail-container {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hint {
  margin-left: 12px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

:deep(.el-divider__text) {
  font-size: 16px;
  font-weight: 600;
}
</style>
