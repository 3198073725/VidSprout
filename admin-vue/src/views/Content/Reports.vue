<template>
  <div class="reports-container">
    <el-card>
      <!-- 搜索和筛选 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="searchQuery"
            placeholder="搜索举报内容..."
            clearable
            style="width: 300px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <el-select v-model="filters.status" placeholder="状态" clearable style="width: 140px" @change="handleSearch">
            <el-option label="待处理" value="pending" />
            <el-option label="已处理" value="resolved" />
            <el-option label="已忽略" value="ignored" />
          </el-select>

          <el-select v-model="filters.type" placeholder="类型" clearable style="width: 140px" @change="handleSearch">
            <el-option label="媒体举报" value="media" />
            <el-option label="评论举报" value="comment" />
            <el-option label="用户举报" value="user" />
          </el-select>
        </div>

        <div class="toolbar-right">
          <el-button @click="handleRefresh">
            <el-icon><RefreshRight /></el-icon>
            刷新
          </el-button>
        </div>
      </div>

      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="reportList"
        style="width: 100%; margin-top: 20px"
      >
        <el-table-column type="expand">
          <template #default="{ row }">
            <div class="report-detail">
              <p><strong>举报原因：</strong></p>
              <p>{{ row.reason }}</p>
              <el-divider />
              <p><strong>详细描述：</strong></p>
              <p>{{ row.description || '无' }}</p>
              <el-divider />
              <p><strong>被举报对象：</strong>{{ row.target_title }}</p>
              <p><strong>举报人：</strong>{{ row.reporter_name }}</p>
              <p><strong>举报时间：</strong>{{ formatDate(row.created_at) }}</p>
              <p v-if="row.handled_at"><strong>处理时间：</strong>{{ formatDate(row.handled_at) }}</p>
              <p v-if="row.handler_name"><strong>处理人：</strong>{{ row.handler_name }}</p>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTypeColor(row.type)" size="small">
              {{ getTypeName(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_title" label="被举报对象" min-width="200" show-overflow-tooltip />
        <el-table-column prop="reason" label="举报原因" min-width="200" show-overflow-tooltip />
        <el-table-column prop="reporter_name" label="举报人" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusColor(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="举报时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button 
                v-if="row.status === 'pending'" 
                type="success" 
                size="small"
                @click="handleReport(row, 'resolved')"
              >
                <el-icon><Check /></el-icon>
                已处理
              </el-button>
              <el-button 
                v-if="row.status === 'pending'" 
                type="warning" 
                size="small"
                @click="handleReport(row, 'ignored')"
              >
                <el-icon><Close /></el-icon>
                忽略
              </el-button>
              <el-button 
                v-if="row.status === 'pending' && row.type === 'media'" 
                type="danger" 
                size="small"
                @click="handleDeleteMedia(row)"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
              <el-button 
                type="primary" 
                size="small"
                @click="viewTarget(row)"
              >
                <el-icon><View /></el-icon>
                查看
              </el-button>
            </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'
import { getManageReports, handleReport as handleReportAction, type ReportItem } from '@/api/admin'

const router = useRouter()

const loading = ref(false)
const reportList = ref<ReportItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')

const filters = ref({
  status: undefined as undefined | string,
  type: undefined as undefined | string
})

// 加载举报列表（连接后端API）
const loadReports = async () => {
  loading.value = true
  try {
    console.log('📥 加载举报列表...')
    const response = await getManageReports({
      page: currentPage.value,
      page_size: pageSize.value,
      status: filters.value.status as any,
      search: searchQuery.value
    })
    
    reportList.value = response.results
    total.value = response.count
    
    console.log('✅ 加载举报列表成功:', {
      total: total.value,
      currentPage: currentPage.value,
      count: reportList.value.length
    })
  } catch (error) {
    console.error('❌ 加载举报列表失败:', error)
    ElMessage.error('加载举报列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadReports()
}

const handleRefresh = () => {
  loadReports()
}

const getTypeColor = (type: string) => {
  const map: Record<string, any> = {
    media: '',
    comment: 'warning',
    user: 'danger'
  }
  return map[type] || 'info'
}

const getTypeName = (type: string) => {
  const map: Record<string, string> = {
    media: '媒体举报',
    comment: '评论举报',
    user: '用户举报'
  }
  return map[type] || type
}

const getStatusColor = (status: string) => {
  const map: Record<string, any> = {
    pending: 'warning',
    resolved: 'success',
    ignored: 'info'
  }
  return map[status] || 'info'
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    pending: '待处理',
    resolved: '已处理',
    ignored: '已忽略'
  }
  return map[status] || status
}

const formatDate = (date: string) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const handleReport = async (report: ReportItem, action: 'resolved' | 'ignored') => {
  const actionText = action === 'resolved' ? '标记为已处理' : '忽略'
  const apiAction = action === 'resolved' ? 'resolve' : 'ignore'
  
  try {
    await ElMessageBox.confirm(`确定要${actionText}这条举报吗？`, '提示', {
      type: action === 'resolved' ? 'success' : 'warning'
    })
    
    console.log(`📤 ${actionText}举报:`, report.id)
    await handleReportAction(report.id, apiAction)
    
    ElMessage.success(`${actionText}成功`)
    console.log(`✅ ${actionText}成功`)
    
    // 重新加载列表
    await loadReports()
  } catch (error: any) {
    // 用户取消操作或API错误
    if (error !== 'cancel') {
      console.error(`❌ ${actionText}失败:`, error)
      ElMessage.error(`${actionText}失败`)
    }
  }
}

const viewTarget = (report: ReportItem) => {
  console.log('📍 查看被举报对象:', report)
  
  if (report.type === 'media' && report.media?.friendly_token) {
    // 跳转到媒体详情页
    const mediaToken = report.media.friendly_token
    console.log('  - 跳转到媒体详情:', mediaToken)
    router.push(`/media/detail/${mediaToken}`)
  } else if (report.type === 'comment') {
    router.push('/content/comments')
  } else if (report.type === 'user') {
    router.push(`/users/detail/${report.target_id}`)
  } else {
    ElMessage.warning('无法定位被举报对象')
  }
}

// 添加删除被举报媒体的功能
const handleDeleteMedia = async (report: ReportItem) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个被举报的媒体吗？此操作无法撤销！',
      '警告',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'error'
      }
    )
    
    console.log('📤 删除被举报的媒体:', report.id)
    await handleReportAction(report.id, 'delete_media', '媒体包含违规内容')
    
    ElMessage.success('已删除被举报的媒体')
    console.log('✅ 删除成功')
    
    // 重新加载列表
    await loadReports()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('❌ 删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadReports()
})
</script>

<style scoped lang="scss">
.reports-container {
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

.report-detail {
  padding: 16px;
  background: var(--el-fill-color-lighter);
  border-radius: 4px;
  margin: 12px;

  p {
    margin: 8px 0;
    line-height: 1.6;
  }

  strong {
    color: var(--el-text-color-primary);
  }
}

/* 操作按钮样式 */
.action-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
  
  .el-button {
    margin: 0;
  }
}
</style>
