<template>
  <div class="search-suggestions" v-if="showSuggestions">
    <div class="suggestions-container">
      <!-- 搜索建议 -->
      <div class="suggestion-section" v-if="suggestions.length > 0">
        <div class="section-title">搜索建议</div>
        <div 
          v-for="(suggestion, index) in suggestions" 
          :key="`suggestion-${index}`"
          class="suggestion-item"
          @click="selectSuggestion(suggestion.keyword)"
        >
          <el-icon><Search /></el-icon>
          <span class="suggestion-text" v-html="highlightMatch(suggestion.keyword)"></span>
          <span class="suggestion-type" :class="`type-${suggestion.suggestion_type}`">
            {{ getSuggestionTypeLabel(suggestion.suggestion_type) }}
          </span>
        </div>
      </div>

      <!-- 搜索历史 -->
      <div class="suggestion-section" v-if="searchHistory.length > 0 && showHistory">
        <div class="section-header">
          <div class="section-title">搜索历史</div>
          <el-button link type="primary" size="small" @click="clearHistory">
            清空历史
          </el-button>
        </div>
        <div 
          v-for="(history, index) in searchHistory" 
          :key="`history-${index}`"
          class="suggestion-item"
          @click="selectSuggestion(history.query)"
        >
          <el-icon><Clock /></el-icon>
          <span class="suggestion-text">{{ history.query }}</span>
          <span class="search-count">{{ history.search_count }}</span>
        </div>
      </div>

      <!-- 热门搜索 -->
      <div class="suggestion-section" v-if="popularSearches.length > 0">
        <div class="section-title">热门搜索</div>
        <div class="popular-tags">
          <el-tag
            v-for="(tag, index) in popularSearches"
            :key="`popular-${index}`"
            class="popular-tag"
            @click="selectSuggestion(tag)"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>正在获取建议...</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { Search, Clock, Loading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { SearchSuggestionItem, SearchHistoryItem } from '@/api/types'

interface Props {
  modelValue: string
  visible: boolean
  maxSuggestions?: number
  showHistory?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'select', value: string): void
  (e: 'update:visible', visible: boolean): void
}

const props = withDefaults(defineProps<Props>(), {
  maxSuggestions: 10,
  showHistory: true
})

const emit = defineEmits<Emits>()

// 状态
const suggestions = ref<SearchSuggestionItem[]>([])
const searchHistory = ref<SearchHistoryItem[]>([])
const popularSearches = ref<string[]>([])
const loading = ref(false)
const showSuggestions = ref(false)

// 防抖计时器
let debounceTimer: NodeJSTimeout | null = null
let abortController: AbortController | null = null

// 监听输入变化
watch(() => props.modelValue, (newValue) => {
  if (newValue.trim()) {
    debounceGetSuggestions(newValue)
  } else {
    clearSuggestions()
  }
})

watch(() => props.visible, (visible) => {
  showSuggestions.value = visible
})

// 获取搜索建议
const debounceGetSuggestions = (query: string) => {
  // 清除之前的计时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  
  // 取消之前的请求
  if (abortController) {
    abortController.abort()
  }

  // 设置新的防抖计时器
  debounceTimer = setTimeout(() => {
    getSuggestions(query)
  }, 300) // 300ms 防抖
}

const getSuggestions = async (query: string) => {
  if (!query.trim() || query.length < 2) return

  loading.value = true
  abortController = new AbortController()

  try {
    // 这里需要实现对应的API调用
    // 暂时使用模拟数据
    suggestions.value = await mockGetSuggestions(query)
    
    // 同时获取搜索历史和热门搜索
    if (props.showHistory) {
      await Promise.all([
        getSearchHistory(),
        getPopularSearches()
      ])
    }
  } catch (error) {
    if (error instanceof Error && error.name !== 'AbortError') {
      console.error('获取搜索建议失败:', error)
    }
  } finally {
    loading.value = false
  }
}

// 模拟API调用（实际使用时替换为真实API）
const mockGetSuggestions = async (query: string): Promise<SearchSuggestionItem[]> => {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 200))
  
  const mockData: SearchSuggestionItem[] = [
    { id: 1, keyword: `${query} 教程`, suggestion_type: 'popular', weight: 10, search_count: 100, click_count: 50 },
    { id: 2, keyword: `${query} 视频`, suggestion_type: 'related', weight: 8, search_count: 80, click_count: 40 },
    { id: 3, keyword: `${query} 下载`, suggestion_type: 'trending', weight: 6, search_count: 60, click_count: 30 },
  ]
  
  return mockData.filter(item => 
    item.keyword.toLowerCase().includes(query.toLowerCase())
  )
}

