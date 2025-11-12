<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RatingAPI } from '@/api'
import type { RatingCategory, MediaRatingStats } from '@/api/rating'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'

const props = defineProps<{
  mediaToken: string
}>()

const auth = useAuthStore()
const loading = ref(false)
const categories = ref<RatingCategory[]>([])
const ratingsStats = ref<MediaRatingStats[]>([])
const submitting = ref(false)

// 加载评分分类和统计
onMounted(async () => {
  await loadRatings()
})

async function loadRatings() {
  loading.value = true
  try {
    // 并行加载评分分类和媒体评分统计
    const [categoriesData, statsData] = await Promise.all([
      RatingAPI.getRatingCategories(),
      RatingAPI.getMediaRatings(props.mediaToken)
    ])
    
    categories.value = categoriesData
    ratingsStats.value = statsData.ratings
  } catch (error) {
    console.error('加载评分失败:', error)
    ElMessage.error('加载评分失败')
  } finally {
    loading.value = false
  }
}

// 获取指定分类的统计信息
function getCategoryStats(categoryId: number): MediaRatingStats | undefined {
  return ratingsStats.value.find(s => s.category_id === categoryId)
}

// 提交评分
async function handleRate(categoryId: number, score: number) {
  if (!auth.isLoggedIn) {
    ElMessage.warning('请先登录才能评分')
    return
  }
  
  submitting.value = true
  try {
    await RatingAPI.rateMedia(props.mediaToken, categoryId, score)
    ElMessage.success('评分成功！')
    // 重新加载评分统计
    await loadRatings()
  } catch (error) {
    console.error('评分失败:', error)
    ElMessage.error('评分失败，请稍后再试')
  } finally {
    submitting.value = false
  }
}

// 是否有评分数据
const hasRatings = computed(() => {
  return ratingsStats.value.some(s => s.count > 0)
})
</script>

<template>
  <div class="media-rating">
    <div class="rating-header">
      <h3>
        <el-icon><StarFilled /></el-icon>
        媒体评分
      </h3>
      <span v-if="hasRatings" class="rating-count">
        {{ ratingsStats.reduce((sum, s) => sum + s.count, 0) }} 个评分
      </span>
    </div>

    <el-skeleton :loading="loading" animated>
      <template #template>
        <div class="rating-skeleton">
          <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 12px;" />
          <el-skeleton-item variant="text" style="width: 100%; margin-bottom: 12px;" />
        </div>
      </template>

      <template #default>
        <div v-if="categories.length === 0" class="no-categories">
          <el-empty description="暂无评分分类" :image-size="80" />
        </div>

        <div v-else class="rating-list">
          <div 
            v-for="category in categories" 
            :key="category.id"
            class="rating-item"
          >
            <div class="rating-item-header">
              <div class="category-info">
                <span class="category-title">{{ category.title }}</span>
                <span v-if="category.description" class="category-desc">
                  {{ category.description }}
                </span>
              </div>
              <div class="rating-stats">
                <template v-if="getCategoryStats(category.id)?.count">
                  <div class="average-score">
                    <span class="score-number">
                      {{ getCategoryStats(category.id)?.average_score?.toFixed(1) || 'N/A' }}
                    </span>
                    <span class="score-max">/5</span>
                  </div>
                  <div class="rating-count-small">
                    {{ getCategoryStats(category.id)?.count }} 人评分
                  </div>
                </template>
                <span v-else class="no-rating">暂无评分</span>
              </div>
            </div>

            <div class="rating-control">
              <span class="your-rating-label">{{ 
                getCategoryStats(category.id)?.user_score 
                  ? '你的评分：' 
                  : '给个评分：' 
              }}</span>
              <el-rate
                :model-value="getCategoryStats(category.id)?.user_score || 0"
                :max="5"
                :disabled="submitting || !auth.isLoggedIn"
                allow-half
                show-score
                @change="(value: number) => handleRate(category.id, value)"
              />
              <span v-if="!auth.isLoggedIn" class="login-tip">
                (请先登录)
              </span>
            </div>
          </div>
        </div>
      </template>
    </el-skeleton>
  </div>
</template>

<style scoped>
.media-rating {
  padding: 24px;
  background: var(--mc-bg-primary, #fff);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-bottom: 24px;
}

[data-theme="dark"] .media-rating {
  background: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.rating-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.rating-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--mc-text-primary, #222);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

[data-theme="dark"] .rating-header h3 {
  color: #ffffff;
}

.rating-header h3 .el-icon {
  color: #f7ba2a;
  font-size: 20px;
}

.rating-count {
  font-size: 14px;
  color: var(--mc-text-secondary, #666);
}

[data-theme="dark"] .rating-count {
  color: #999;
}

.rating-skeleton {
  padding: 20px 0;
}

.no-categories {
  padding: 40px 0;
  text-align: center;
}

.rating-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.rating-item {
  padding: 16px;
  background: var(--el-fill-color-lighter);
  border-radius: 8px;
  transition: all 0.3s;
}

[data-theme="dark"] .rating-item {
  background: #262626;
}

.rating-item:hover {
  background: var(--el-fill-color-light);
}

[data-theme="dark"] .rating-item:hover {
  background: #2a2a2a;
}

.rating-item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.category-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.category-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--mc-text-primary, #222);
}

[data-theme="dark"] .category-title {
  color: #ffffff;
}

.category-desc {
  font-size: 13px;
  color: var(--mc-text-secondary, #666);
}

[data-theme="dark"] .category-desc {
  color: #999;
}

.rating-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.average-score {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.score-number {
  font-size: 24px;
  font-weight: 600;
  color: #f7ba2a;
}

.score-max {
  font-size: 14px;
  color: var(--mc-text-secondary, #666);
}

[data-theme="dark"] .score-max {
  color: #999;
}

.rating-count-small {
  font-size: 12px;
  color: var(--mc-text-light, #999);
}

[data-theme="dark"] .rating-count-small {
  color: #666;
}

.no-rating {
  font-size: 14px;
  color: var(--mc-text-light, #999);
}

[data-theme="dark"] .no-rating {
  color: #666;
}

.rating-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.your-rating-label {
  font-size: 14px;
  color: var(--mc-text-secondary, #666);
  font-weight: 500;
}

[data-theme="dark"] .your-rating-label {
  color: #cccccc;
}

.login-tip {
  font-size: 13px;
  color: var(--el-color-warning);
}

/* 响应式 */
@media (max-width: 768px) {
  .media-rating {
    padding: 16px;
  }

  .rating-item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .rating-stats {
    align-items: flex-start;
  }

  .rating-control {
    flex-wrap: wrap;
  }
}
</style>

