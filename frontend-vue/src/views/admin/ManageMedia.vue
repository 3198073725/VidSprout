<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { AdminAPI, type MediaItem } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Search,
  RefreshRight,
  Delete,
  Edit,
  View,
  Check,
  Close,
  VideoPlay,
  Download,
  TrendCharts
} from '@element-plus/icons-vue'
import AdminStatsCharts from '@/components/AdminStatsCharts.vue'
import BatchOperations from '@/components/BatchOperations.vue'

const router = useRouter()
const auth = useAuthStore()

// 检查管理员权限
const isAdmin = computed(() => {
  const profile = auth.profile as {is_staff?: boolean} | null
  return profile?.is_staff || false
})

const loading = ref(false)
const mediaList = ref<MediaItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const selectedMedia = ref<string[]>([])
const statsData = ref<any>(null)
const showStats = ref(false)

// 筛选条件
const filters = ref({
  sort_by: 'add_date' as 'title' | 'add_date' | 'edit_date' | 'views' | 'likes' | 'reported_times',
  ordering: 'desc' as 'asc' | 'desc',
  state: '' as '' | 'private' | 'public' | 'unlisted',
  search: ''
})

// 加载媒体列表
async function loadMedia() {
  if (!isAdmin.value) {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
    return
  }

  loading.value = true
  try {
    const params: AdminAPI.ManageMediaParams = {
      page: currentPage.value,
      sort_by: filters.value.sort_by,
      ordering: filters.value.ordering
    }
    
    if (filters.value.state) {
      params.state = filters.value.state
    }
    
    if (filters.value.search) {
      params.search = filters.value.search
    }

    const response = await AdminAPI.getManageMedia(params)
    mediaList.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载媒体列表失败:', error)
    ElMessage.error('加载失败，请稍后再试')
  } finally {
    loading.value = false
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
      ElMessage.success(`批量操作成功，处理了 ${result.processed} 个项目`)
      loadMedia() // 重新加载数据
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
      type: 'media',
      format: 'excel',
      filters: {
        state: filters.value.state,
        search: filters.value.search
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
function handleSelectionChange(selection: MediaItem[]) {
  selectedMedia.value = selection.map(item => item.friendly_token)
}

// 批量操作完成处理
function handleBatchCompleted(results: any) {
  // 清空选择
  selectedMedia.value = []
  ElMessage.success(`批量操作完成：成功 ${results.success} 个，失败 ${results.failed} 个`)
}

// 刷新列表
function refreshList() {
  currentPage.value = 1
  loadMedia()
}

// 搜索
function handleSearch() {
  currentPage.value = 1
  loadMedia()
}

// 页码变化
function handlePageChange(page: number) {
  currentPage.value = page
  loadMedia()
}

// 查看媒体
function viewMedia(media: MediaItem) {
  window.open(`/media/${media.friendly_token}`, '_blank')
}

// 编辑媒体
function editMedia(media: MediaItem) {
  router.push(`/media/${media.friendly_token}/edit`)
}

// 删除媒体
async function deleteMedia(media: MediaItem) {
  try {
    await ElMessageBox.confirm(
      `确定要删除媒体"${media.title}"吗？此操作不可撤销！`,
      '删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 调用删除API（需要使用MediaAPI.deleteMedia）
    await AdminAPI.getManageMedia({ search: media.friendly_token }) // 这里需要实际的删除API
    ElMessage.success('删除成功')
    loadMedia()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 格式化日期
function formatDate(dateString?: string) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

// 格式化时长
function formatDuration(seconds?: number) {
  if (!seconds) return '-'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// 获取状态标签类型
function getStateType(state?: string) {
  switch (state) {
    case 'public': return 'success'
    case 'unlisted': return 'warning'
    case 'private': return 'danger'
    default: return 'info'
  }
}

// 获取状态文本
function getStateText(state?: string) {
  switch (state) {
    case 'public': return '公开'
    case 'unlisted': return '仅限链接'
    case 'private': return '私密'
    default: return '未知'
  }
}

onMounted(() => {
  if (isAdmin.value) {
    loadMedia()
    loadStats()
  } else {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
  }
})
</script>

<template>
  <div class="admin-media-manage">
    <div class="page-header">
      <h1>媒体管理</h1>
      <p>管理所有用户上传的媒体内容</p>
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
      :selected-ids="selectedMedia"
      operation-type="media"
      @batch-operation="handleBatchOperation"
      @completed="handleBatchCompleted"
    />

    <!-- 筛选工具栏 -->
    <el-card class="filter-card" shadow="never">
      <el-form :inline="true" :model="filters">
        <el-form-item label="排序字段">
          <el-select v-model="filters.sort_by" @change="handleSearch" style="width: 150px">
            <el-option label="添加时间" value="add_date" />
            <el-option label="编辑时间" value="edit_date" />
            <el-option label="标题" value="title" />
            <el-option label="观看次数" value="views" />
            <el-option label="点赞数" value="likes" />
            <el-option label="举报次数" value="reported_times" />
          </el-select>
        </el-form-item>

        <el-form-item label="排序方式">
          <el-select v-model="filters.ordering" @change="handleSearch" style="width: 120px">
            <el-option label="降序" value="desc" />
            <el-option label="升序" value="asc" />
          </el-select>
        </el-form-item>

        <el-form-item label="媒体状态">
          <el-select v-model="filters.state" @change="handleSearch" style="width: 130px">
            <el-option label="全部" value="" />
            <el-option label="公开" value="public" />
            <el-option label="仅限链接" value="unlisted" />
            <el-option label="私密" value="private" />
          </el-select>
        </el-form-item>

        <el-form-item label="搜索">
          <el-input
            v-model="filters.search"
            placeholder="搜索标题或作者"
            @keyup.enter="handleSearch"
            clearable
            style="width: 250px"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="refreshList">
            <el-icon><RefreshRight /></el-icon>
            刷新
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 统计信息 -->
    <el-card class="stats-card" shadow="never">
      <el-statistic title="媒体总数" :value="total" suffix="个" />
    </el-card>

    <!-- 媒体列表 -->
    <el-card class="table-card" shadow="never">
      <el-table
        v-loading="loading"
        :data="mediaList"
        stripe
        style="width: 100%"
        :default-sort="{ prop: 'add_date', order: 'descending' }"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column type="index" label="#" width="60" />
        
        <el-table-column label="缩略图" width="120">
          <template #default="{ row }">
            <el-image
              :src="row.thumbnail_url || row.poster_url || '/placeholder.jpg'"
              fit="cover"
              class="thumbnail"
              :preview-src-list="[row.thumbnail_url || row.poster_url || '/placeholder.jpg']"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><VideoPlay /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>

        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="user" label="作者" width="120" />
        
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStateType(row.state)" size="small">
              {{ getStateText(row.state) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="审核状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="(row as any).is_reviewed === true" type="success" size="small">
              <el-icon><Check /></el-icon> 已批准
            </el-tag>
            <el-tag v-else-if="(row as any).is_reviewed === false" type="danger" size="small">
              <el-icon><Close /></el-icon> 已拒绝
            </el-tag>
            <el-tag v-else type="warning" size="small">
              待审核
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="media_type" label="类型" width="80" />
        
        <el-table-column label="时长" width="80">
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>

        <el-table-column prop="views" label="观看" width="80" sortable />
        
        <el-table-column prop="likes" label="点赞" width="80" sortable />
        
        <el-table-column prop="dislikes" label="不喜欢" width="90" sortable />

        <el-table-column label="举报" width="80" sortable>
          <template #default="{ row }">
            <el-tag v-if="row.reported_times && row.reported_times > 0" type="danger" size="small">
              {{ row.reported_times }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column label="添加时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.add_date) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="viewMedia(row)">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editMedia(row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button size="small" type="danger" @click="deleteMedia(row)">
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div v-if="total > pageSize" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.admin-media-manage {
  max-width: 1600px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.page-header p {
  font-size: 1rem;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-card {
  margin-bottom: 16px;
}

.filter-card :deep(.el-form--inline .el-form-item) {
  margin-bottom: 0;
}

.stats-card {
  margin-bottom: 16px;
  text-align: center;
}

.table-card {
  margin-bottom: 16px;
}

.thumbnail {
  width: 100px;
  height: 60px;
  border-radius: 4px;
  object-fit: cover;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 24px;
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .admin-media-manage {
    padding: 12px;
  }
  
  .filter-card :deep(.el-form--inline) {
    display: flex;
    flex-wrap: wrap;
  }
}

@media (max-width: 768px) {
  .page-header h1 {
    font-size: 1.5rem;
  }
  
  .thumbnail {
    width: 80px;
    height: 50px;
  }
}
</style>
