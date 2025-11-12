<template>
  <div class="comments-container">
    <!-- 批量操作 -->
    <BatchOperations
      :selected-ids="selectedIds"
      type="comments"
      @batch-success="handleBatchSuccess"
      @clear-selection="clearSelection"
    />

    <el-card>
      <!-- 搜索和筛选 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="searchQuery"
            placeholder="搜索评论内容..."
            clearable
            style="width: 300px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <el-select v-model="filters.sort_by" placeholder="排序字段" style="width: 140px" @change="handleSearch">
            <el-option label="按时间排序" value="add_date" />
            <el-option label="按内容排序" value="text" />
          </el-select>

          <el-select v-model="filters.ordering" placeholder="排序方式" style="width: 120px" @change="handleSearch">
            <el-option label="降序" value="desc" />
            <el-option label="升序" value="asc" />
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
        :data="commentList"
        style="width: 100%; margin-top: 20px"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column type="expand">
          <template #default="{ row }">
            <div class="comment-detail">
              <p><strong>评论内容：</strong></p>
              <p>{{ row.text }}</p>
              <el-divider />
              <p><strong>媒体标题：</strong>{{ row.media?.title || '-' }}</p>
              <p><strong>媒体链接：</strong>
                <a v-if="row.media_url" :href="row.media_url" target="_blank" class="media-link">
                  {{ row.media_url }}
                </a>
                <span v-else>-</span>
              </p>
              <p><strong>评论用户：</strong>{{ row.author_name }}</p>
              <p><strong>评论时间：</strong>{{ formatDate(row.add_date) }}</p>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="text" label="评论内容" min-width="300" show-overflow-tooltip />
        <el-table-column prop="author_name" label="用户" width="150" show-overflow-tooltip />
        <el-table-column label="所属媒体" width="200" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.media?.title || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="add_date" label="评论时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.add_date) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="danger" link @click="deleteComment(row)">
              <el-icon><Delete /></el-icon>
              删除
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import BatchOperations from '@/components/BatchOperations.vue'
import { getManageComments, deleteComments } from '@/api/admin'
import dayjs from 'dayjs'

// 评论数据类型
interface Comment {
  uid: string
  text: string
  author_name: string
  media_url?: string
  media?: {
    title?: string
    friendly_token?: string
  }
  add_date: string
}

const loading = ref(false)
const commentList = ref<Comment[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')
const selectedComments = ref<Comment[]>([])

const filters = ref({
  sort_by: 'add_date' as 'text' | 'add_date',
  ordering: 'desc' as 'asc' | 'desc'
})

const selectedIds = computed(() => selectedComments.value.map(c => c.uid))

// 加载评论列表
const loadComments = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      sort_by: filters.value.sort_by,
      ordering: filters.value.ordering
    }
    
    const response = await getManageComments(params)
    commentList.value = response.results
    total.value = response.count
  } catch (error) {
    console.error('加载评论列表失败:', error)
    ElMessage.error('加载评论列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadComments()
}

const handleRefresh = () => {
  loadComments()
}

const handleSelectionChange = (selection: Comment[]) => {
  selectedComments.value = selection
}

const clearSelection = () => {
  selectedComments.value = []
}

const handleBatchSuccess = () => {
  clearSelection()
  loadComments()
}

const formatDate = (date: string) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const deleteComment = async (comment: Comment) => {
  try {
    await ElMessageBox.confirm(`确定要删除这条评论吗？此操作不可撤销！`, '警告', {
      type: 'error'
    })
    
    loading.value = true
    await deleteComments([comment.uid])
    ElMessage.success('删除成功')
    loadComments()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除评论失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadComments()
})
</script>

<style scoped lang="scss">
.comments-container {
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

.comment-detail {
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

  .media-link {
    color: var(--el-color-primary);
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
