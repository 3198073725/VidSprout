<template>
  <div class="batch-operations">
    <el-card class="batch-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>批量操作</span>
          <el-tag type="info">已选择 {{ selectedCount }} 项</el-tag>
        </div>
      </template>
      
      <div class="batch-content">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-button-group class="batch-group">
              <el-button 
                type="danger" 
                :disabled="selectedCount === 0"
                @click="handleBatchDelete"
                :loading="loading.delete"
              >
                <el-icon><Delete /></el-icon>
                批量删除
              </el-button>
              <el-button 
                type="warning" 
                :disabled="selectedCount === 0"
                @click="handleBatchBlock"
                :loading="loading.block"
              >
                <el-icon><Lock /></el-icon>
                批量封禁
              </el-button>
            </el-button-group>
          </el-col>
          
          <el-col :span="8">
            <el-button-group class="batch-group">
              <el-button 
                type="success" 
                :disabled="selectedCount === 0"
                @click="handleBatchApprove"
                :loading="loading.approve"
              >
                <el-icon><Check /></el-icon>
                批量审核
              </el-button>
              <el-button 
                type="info" 
                :disabled="selectedCount === 0"
                @click="handleBatchReject"
                :loading="loading.reject"
              >
                <el-icon><Close /></el-icon>
                批量拒绝
              </el-button>
            </el-button-group>
          </el-col>
          
          <el-col :span="8">
            <el-button-group class="batch-group">
              <el-button 
                type="primary" 
                :disabled="selectedCount === 0"
                @click="handleBatchFeature"
                :loading="loading.feature"
              >
                <el-icon><Star /></el-icon>
                批量推荐
              </el-button>
              <el-button 
                type="primary" 
                :disabled="selectedCount === 0"
                @click="handleBatchUnfeature"
                :loading="loading.unfeature"
              >
                <el-icon><StarFilled /></el-icon>
                取消推荐
              </el-button>
            </el-button-group>
          </el-col>
        </el-row>
        
        <el-row :gutter="16" style="margin-top: 16px;">
          <el-col :span="12">
            <el-select 
              v-model="batchOperation.category" 
              placeholder="批量修改分类"
              :disabled="selectedCount === 0"
              style="width: 100%"
            >
              <el-option label="科技" value="tech" />
              <el-option label="娱乐" value="entertainment" />
              <el-option label="教育" value="education" />
              <el-option label="新闻" value="news" />
              <el-option label="体育" value="sports" />
            </el-select>
          </el-col>
          
          <el-col :span="12">
            <el-button 
              type="primary" 
              :disabled="selectedCount === 0 || !batchOperation.category"
              @click="handleBatchCategory"
              :loading="loading.category"
            >
              <el-icon><Edit /></el-icon>
              应用分类
            </el-button>
          </el-col>
        </el-row>
        
        <el-row :gutter="16" style="margin-top: 16px;">
          <el-col :span="12">
            <el-select 
              v-model="batchOperation.state" 
              placeholder="批量修改状态"
              :disabled="selectedCount === 0"
              style="width: 100%"
            >
              <el-option label="公开" value="public" />
              <el-option label="私密" value="private" />
              <el-option label="仅限链接" value="unlisted" />
            </el-select>
          </el-col>
          
          <el-col :span="12">
            <el-button 
              type="primary" 
              :disabled="selectedCount === 0 || !batchOperation.state"
              @click="handleBatchState"
              :loading="loading.state"
            >
              <el-icon><Edit /></el-icon>
              应用状态
            </el-button>
          </el-col>
        </el-row>
      </div>
    </el-card>
    
    <!-- 批量操作确认对话框 -->
    <el-dialog
      v-model="confirmDialog.visible"
      :title="confirmDialog.title"
      width="400px"
      :before-close="handleCloseConfirm"
    >
      <div class="confirm-content">
        <el-alert
          :title="confirmDialog.warning"
          type="warning"
          :description="confirmDialog.description"
          show-icon
          :closable="false"
        />
        <div class="confirm-stats">
          <el-statistic :title="'受影响项目'" :value="selectedCount" />
        </div>
      </div>
      
      <template #footer>
        <el-button @click="handleCloseConfirm">取消</el-button>
        <el-button 
          :type="confirmDialog.confirmType" 
          @click="handleConfirmOperation"
          :loading="confirmDialog.loading"
        >
          {{ confirmDialog.confirmText }}
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 批量操作进度对话框 -->
    <el-dialog
      v-model="progressDialog.visible"
      title="批量操作进度"
      width="500px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :show-close="false"
    >
      <div class="progress-content">
        <el-progress 
          :percentage="progressDialog.percentage" 
          :status="progressDialog.status"
          :stroke-width="20"
          striped
          striped-flow
        />
        
        <div class="progress-stats">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="stat-item">
                <div class="stat-label">已处理</div>
                <div class="stat-value">{{ progressDialog.processed }}</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-item">
                <div class="stat-label">成功</div>
                <div class="stat-value text-success">{{ progressDialog.success }}</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-item">
                <div class="stat-label">失败</div>
                <div class="stat-value text-danger">{{ progressDialog.failed }}</div>
              </div>
            </el-col>
          </el-row>
        </div>
        
        <div class="progress-logs" v-if="progressDialog.logs.length > 0">
          <el-scrollbar max-height="200px">
            <div 
              v-for="(log, index) in progressDialog.logs" 
              :key="index"
              class="log-item"
              :class="log.type"
            >
              <el-icon>
                <CircleCheck v-if="log.type === 'success'" />
                <CircleClose v-else-if="log.type === 'error'" />
                <InfoFilled v-else />
              </el-icon>
              <span>{{ log.message }}</span>
            </div>
          </el-scrollbar>
        </div>
      </div>
      
      <template #footer>
        <el-button 
          @click="handleCloseProgress" 
          :disabled="progressDialog.status === 'exception'"
        >
          关闭
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Delete, 
  Lock, 
  Check, 
  Close, 
  Star, 
  StarFilled, 
  Edit,
  CircleCheck,
  CircleClose,
  InfoFilled
} from '@element-plus/icons-vue'

