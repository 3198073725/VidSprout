<script setup lang="ts">
import { onMounted, ref, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Filter, Close } from '@element-plus/icons-vue'
import { SearchAPI } from '@/api'
import type { MediaItem, Paginated, AdvancedSearchParams } from '@/api'
import MediaSection from '@/components/home/MediaSection.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const list = ref<Paginated<MediaItem> | null>(null)
const q = ref<string>((route.query.q as string) || '')
const page = ref(1)
const showAdvancedFilters = ref(false)

// 基础筛选器
const filters = ref({
  type: '', // video, audio, image
  sort: 'relevance' // relevance, -add_date, -views
})

// 高级筛选器
const advancedFilters = ref({
  category: '',
  tag: '',
  author: '',
  duration_min: null as number | null,
  duration_max: null as number | null,
  upload_date: '' as '' | 'today' | 'this_week' | 'this_month' | 'this_year',
  ordering: 'desc' as 'asc' | 'desc'
})

async function load() {
  // 检查是否有任何搜索条件（关键词或筛选器）
  const hasFilters = advancedFilters.value.category || 
                     advancedFilters.value.tag || 
                     advancedFilters.value.author ||
                     filters.value.type
  
  if (!q.value.trim() && !hasFilters) {
    list.value = null
    return
  }
  
  loading.value = true
  try {
    // 构建搜索参数
    const searchParams: AdvancedSearchParams = {
      q: q.value || '', // 空字符串表示无关键词搜索（后端会只使用筛选条件）
      page: page.value,
      media_type: (filters.value.type as 'video' | 'audio' | 'image' | undefined) || undefined,
      sort_by: filters.value.sort === 'relevance' ? 'relevance' : filters.value.sort.replace('-', '') as any,
      ordering: filters.value.sort.startsWith('-') ? 'desc' : 'asc',
      category: advancedFilters.value.category || undefined,
      tag: advancedFilters.value.tag || undefined,
      author: advancedFilters.value.author || undefined,
      duration_min: advancedFilters.value.duration_min || undefined,
      duration_max: advancedFilters.value.duration_max || undefined,
      upload_date: advancedFilters.value.upload_date || undefined,
      highlight: true
    }

    console.log('🔍 执行搜索:', searchParams)
    console.log('📝 分类筛选:', advancedFilters.value.category)
    console.log('🏷️ 标签筛选:', advancedFilters.value.tag)
    
    // 使用增强版搜索API
    list.value = await SearchAPI.enhancedSearch(searchParams)
    
    console.log('✅ 搜索结果:', list.value?.results?.length, '个媒体')
    
    // 保存搜索历史（如果有关键词且用户登录）
    if (q.value.trim()) {
      try {
        await SearchAPI.saveSearchHistory(q.value)
      } catch (error) {
        console.warn('保存搜索历史失败:', error)
      }
    }
  } catch (error: any) {
    console.error('❌ 搜索失败:', error)
    console.error('错误详情:', error.response?.data)
    ElMessage.error('搜索失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  router.push({ name: 'search', query: { q: q.value } })
}

function clearSearch() {
  q.value = ''
  router.push({ name: 'home' })
}

function toggleAdvancedFilters() {
  showAdvancedFilters.value = !showAdvancedFilters.value
}

function clearAdvancedFilters() {
  advancedFilters.value = {
    category: '',
    tag: '',
    author: '',
    duration_min: null,
    duration_max: null,
    upload_date: '',
    ordering: 'desc'
  }
}

function handlePageChange(p: number) {
  page.value = p
  load()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 标志位，防止循环触发
let isUpdatingFromRoute = false

watch(() => route.query, (newQuery) => {
  isUpdatingFromRoute = true
  
  // 更新搜索关键词
  q.value = (newQuery.q as string) || ''
  
  // 更新基础筛选器
  filters.value.type = (newQuery.type as string) || ''
  filters.value.sort = (newQuery.sort as string) || 'relevance'
  
  // 更新高级筛选器
  advancedFilters.value.category = (newQuery.category as string) || ''
  advancedFilters.value.tag = (newQuery.tag as string) || ''
  advancedFilters.value.author = (newQuery.author as string) || ''
  
  // 如果有高级筛选器，自动展开
  if (newQuery.category || newQuery.tag || newQuery.author) {
    showAdvancedFilters.value = true
  }
  
  page.value = 1
  load()
  
  nextTick(() => {
    isUpdatingFromRoute = false
  })
}, { immediate: true })

watch(() => filters.value.type, () => {
  if (!isUpdatingFromRoute) {
    page.value = 1
    load()
  }
})

watch(() => filters.value.sort, () => {
  if (!isUpdatingFromRoute) {
    page.value = 1
    load()
  }
})

// 监听高级筛选器变化
watch(() => advancedFilters.value, () => {
  if (!isUpdatingFromRoute) {
    page.value = 1
    load()
  }
}, { deep: true })

// onMounted 由 watch 的 immediate: true 处理，不需要单独调用
onMounted(() => {
  console.log('🔍 搜索页面已挂载')
  console.log('路由参数:', route.query)
})
</script>

<template>
  <section class="home-sec search-page">
    <div class="home-sec-head">
      <div class="home-sec-title">搜索</div>
      <div class="search-stats" v-if="list?.count">
        找到 <strong>{{ list.count }}</strong> 个结果
      </div>
    </div>
    
    <!-- 搜索信息和筛选器 -->
    <div class="search-info-bar">
      <div class="search-keywords">
        <span v-if="q.trim()" class="keyword-label">搜索关键词：</span>
        <el-tag v-if="q.trim()" size="large" closable @close="clearSearch">{{ q }}</el-tag>
        <span v-else class="no-keyword-text">使用筛选器浏览内容</span>
      </div>
      <div class="filter-controls">
        <el-button
          @click="toggleAdvancedFilters"
          :icon="Filter"
          :type="showAdvancedFilters ? 'primary' : 'default'"
          size="default"
        >
          {{ showAdvancedFilters ? '收起筛选' : '高级筛选' }}
        </el-button>
      </div>
    </div>
    
    <!-- 高级筛选器 -->
    <div class="advanced-filter-panel" v-if="showAdvancedFilters">
      <el-card>
        <template #header>
          <div class="filter-header">
            <span>高级筛选选项</span>
            <el-button link type="primary" @click="clearAdvancedFilters">
              <el-icon><Close /></el-icon>
              清空筛选
            </el-button>
          </div>
        </template>
        
        <el-form :model="advancedFilters" label-width="100px">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="分类">
                <el-input
                  v-model="advancedFilters.category"
                  placeholder="输入分类名称"
                  clearable
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="标签">
                <el-input
                  v-model="advancedFilters.tag"
                  placeholder="输入标签名称"
                  clearable
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="上传者">
                <el-input
                  v-model="advancedFilters.author"
                  placeholder="输入上传者用户名"
                  clearable
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="时长范围">
                <el-input-number
                  v-model="advancedFilters.duration_min"
                  :min="0"
                  :step="60"
                  placeholder="最小值(秒)"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="至">
                <el-input-number
                  v-model="advancedFilters.duration_max"
                  :min="0"
                  :step="60"
                  placeholder="最大值(秒)"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="上传时间">
                <el-select v-model="advancedFilters.upload_date" clearable style="width: 100%">
                  <el-option label="全部时间" value="" />
                  <el-option label="今天" value="today" />
                  <el-option label="本周" value="this_week" />
                  <el-option label="本月" value="this_month" />
                  <el-option label="今年" value="this_year" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </el-card>
    </div>
    
    <!-- 基础筛选器 -->
    <div class="filter-bar" v-if="q.trim()">
      <el-form inline>
        <el-form-item label="类型">
          <el-select v-model="filters.type" placeholder="全部类型" style="width: 140px">
            <el-option label="全部" value="" />
            <el-option label="视频" value="video" />
            <el-option label="音频" value="audio" />
            <el-option label="图片" value="image" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-select v-model="filters.sort" style="width: 140px">
            <el-option label="相关性" value="relevance" />
            <el-option label="最新发布" value="-add_date" />
            <el-option label="最多观看" value="-views" />
            <el-option label="最多点赞" value="-likes" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>
    
    <!-- 搜索结果 -->
    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="skeleton-grid">
          <el-skeleton-item 
            v-for="n in 6" 
            :key="n"
            variant="image" 
            style="width:100%;height:200px" 
          />
        </div>
      </template>
      <template #default>
        <div v-if="list?.results?.length" class="search-results">
          <MediaSection 
            title="" 
            :items="list.results" 
            @open="(item) => router.push({ name: 'media-detail', params: { token: item.friendly_token } })" 
          />
          
          <!-- 分页 -->
          <el-pagination
            v-if="list.count > 20"
            v-model:current-page="page"
            :page-size="20"
            :total="list.count"
            layout="prev, pager, next, jumper, total"
            @current-change="handlePageChange"
            class="pagination"
          />
        </div>
        <el-empty 
          v-else-if="q.trim()" 
          description="没有找到相关结果" 
          :image-size="120"
        >
          <el-button type="primary" @click="q = ''; handleSearch()">清空搜索</el-button>
        </el-empty>
        <el-empty 
          v-else 
          description="请输入关键词开始搜索" 
          :image-size="120"
        />
      </template>
    </el-skeleton>
  </section>
</template>

<style scoped>
.search-page {
  max-width: 1200px;
  margin: 0 auto;
}

.home-sec-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-stats {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.search-stats strong {
  color: var(--el-color-primary);
  font-weight: 600;
}

[data-theme="dark"] .search-stats {
  color: #999;
}

[data-theme="dark"] .search-stats strong {
  color: #4a9eff;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.search-input-container {
  flex: 1;
  position: relative;
}

.advanced-filter-btn {
  white-space: nowrap;
}

.advanced-filter-panel {
  margin-bottom: 20px;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-bar {
  margin-bottom: 24px;
  padding: 16px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
}

[data-theme="dark"] .filter-bar {
  background: #2a2a2a;
}

.filter-bar :deep(.el-form-item) {
  margin-bottom: 0;
  margin-right: 16px;
}

.filter-bar :deep(.el-form-item__label) {
  font-weight: 500;
}

/* 高亮样式 */
:deep(mark) {
  background-color: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
  font-weight: 500;
  padding: 0 2px;
  border-radius: 2px;
}

[data-theme="dark"] :deep(mark) {
  background-color: rgba(64, 158, 255, 0.2);
  color: #4a9eff;
}

.search-results {
  min-height: 400px;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-sec-head {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .filter-bar {
    padding: 12px;
  }
  
  .filter-bar :deep(.el-form) {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .filter-bar :deep(.el-form-item) {
    margin: 0;
  }
  
  .filter-bar :deep(.el-select) {
    width: 100% !important;
  }
  
  .skeleton-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }
  
  .search-info-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 16px 20px;
    background: var(--el-bg-color-page);
    border-radius: 8px;
    border: 1px solid var(--el-border-color-light);
    min-height: 56px;
    gap: 20px;
  }
  
  .search-keywords {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 1;
    min-width: 0;
  }
  
  .keyword-label {
    font-size: 14px;
    color: var(--el-text-color-regular);
    font-weight: 500;
    white-space: nowrap;
  }
  
  .search-keywords .el-tag {
    height: 32px;
    line-height: 30px;
    font-size: 14px;
  }
  
  .filter-controls {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
    margin-left: auto;
  }
  
  .filter-controls .el-button {
    height: 32px;
  }
  
  .no-keyword-text {
    font-size: 14px;
    color: var(--el-text-color-placeholder);
    font-style: italic;
  }
}
</style>
