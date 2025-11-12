<template>
  <el-card v-if="selectedCount > 0" class="batch-operations">
    <div class="batch-header">
      <div class="batch-info">
        <el-icon :size="20" color="#409eff"><Select /></el-icon>
        <span>已选择 <strong>{{ selectedCount }}</strong> 项</span>
      </div>
      <el-button text @click="$emit('clear-selection')">
        <el-icon><Close /></el-icon>
        清空选择
      </el-button>
    </div>

    <el-divider style="margin: 12px 0" />

    <div class="batch-actions">
      <!-- 媒体批量操作 -->
      <template v-if="type === 'media'">
        <el-button type="primary" @click="handleBatchFeature(true)">
          <el-icon><Star /></el-icon>
          批量推荐
        </el-button>
        <el-button @click="handleBatchFeature(false)">
          <el-icon><StarFilled /></el-icon>
          取消推荐
        </el-button>
        <el-button type="success" @click="handleBatchUpdateState('public')">
          <el-icon><Check /></el-icon>
          设为公开
        </el-button>
        <el-button type="warning" @click="handleBatchUpdateState('private')">
          <el-icon><Lock /></el-icon>
          设为私密
        </el-button>
        <el-button type="danger" @click="handleBatchDelete">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
      </template>

      <!-- 用户批量操作 -->
      <template v-else-if="type === 'users'">
        <el-button type="warning" @click="handleBatchBlock">
          <el-icon><Lock /></el-icon>
          批量封禁
        </el-button>
        <el-button type="success" @click="handleBatchUnblock">
          <el-icon><Unlock /></el-icon>
          批量解封
        </el-button>
        <el-button type="danger" @click="handleBatchDelete">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
      </template>

      <!-- 评论批量操作 -->
      <template v-else-if="type === 'comments'">
        <el-button type="success" @click="handleBatchApprove">
          <el-icon><Check /></el-icon>
          批量通过
        </el-button>
        <el-button type="warning" @click="handleBatchReject">
          <el-icon><Close /></el-icon>
          批量拒绝
        </el-button>
        <el-button type="danger" @click="handleBatchDelete">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
      </template>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { 
  batchFeatureMedia, 
  batchUpdateMediaState, 
  batchDeleteMedia,
  deleteComments,
  batchBlockUsers,
  batchUnblockUsers,
  batchDeleteUsers
} from '@/api/admin'

interface Props {
  selectedIds: string[]
  type: 'media' | 'users' | 'comments'
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'batch-success': []
  'clear-selection': []
}>()

const selectedCount = computed(() => props.selectedIds.length)

// 批量推荐/取消推荐
const handleBatchFeature = async (featured: boolean) => {
  try {
    await ElMessageBox.confirm(
      `确定要${featured ? '推荐' : '取消推荐'}选中的 ${selectedCount.value} 个媒体吗？`,
      '提示',
      { type: 'warning' }
    )

    const result = await batchFeatureMedia(props.selectedIds, featured)
    ElMessage.success(`操作成功：处理了 ${result.processed} 个项目`)
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

// 批量更新状态
const handleBatchUpdateState = async (state: string) => {
  try {
    const stateText = state === 'public' ? '公开' : '私密'
    await ElMessageBox.confirm(
      `确定要将选中的 ${selectedCount.value} 个媒体设为${stateText}吗？`,
      '提示',
      { type: 'warning' }
    )

    const result = await batchUpdateMediaState(props.selectedIds, state)
    ElMessage.success(`操作成功：处理了 ${result.processed} 个项目`)
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

// 批量删除
const handleBatchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedCount.value} 个项目吗？此操作不可撤销！`,
      '警告',
      {
        type: 'error',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消'
      }
    )

    if (props.type === 'media') {
      await batchDeleteMedia(props.selectedIds)
      ElMessage.success(`删除成功`)
    } else if (props.type === 'comments') {
      await deleteComments(props.selectedIds)
      ElMessage.success(`删除成功`)
    } else if (props.type === 'users') {
      await batchDeleteUsers(props.selectedIds)
      ElMessage.success(`删除成功`)
    }
    
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

// 批量封禁
const handleBatchBlock = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要封禁选中的 ${selectedCount.value} 个用户吗？`,
      '警告',
      { type: 'warning' }
    )
    
    await batchBlockUsers(props.selectedIds)
    ElMessage.success('批量封禁成功')
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

// 批量解封
const handleBatchUnblock = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要解封选中的 ${selectedCount.value} 个用户吗？`,
      '提示',
      { type: 'info' }
    )
    
    await batchUnblockUsers(props.selectedIds)
    ElMessage.success('批量解封成功')
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

// 批量通过
const handleBatchApprove = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要通过选中的 ${selectedCount.value} 个评论吗？`,
      '提示',
      { type: 'success' }
    )
    
    ElMessage.info('批量通过功能待实现')
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

// 批量拒绝
const handleBatchReject = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要拒绝选中的 ${selectedCount.value} 个评论吗？`,
      '提示',
      { type: 'warning' }
    )
    
    ElMessage.info('批量拒绝功能待实现')
    emit('batch-success')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
    }
  }
}
</script>

<style scoped lang="scss">
.batch-operations {
  margin-bottom: 20px;
  border: 2px dashed #409eff;
  
  :deep(.el-card__body) {
    padding: 16px;
  }
}

.batch-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;

  strong {
    color: #409eff;
    font-size: 16px;
  }
}

.batch-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

[data-theme='dark'] {
  .batch-operations {
    border-color: #409eff;
  }
}
</style>