interface Props {
  selectedIds: string[]
  operationType: 'media' | 'users' | 'comments'
}

interface BatchOperationState {
  category: string
  state: string
}

interface LoadingState {
  delete: boolean
  block: boolean
  approve: boolean
  reject: boolean
  feature: boolean
  unfeature: boolean
  category: boolean
  state: boolean
}

interface ConfirmDialogState {
  visible: boolean
  title: string
  warning: string
  description: string
  confirmText: string
  confirmType: string
  operation: string
  loading: boolean
}

interface ProgressDialogState {
  visible: boolean
  percentage: number
  status: string
  processed: number
  success: number
  failed: number
  total: number
  logs: Array<{ type: string; message: string }>
}

const props = defineProps<Props>()
const emit = defineEmits<{
  batchOperation: [operation: string, data: any]
  completed: [results: any]
}>()

const selectedCount = computed(() => props.selectedIds.length)

const batchOperation = reactive<BatchOperationState>({
  category: '',
  state: ''
})

const loading = reactive<LoadingState>({
  delete: false,
  block: false,
  approve: false,
  reject: false,
  feature: false,
  unfeature: false,
  category: false,
  state: false
})

const confirmDialog = reactive<ConfirmDialogState>({
  visible: false,
  title: '',
  warning: '',
  description: '',
  confirmText: '确认',
  confirmType: 'primary',
  operation: '',
  loading: false
})

const progressDialog = reactive<ProgressDialogState>({
  visible: false,
  percentage: 0,
  status: '',
  processed: 0,
  success: 0,
  failed: 0,
  total: 0,
  logs: []
})

// 批量删除
function handleBatchDelete() {
  showConfirmDialog(
    '批量删除确认',
    '此操作将永久删除选中的项目',
    '删除后无法恢复，请谨慎操作',
    '删除',
    'danger',
    'delete'
  )
}

// 批量封禁
function handleBatchBlock() {
  showConfirmDialog(
    '批量封禁确认',
    '此操作将封禁选中的用户',
    '被封禁的用户将无法登录系统',
    '封禁',
    'warning',
    'block'
  )
}

// 批量审核
function handleBatchApprove() {
  showConfirmDialog(
    '批量审核确认',
    '此操作将通过选中的项目审核',
    '审核通过的项目将对用户可见',
    '通过',
    'success',
    'approve'
  )
}

// 批量拒绝
function handleBatchReject() {
  showConfirmDialog(
    '批量拒绝确认',
    '此操作将拒绝选中的项目审核',
    '被拒绝的项目需要重新提交审核',
    '拒绝',
    'info',
    'reject'
  )
}

// 批量推荐
function handleBatchFeature() {
  showConfirmDialog(
    '批量推荐确认',
    '此操作将推荐选中的媒体',
    '推荐的媒体将在首页展示',
    '推荐',
    'primary',
    'feature'
  )
}

// 取消推荐
function handleBatchUnfeature() {
  showConfirmDialog(
    '取消推荐确认',
    '此操作将取消选中的媒体推荐',
    '取消推荐后媒体将不再在首页展示',
    '取消推荐',
    'primary',
    'unfeature'
  )
}

// 批量修改分类
function handleBatchCategory() {
  if (!batchOperation.category) return
  
  showConfirmDialog(
    '批量修改分类确认',
    '此操作将修改选中的项目分类',
    `分类将修改为: ${batchOperation.category}`,
    '修改',
    'primary',
    'category'
  )
}

