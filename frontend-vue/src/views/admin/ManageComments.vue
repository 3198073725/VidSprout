<template>
  <div class="manage-comments">
    <div class="header">
      <h1>评论管理</h1>
      <p class="description">管理所有用户评论，支持批量删除和审核</p>
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
      :selected-ids="selectedComments"
      operation-type="comments"
      @batch-operation="handleBatchOperation"
      @completed="handleBatchCompleted"
    />

    <!-- 筛选工具栏 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="排序字段">
          <el-select v-model="filters.sort_by" placeholder="选择排序字段" @change="loadComments">
            <el-option label="发布时间" value="publish_date" />
            <el-option label="点赞数" value="likes" />
            <el-option label="举报次数" value="reported_times" />
          </el-select>
        </el-form-item>

        <el-form-item label="排序方式">
          <el-select v-model="filters.ordering" placeholder="选择排序方式" @change="loadComments">
            <el-option label="升序" value="asc" />
            <el-option label="降序" value="desc" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="loadComments">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
          <el-button 
            type="danger" 
            :disabled="selectedComments.length === 0"
            @click="batchDeleteComments"
          >
            <el-icon><Delete /></el-icon>
            批量删除 ({{ selectedComments.length }})
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 评论列表表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="commentList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column label="序号" type="index" width="60" />

        <el-table-column label="评论内容" min-width="300">
          <template #default="{ row }">
            <div class="comment-content">
              <p class="text">{{ row.text }}</p>
              <div v-if="row.parent" class="reply-info">
                <el-icon><MessageBox /></el-icon>
                <span>回复评论ID: {{ row.parent }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="评论者" width="150">
          <template #default="{ row }">
            <div class="user-info" v-if="row.user">
              <el-avatar :size="32" :src="row.user.avatar_url" />
              <span class="username">{{ row.user.username }}</span>
            </div>
            <div v-else class="user-info">
              <el-avatar :size="32" :src="row.author_thumbnail_url || undefined" />
              <span class="username">{{ row.author_name }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="所属媒体" width="200">
          <template #default="{ row }">
            <div class="media-info" v-if="row.media">
              <img :src="row.media.thumbnail_url" class="thumbnail" />
              <span class="title">{{ row.media.title }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="点赞" width="80" align="center">
          <template #default="{ row }">
            <span>{{ row.likes || 0 }}</span>
          </template>
        </el-table-column>

        <el-table-column label="举报次数" width="100" align="center">
          <template #default="{ row }">
            <el-tag 
              :type="(row.reported_times || 0) > 0 ? 'danger' : 'info'" 
              size="small"
            >
              <el-icon><Warning /></el-icon>
              {{ row.reported_times || 0 }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="发布时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.add_date) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              link
              @click="viewComment(row)"
            >
              <el-icon><View /></el-icon>
              查看
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              link
              @click="deleteComment(row)"
            >
              <el-icon><Delete /></el-icon>
              删除
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
          @size-change="loadComments"
          @current-change="loadComments"
        />
      </div>
    </el-card>

    <!-- 评论详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="评论详情"
      width="600px"
    >
      <div v-if="currentComment" class="comment-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="评论内容">
            {{ currentComment.text }}
          </el-descriptions-item>
          
          <el-descriptions-item label="评论者">
            <div class="user-info" v-if="currentComment.user">
              <el-avatar :size="32" :src="currentComment.user.avatar_url" />
              <span>{{ currentComment.user.username }}</span>
            </div>
            <div v-else class="user-info">
              <el-avatar :size="32" :src="currentComment.author_thumbnail_url || undefined" />
              <span>{{ currentComment.author_name }}</span>
            </div>
          </el-descriptions-item>

          <el-descriptions-item label="所属媒体" v-if="currentComment.media">
            <a :href="`/media/${currentComment.media.friendly_token}`" target="_blank">
              {{ currentComment.media.title }}
            </a>
          </el-descriptions-item>

          <el-descriptions-item label="父评论" v-if="currentComment.parent">
            父评论ID: {{ currentComment.parent }}
          </el-descriptions-item>

          <el-descriptions-item label="点赞数">
            {{ currentComment.likes || 0 }}
          </el-descriptions-item>

          <el-descriptions-item label="举报次数">
            <el-tag :type="(currentComment.reported_times || 0) > 0 ? 'danger' : 'info'">
              {{ currentComment.reported_times || 0 }}
            </el-tag>
          </el-descriptions-item>

          <el-descriptions-item label="发布时间">
            {{ formatDate(currentComment.add_date) }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="danger" @click="deleteComment(currentComment)">
          <el-icon><Delete /></el-icon>
          删除评论
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Refresh,
  Delete,
  View,
  Warning,
  MessageBox,
  TrendCharts,
  Download
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import * as AdminAPI from '@/api/admin'
import type { ManageCommentItem } from '@/api/types'
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
const commentList = ref<ManageCommentItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedComments = ref<string[]>([])
const detailDialogVisible = ref(false)
const currentComment = ref<ManageCommentItem | null>(null)
const statsData = ref<any>(null)
const showStats = ref(false)

// 筛选条件
const filters = ref({
  sort_by: 'publish_date',
  ordering: 'desc' as 'asc' | 'desc'
})

// 加载评论列表
async function loadComments() {
  if (!isAdmin.value) {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
    return
  }

  loading.value = true
  try {
    const params: AdminAPI.ManageCommentsParams = {
      page: currentPage.value,
      sort_by: filters.value.sort_by,
      ordering: filters.value.ordering
    }

    const response = await AdminAPI.getManageComments(params)
    commentList.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载评论列表失败:', error)
    ElMessage.error('加载失败，请稍后再试')
  } finally {
    loading.value = false
  }
}

// 处理选择变化
function handleSelectionChange(selection: ManageCommentItem[]) {
  selectedComments.value = selection.map(item => item.uid)
}

// 查看评论详情
function viewComment(comment: ManageCommentItem) {
  currentComment.value = comment
  detailDialogVisible.value = true
}

// 删除单个评论
async function deleteComment(comment: ManageCommentItem | null) {
  if (!comment) return

  try {
    await ElMessageBox.confirm(
      `确定要删除这条评论吗？此操作不可撤销！`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await AdminAPI.deleteComments([comment.uid])
    ElMessage.success('删除成功')
    detailDialogVisible.value = false
    loadComments()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('删除评论失败:', err)
      ElMessage.error('删除失败')
    }
  }
}

// 批量删除评论
async function batchDeleteComments() {
  if (selectedComments.value.length === 0) {
    ElMessage.warning('请先选择要删除的评论')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedComments.value.length} 条评论吗？此操作不可撤销！`,
      '批量删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const commentIds = selectedComments.value
    await AdminAPI.deleteComments(commentIds)
    ElMessage.success(`成功删除 ${commentIds.length} 条评论`)
    selectedComments.value = []
    loadComments()
  } catch (err) {
    if (err !== 'cancel') {
      console.error('批量删除评论失败:', err)
      ElMessage.error('批量删除失败')
    }
  }
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
      ElMessage.success(`批量操作成功，处理了 ${result.processed} 条评论`)
      loadComments() // 重新加载数据
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
      type: 'comments',
      format: 'excel'
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

// 批量操作完成处理
function handleBatchCompleted(results: any) {
  // 清空选择
  selectedComments.value = []
  ElMessage.success(`批量操作完成：成功 ${results.success} 个，失败 ${results.failed} 个`)
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

// 初始化
onMounted(() => {
  if (isAdmin.value) {
    loadComments()
    loadStats()
  } else {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
  }
})
</script>

<style scoped lang="scss">
.manage-comments {
  padding: 24px;
  max-width: 1400px;
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
    .comment-content {
      .text {
        margin: 0 0 8px 0;
        line-height: 1.6;
        word-break: break-word;
      }

      .reply-info {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background-color: #f3f4f6;
        border-radius: 4px;
        font-size: 12px;
        color: #6b7280;

        .el-icon {
          font-size: 14px;
        }
      }
    }

    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;

      .username {
        font-size: 14px;
        color: #374151;
      }
    }

    .media-info {
      display: flex;
      align-items: center;
      gap: 8px;

      .thumbnail {
        width: 60px;
        height: 40px;
        object-fit: cover;
        border-radius: 4px;
      }

      .title {
        flex: 1;
        font-size: 13px;
        color: #374151;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
      }
    }

    .pagination-container {
      display: flex;
      justify-content: flex-end;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #e5e7eb;
    }
  }

  .comment-detail {
    .user-info {
      display: flex;
      align-items: center;
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
  .manage-comments {
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
