<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Delete } from '@element-plus/icons-vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { getUserAction, clearUserAction } from '@/api/user'
import type { MediaItem, Paginated } from '@/api'

const router = useRouter()
const loading = ref(false)
const clearingAll = ref(false)
const page = ref(1)
const list = ref<Paginated<MediaItem> | null>(null)
const timeFilter = ref<'all' | 'today' | 'week' | 'month'>('all')

const load = async (p = 1) => {
  loading.value = true
  try {
    page.value = p
    list.value = await getUserAction('watch', { page: p })
    
    // 前端过滤（如果后端不支持时间筛选）
    if (timeFilter.value !== 'all' && list.value?.results) {
      list.value.results = filterByTime(list.value.results)
    }
  } finally {
    loading.value = false
  }
}

const formatDuration = (seconds?: number) => {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const filterByTime = (items: MediaItem[]): MediaItem[] => {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  return items.filter(item => {
    if (!item.add_date) return true
    const itemDate = new Date(item.add_date)
    
    switch (timeFilter.value) {
      case 'today':
        return itemDate >= today
      case 'week':
        const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000)
        return itemDate >= weekAgo
      case 'month':
        const monthAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)
        return itemDate >= monthAgo
      default:
        return true
    }
  })
}

const handleTimeFilter = (filter: typeof timeFilter.value) => {
  timeFilter.value = filter
  load(1)
}

const clearHistory = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空所有历史记录吗？此操作不可恢复！',
      '清空历史',
      {
        confirmButtonText: '确定清空',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    clearingAll.value = true
    
    try {
      // 调用后端API批量删除观看记录
      const response = await clearUserAction('watch')
      
      ElMessage.success(response.detail || `已清空 ${response.count} 条历史记录`)
      
      // 重新加载列表（应该为空）
      await load(1)
    } catch (error) {
      console.error('清空历史失败:', error)
      ElMessage.error('清空历史失败，请稍后再试')
    } finally {
      clearingAll.value = false
    }
  } catch {
    // 用户取消
  }
}

const openMedia = (item: MediaItem) => {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

const handlePageChange = (p: number) => {
  load(p)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => load(1))
</script>

<template>
  <div class="history-page">
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">历史记录</h1>
        <div class="history-stats" v-if="list?.count">
          共 <strong>{{ list.count }}</strong> 条观看记录
        </div>
      </div>
      <div class="header-actions">
        <el-button-group class="time-filter">
          <el-button 
            :type="timeFilter === 'all' ? 'primary' : 'default'"
            size="small"
            @click="handleTimeFilter('all')"
          >
            全部
          </el-button>
          <el-button 
            :type="timeFilter === 'today' ? 'primary' : 'default'"
            size="small"
            @click="handleTimeFilter('today')"
          >
            今天
          </el-button>
          <el-button 
            :type="timeFilter === 'week' ? 'primary' : 'default'"
            size="small"
            @click="handleTimeFilter('week')"
          >
            本周
          </el-button>
          <el-button 
            :type="timeFilter === 'month' ? 'primary' : 'default'"
            size="small"
            @click="handleTimeFilter('month')"
          >
            本月
          </el-button>
        </el-button-group>
        <el-button 
          type="danger" 
          @click="clearHistory"
          v-if="list?.results?.length"
          :loading="clearingAll"
        >
          <el-icon><Delete /></el-icon>
          清空历史
        </el-button>
      </div>
    </div>
    
    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="skeleton-container">
          <div class="items-grid">
            <el-skeleton-item 
              v-for="n in 12" 
              :key="n"
              variant="rect" 
              style="width: 100%; padding-top: 56.25%; margin-bottom: 8px"
            />
          </div>
        </div>
      </template>

      <template #default>
        <div v-if="list?.results?.length" class="history-content">
          <!-- 使用和首页一致的网格布局 -->
          <div class="items-grid">
            <div 
              v-for="item in list.results" 
              :key="item.friendly_token"
              class="item-thumb"
              :class="{ 'image-media-thumb': item.media_type === 'image' }"
              @click="openMedia(item)"
            >
              <div class="thumb-image-container">
                <img 
                  :src="item.thumbnail_url || item.poster_url || '/placeholder.jpg'"
                  :alt="item.title"
                  class="thumb-image"
                  :class="{ 'image-media': item.media_type === 'image' }"
                />
                <div v-if="item.duration" class="thumb-duration">
                  {{ formatDuration(item.duration) }}
                </div>
              </div>
              <div class="thumb-body">
                <div class="thumb-title">{{ item.title }}</div>
                <div class="thumb-meta">
                  {{ item.author_name || item.user }} · {{ item.views || 0 }} 次观看
                </div>
                
                <!-- 显示分类和标签 -->
                <div v-if="item.categories_info?.length || item.tags_info?.length" class="thumb-tags">
                  <el-tag 
                    v-for="category in item.categories_info?.slice(0, 2)" 
                    :key="category.title"
                    size="small"
                    type="primary"
                    class="media-tag"
                  >
                    {{ category.title }}
                  </el-tag>
                  <el-tag 
                    v-for="tag in item.tags_info?.slice(0, 2)" 
                    :key="tag.title"
                    size="small"
                    class="media-tag"
                  >
                    {{ tag.title }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
          
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
          v-else 
          description="还没有观看记录" 
          :image-size="120"
        >
          <el-button type="primary" @click="router.push('/')">去首页看看</el-button>
        </el-empty>
      </template>
    </el-skeleton>
  </div>
</template>

<style scoped>
.history-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.time-filter {
  display: flex;
}

.history-stats {
  font-size: 14px;
  color: #666;
}

.history-stats strong {
  color: #409eff;
  font-weight: 600;
}

.history-content {
  min-height: 400px;
}

/* 使用和首页一致的网格布局 */
.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
  padding: 0;
  width: 100%;
}

.item-thumb {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  height: 220px;
}

.item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-4px);
}