// 批量修改状态
function handleBatchState() {
  if (!batchOperation.state) return
  
  showConfirmDialog(
    '批量修改状态确认',
    '此操作将修改选中的项目状态',
    `状态将修改为: ${getStateText(batchOperation.state)}`,
    '修改',
    'primary',
    'state'
  )
}

// 显示确认对话框
function showConfirmDialog(
  title: string,
  warning: string,
  description: string,
  confirmText: string,
  confirmType: string,
  operation: string
) {
  confirmDialog.title = title
  confirmDialog.warning = warning
  confirmDialog.description = description
  confirmDialog.confirmText = confirmText
  confirmDialog.confirmType = confirmType
  confirmDialog.operation = operation
  confirmDialog.visible = true
}

// 关闭确认对话框
function handleCloseConfirm() {
  confirmDialog.visible = false
  confirmDialog.loading = false
}

// 确认操作
async function handleConfirmOperation() {
  confirmDialog.loading = true
  
  try {
    const operation = confirmDialog.operation
    const data: any = {
      ids: props.selectedIds,
      operation: operation
    }
    
    // 添加特定操作的参数
    if (operation === 'category') {
      data.category = batchOperation.category
    } else if (operation === 'state') {
      data.state = batchOperation.state
    }
    
    // 显示进度对话框
    showProgressDialog()
    
    // 执行批量操作
    await executeBatchOperation(operation, data)
    
    confirmDialog.visible = false
    ElMessage.success('批量操作完成')
    
    // 重置批量操作参数
    batchOperation.category = ''
    batchOperation.state = ''
    
  } catch (error) {
    ElMessage.error('批量操作失败')
  } finally {
    confirmDialog.loading = false
  }
}

// 显示进度对话框
function showProgressDialog() {
  progressDialog.visible = true
  progressDialog.percentage = 0
  progressDialog.status = ''
  progressDialog.processed = 0
  progressDialog.success = 0
  progressDialog.failed = 0
  progressDialog.total = props.selectedIds.length
  progressDialog.logs = []
}

// 关闭进度对话框
function handleCloseProgress() {
  progressDialog.visible = false
  emit('completed', {
    processed: progressDialog.processed,
    success: progressDialog.success,
    failed: progressDialog.failed
  })
}

// 执行批量操作
async function executeBatchOperation(operation: string, data: any) {
  // 模拟批量操作进度
  const total = props.selectedIds.length
  const batchSize = 5 // 每批处理5个
  const batches = Math.ceil(total / batchSize)
  
  for (let i = 0; i < batches; i++) {
    const start = i * batchSize
    const end = Math.min(start + batchSize, total)
    const batchIds = props.selectedIds.slice(start, end)
    
    try {
      // 发送批量操作请求
      await emit('batchOperation', operation, {
        ...data,
        ids: batchIds
      })
      
      // 更新进度
      progressDialog.processed = end
      progressDialog.success += batchIds.length
      progressDialog.percentage = Math.round((end / total) * 100)
      
      // 添加成功日志
      progressDialog.logs.push({
        type: 'success',
        message: `第 ${i + 1} 批处理完成 (${batchIds.length} 个项目)`
      })
      
    } catch (error) {
      // 更新失败统计
      progressDialog.failed += batchIds.length
      progressDialog.processed = end
      progressDialog.percentage = Math.round((end / total) * 100)
      
      // 添加错误日志
      progressDialog.logs.push({
        type: 'error',
        message: `第 ${i + 1} 批处理失败: ${error}`
      })
    }
    
    // 小延迟以显示进度
    await new Promise(resolve => setTimeout(resolve, 500))
  }
  
  // 设置最终状态
  if (progressDialog.failed > 0) {
    progressDialog.status = 'exception'
  } else {
    progressDialog.status = 'success'
  }
}

// 获取状态文本
function getStateText(state: string): string {
  const stateMap: Record<string, string> = {
    'public': '公开',
    'private': '私密',
    'unlisted': '仅限链接'
  }
  return stateMap[state] || state
}
</script>

<style scoped>
.batch-operations {
  margin-bottom: 20px;
}

.batch-card {
  border: 1px solid #e4e7ed;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-content {
  padding: 20px 0;
}

.batch-group {
  width: 100%;
}

.batch-group .el-button {
  flex: 1;
}

.confirm-content {
  padding: 20px 0;
}

.confirm-stats {
  margin-top: 20px;
  text-align: center;
}

.progress-content {
  padding: 20px 0;
}

.progress-stats {
  margin-top: 20px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stat-value.text-success {
  color: #67c23a;
}

.stat-value.text-danger {
  color: #f56c6c;
}

.progress-logs {
  margin-top: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 10px;
}

.log-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 0;
  font-size: 12px;
}

.log-item.success {
  color: #67c23a;
}

.log-item.error {
  color: #f56c6c;
}

.log-item.info {
  color: #909399;
}
</style>