const getSearchHistory = async () => {
  try {
    // 从 localStorage 获取搜索历史
    const historyStr = localStorage.getItem('mediacms_search_history')
    if (historyStr) {
      const history = JSON.parse(historyStr) as SearchHistoryItem[]
      // 按搜索次数和最后搜索时间排序
      searchHistory.value = history
        .sort((a, b) => {
          // 先按搜索次数排序
          if (b.search_count !== a.search_count) {
            return b.search_count - a.search_count
          }
          // 搜索次数相同则按时间排序
          return new Date(b.last_searched).getTime() - new Date(a.last_searched).getTime()
        })
        .slice(0, 5) // 最多显示5条
    } else {
      searchHistory.value = []
    }
  } catch (error) {
    console.error('获取搜索历史失败:', error)
    searchHistory.value = []
  }
}

const getPopularSearches = async () => {
  try {
    // 实际API调用
    // popularSearches.value = await SearchAPI.getPopular()
    
    // 模拟数据
    popularSearches.value = ['JavaScript', 'Python', 'Vue.js', 'React', 'Node.js']
  } catch (error) {
    console.error('获取热门搜索失败:', error)
  }
}

// 选择建议
const selectSuggestion = (keyword: string) => {
  emit('update:modelValue', keyword)
  emit('select', keyword)
  emit('update:visible', false)
}

// 清空建议
const clearSuggestions = () => {
  suggestions.value = []
  showSuggestions.value = false
}

// 清空历史
const clearHistory = async () => {
  try {
    localStorage.removeItem('mediacms_search_history')
    searchHistory.value = []
    ElMessage.success('搜索历史已清空')
  } catch (error) {
    console.error('清空搜索历史失败:', error)
    ElMessage.error('清空搜索历史失败')
  }
}

// 高亮匹配文本
const highlightMatch = (text: string) => {
  const query = props.modelValue
  if (!query) return text
  
  const regex = new RegExp(`(${query})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
}

// 获取建议类型标签
const getSuggestionTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    'popular': '热门',
    'related': '相关',
    'corrected': '纠错',
    'trending': '趋势'
  }
  return labels[type] || '推荐'
}

// 点击外部关闭
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.search-suggestions') && !target.closest('.search-input-container')) {
    emit('update:visible', false)
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  if (abortController) {
    abortController.abort()
  }
})
</script>

<style scoped>
.search-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  z-index: 2000;
  max-height: 400px;
  overflow-y: auto;
}

.suggestions-container {
  padding: 8px 0;
}

.suggestion-section {
  margin-bottom: 16px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  margin-bottom: 8px;
}

.section-title {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: var(--el-fill-color-light);
  }
  
  .el-icon {
    margin-right: 8px;
    color: var(--el-text-color-secondary);
  }
}

.suggestion-text {
  flex: 1;
  font-size: 14px;
  color: var(--el-text-color-primary);
  
  :deep(mark) {
    background-color: var(--el-color-primary-light-9);
    color: var(--el-color-primary);
    font-weight: 500;
  }
}

.suggestion-type {
  font-size: 12px;
  padding: 2px 6px;
  border-radius: 3px;
  margin-left: 8px;
  
  &.type-popular {
    background-color: #fef0f0;
    color: #f56c6c;
  }
  
  &.type-related {
    background-color: #f0f9ff;
    color: #409eff;
  }
  
  &.type-corrected {
    background-color: #f0f9ff;
    color: #67c23a;
  }
  
  &.type-trending {
    background-color: #fef9e7;
    color: #e6a23c;
  }
}

.search-count {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-left: 8px;
}

.popular-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 0 16px;
}

.popular-tag {
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    transform: translateY(-1px);
  }
}

.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  color: var(--el-text-color-secondary);
  
  .el-icon {
    margin-right: 8px;
  }
}

/* 暗色主题适配 */
[data-theme="dark"] {
  .search-suggestions {
    background: var(--el-bg-color);
    border-color: var(--el-border-color-darker);
  }
  
  .suggestion-item:hover {
    background-color: var(--el-fill-color-darker);
  }
}
</style>