.thumb-image-container {
  position: relative;
  width: 100%;
  flex: 0 0 auto;
  aspect-ratio: 16 / 9;
  background: #f5f5f5;
  overflow: hidden;
  border-radius: 8px 8px 0 0;
}

.thumb-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  border-radius: 8px 8px 0 0;
}

.thumb-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  font-family: monospace;
  font-weight: 500;
}

.thumb-body {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 0 0 auto;
  min-height: 70px;
  overflow: visible;
}

.thumb-title {
  font-size: 13px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
  flex-shrink: 0;
}

.thumb-meta {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex-shrink: 0;
}

.skeleton-container {
  padding: 20px 0;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.pagination {
  margin-top: 32px;
  display: flex;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .history-page {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .header-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .time-filter {
    width: 100%;
  }
  
  .time-filter :deep(.el-button) {
    flex: 1;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 16px;
  }
  
  .thumb-body {
    padding: 10px;
    gap: 4px;
  }
  
  .thumb-title {
    font-size: 13px;
  }
  
  .thumb-meta {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .history-page {
    padding: 12px;
  }
  
  .items-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 12px;
  }
  
  .thumb-body {
    padding: 8px;
  }
  
  .thumb-title {
    font-size: 12px;
    -webkit-line-clamp: 1;
    min-height: 20px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .history-page {
  background: #0a0a0a;
  color: #ffffff;
}

[data-theme="dark"] .page-title {
  color: #ffffff;
}

[data-theme="dark"] .stats-info {
  color: #999;
}

[data-theme="dark"] .item-thumb {
  background: #1a1a1a;
  border-color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .item-thumb:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
}

[data-theme="dark"] .thumb-image-container {
  background: #2a2a2a;
}

[data-theme="dark"] .thumb-title {
  color: #ffffff;
}

[data-theme="dark"] .thumb-meta {
  color: #999;
}

[data-theme="dark"] .thumb-duration {
  background: rgba(0, 0, 0, 0.8);
  color: #ffffff;
}

[data-theme="dark"] .login-required {
  background: #0a0a0a;
}
</style>
