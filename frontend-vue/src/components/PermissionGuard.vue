<template>
  <div class="permission-guard">
    <slot v-if="hasPermission" />
    <div v-else class="permission-denied">
      <el-result
        icon="warning"
        title="权限不足"
        sub-title="您没有权限访问此功能"
      >
        <template #extra>
          <el-button type="primary" @click="goBack">返回</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

interface Props {
  permission?: string | string[]
  role?: string | string[]
  fallback?: string
}

const props = withDefaults(defineProps<Props>(), {
  permission: undefined,
  role: undefined,
  fallback: '/'
})

const router = useRouter()
const authStore = useAuthStore()

const hasPermission = computed(() => {
  // 超级管理员拥有所有权限
  if (authStore.isAdmin) {
    return true
  }

  // 检查角色权限
  if (props.role) {
    const requiredRoles = Array.isArray(props.role) ? props.role : [props.role]
    const userRoles = authStore.profile?.is_manager ? ['manager'] : []
    
    const hasRole = requiredRoles.some(role => userRoles.includes(role))
    if (!hasRole) {
      return false
    }
  }

  // 检查特定权限
  if (props.permission) {
    const requiredPermissions = Array.isArray(props.permission) ? props.permission : [props.permission]
    const userPermissions = authStore.profile?.is_editor ? ['editor'] : []
    
    const hasSpecificPermission = requiredPermissions.some(permission => 
      userPermissions.includes(permission) || authStore.isAdmin
    )
    if (!hasSpecificPermission) {
      return false
    }
  }

  return true
})

function goBack() {
  if (props.fallback && props.fallback !== '/') {
    router.push(props.fallback)
  } else {
    router.back()
  }
}

// 如果没有权限，显示提示
if (!hasPermission.value) {
  ElMessage.warning('您没有权限访问此功能')
}
</script>

<style scoped>
.permission-guard {
  width: 100%;
  height: 100%;
}

.permission-denied {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}
</style>