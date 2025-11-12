<template>
  <div class="media-list-container">
    <!-- 批量操作 -->
    <BatchOperations
      :selected-ids="selectedIds"
      type="media"
      @batch-success="handleBatchSuccess"
      @clear-selection="clearSelection"
    />

    <el-card>
      <!-- 搜索和筛选 -->
      <div class="toolbar">
        <div class="toolbar-left">
          <el-input
            v-model="searchQuery"
            placeholder="搜索媒体标题..."
            clearable
            style="width: 300px"
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>

          <el-select v-model="filters.state" placeholder="状态" clearable style="width: 120px" @change="handleSearch">
            <el-option label="公开" value="public" />
            <el-option label="私密" value="private" />
            <el-option label="仅限链接" value="unlisted" />
          </el-select>

          <el-select v-model="filters.featured" placeholder="精选" clearable style="width: 120px" @change="handleSearch">
            <el-option label="精选" :value="true" />
            <el-option label="普通" :value="false" />
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
        :data="mediaList"
        style="width: 100%; margin-top: 20px"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column label="缩略图" width="120">
          <template #default="{ row }">
            <el-image
              :src="row.thumbnail_url || row.poster_url"
              fit="cover"
              style="width: 80px; height: 60px; border-radius: 4px"
              :preview-src-list="[row.poster_url]"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="media_type" label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="getMediaTypeTag(row.media_type)" size="small">
              {{ row.media_type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="state" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStateTag(row.state)" size="small">
              {{ getStateText(row.state) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="featured" label="精选" width="80">
          <template #default="{ row }">
            <el-icon v-if="row.featured" color="#409eff" :size="20"><StarFilled /></el-icon>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="views" label="观看" width="100" sortable />
        <el-table-column prop="likes" label="点赞" width="100" sortable />
        <el-table-column prop="user" label="作者" width="120" show-overflow-tooltip />
        <el-table-column prop="add_date" label="上传时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.add_date) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button type="primary" size="small" @click="viewMedia(row)">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button type="danger" size="small" @click="deleteMedia(row)">
                <el-icon><Delete /></el-icon>
                删除
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getManageMedia } from '@/api/admin'
import type { MediaItem } from '@/api/types'
import BatchOperations from '@/components/BatchOperations.vue'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const mediaList = ref<MediaItem[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const searchQuery = ref('')
const selectedMedia = ref<MediaItem[]>([])

// 选中的媒体 ID 列表
const selectedIds = computed(() => selectedMedia.value.map(item => item.friendly_token))

// 清空选择
const clearSelection = () => {
  selectedMedia.value = []
}

// 批量操作成功后
const handleBatchSuccess = () => {
  clearSelection()
  loadMedia()
}

const filters = ref({
  state: undefined as undefined | string,
  featured: undefined as undefined | boolean
})

// 加载媒体列表
const loadMedia = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      search: searchQuery.value,
      state: filters.value.state,
      featured: filters.value.featured
    }
    
    const response = await getManageMedia(params)
    mediaList.value = response.results
    total.value = response.count
  } catch (error) {
    ElMessage.error('加载媒体列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadMedia()
}

const handleRefresh = () => {
  loadMedia()
}

const handleSelectionChange = (selection: MediaItem[]) => {
  selectedMedia.value = selection
}

const getMediaTypeTag = (type: string) => {
  const map: Record<string, any> = {
    video: 'primary',
    image: 'success',
    audio: 'warning',
    pdf: 'info'
  }
  return map[type] || ''
}

const getStateTag = (state: string) => {
  const map: Record<string, any> = {
    public: 'success',
    private: 'danger',
    unlisted: 'warning'
  }
  return map[state] || ''
}

const getStateText = (state: string) => {
  const map: Record<string, string> = {
    public: '公开',
    private: '私密',
    unlisted: '仅限链接'
  }
  return map[state] || state
}

const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

// 查看媒体详情（跳转到管理员的媒体详情页，可以查看和编辑）
const viewMedia = (media: MediaItem) => {
  console.log('📍 查看媒体详情:', media.friendly_token)
  router.push(`/media/detail/${media.friendly_token}`)
}

const deleteMedia = async (media: MediaItem) => {
  await ElMessageBox.confirm(`确定要删除媒体"${media.title}"吗？`, '警告', {
    type: 'warning'
  })
  ElMessage.success('删除功能待实现')
}

onMounted(() => {
  loadMedia()
})
</script>

<style scoped lang="scss">
.media-list-container {
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

.image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
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

