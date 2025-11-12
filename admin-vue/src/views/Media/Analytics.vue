<template>
  <div class="analytics-container">
    <!-- 数据概览 -->
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon :size="40" color="#409EFF"><VideoPlay /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ totalMediaCount }}</div>
              <div class="stat-label">总媒体数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon :size="40" color="#67C23A"><View /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ formatNumber(totalViews) }}</div>
              <div class="stat-label">总观看次数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon :size="40" color="#E6A23C"><Star /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ formatNumber(totalLikes) }}</div>
              <div class="stat-label">总点赞数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <el-icon :size="40" color="#F56C6C"><ChatDotRound /></el-icon>
            <div class="stat-content">
              <div class="stat-value">{{ totalComments }}</div>
              <div class="stat-label">总评论数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <!-- 观看趋势 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>观看趋势（最近30天）</span>
              <el-button size="small" @click="loadViewsTrend">
                <el-icon><RefreshRight /></el-icon>
                刷新
              </el-button>
            </div>
          </template>
          <LineChart
            :data="viewsTrendData"
            height="300px"
            x-key="date"
            y-key="views"
            color="#409EFF"
          />
        </el-card>
      </el-col>

      <!-- 媒体类型分布 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>媒体类型分布</span>
            </div>
          </template>
          <PieChart :data="mediaTypeData" height="300px" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 热门媒体列表 -->
    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>热门媒体 Top 10</span>
          <el-button-group>
            <el-button
              :type="sortBy === 'views' ? 'primary' : ''"
              size="small"
              @click="sortBy = 'views'; loadTopMedia()"
            >
              按观看
            </el-button>
            <el-button
              :type="sortBy === 'likes' ? 'primary' : ''"
              size="small"
              @click="sortBy = 'likes'; loadTopMedia()"
            >
              按点赞
            </el-button>
          </el-button-group>
        </div>
      </template>

      <el-table v-loading="loading" :data="topMediaList" style="width: 100%">
        <el-table-column label="排名" width="80">
          <template #default="{ $index }">
            <el-tag v-if="$index === 0" type="danger" size="small">🥇</el-tag>
            <el-tag v-else-if="$index === 1" type="warning" size="small">🥈</el-tag>
            <el-tag v-else-if="$index === 2" type="success" size="small">🥉</el-tag>
            <span v-else>{{ $index + 1 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="封面" width="120">
          <template #default="{ row }">
            <el-image
              :src="row.thumbnail_url"
              fit="cover"
              style="width: 100px; height: 56px; border-radius: 4px"
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
        <el-table-column prop="author_name" label="作者" width="120" />
        <el-table-column label="类型" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ getMediaTypeName(row.media_type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="views" label="观看" width="100" sortable>
          <template #default="{ row }">
            {{ formatNumber(row.views || 0) }}
          </template>
        </el-table-column>
        <el-table-column prop="likes" label="点赞" width="100" sortable>
          <template #default="{ row }">
            {{ formatNumber(row.likes || 0) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="viewDetail(row)">
              <el-icon><View /></el-icon>
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import LineChart from '@/components/charts/LineChart.vue'
import PieChart from '@/components/charts/PieChart.vue'
import { getManageMedia, getDashboardStats } from '@/api/admin'
import type { MediaItem } from '@/api/types'

const router = useRouter()

const loading = ref(false)
const totalMediaCount = ref(0)
const totalViews = ref(0)
const totalLikes = ref(0)
const totalComments = ref(0)
const sortBy = ref<'views' | 'likes'>('views')

const viewsTrendData = ref<Array<{ date: string; views: number }>>([])
const mediaTypeData = ref<Array<{ name: string; value: number }>>([])
const topMediaList = ref<MediaItem[]>([])

// 格式化数字
const formatNumber = (num: number): string => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const getMediaTypeName = (type: string) => {
  const map: Record<string, string> = {
    video: '视频',
    image: '图片',
    audio: '音频',
    pdf: 'PDF'
  }
  return map[type] || type
}

// 从后端API加载观看趋势数据
const loadViewsTrend = async () => {
  try {
    const data = await getDashboardStats()
    
    console.log('📊 后端返回的完整数据:', data)
    console.log('📈 daily_stats 数据:', data.daily_stats)
    
    // 处理近30天的观看趋势数据
    if (data.daily_stats && data.daily_stats.length > 0) {
      viewsTrendData.value = data.daily_stats.map((item: any) => ({
        date: new Date(item.date).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }),
        views: item.views || 0
      }))
      console.log('✅ 观看趋势数据已处理:', viewsTrendData.value)
    } else {
      console.warn('⚠️ daily_stats 数据为空，生成模拟数据')
      // 如果没有数据，生成一些模拟数据以便查看图表
      const now = new Date()
      viewsTrendData.value = Array.from({ length: 30 }, (_, i) => {
        const date = new Date(now)
        date.setDate(date.getDate() - (29 - i))
        return {
          date: date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }),
          views: Math.floor(Math.random() * 20)  // 0-19之间的随机数
        }
      })
    }
  } catch (error) {
    console.error('❌ 加载观看趋势失败:', error)
    viewsTrendData.value = []
  }
}

// 从后端API加载媒体类型分布
const loadMediaTypeDistribution = async () => {
  try {
    const data = await getDashboardStats()
    
    console.log('🎨 media_by_type 数据:', data.media_by_type)
    
    // 媒体类型名称映射
    const typeNameMap: Record<string, string> = {
      'video': '视频',
      'image': '图片',
      'audio': '音频',
      'pdf': 'PDF'
    }
    
    if (data.media_by_type && data.media_by_type.length > 0) {
      mediaTypeData.value = data.media_by_type
        .filter((item: any) => item.count > 0)
        .map((item: any) => ({
          name: typeNameMap[item.media_type] || item.media_type,
          value: item.count
        }))
      console.log('✅ 媒体类型分布已处理:', mediaTypeData.value)
    } else {
      console.warn('⚠️ media_by_type 数据为空，生成模拟数据')
      // 如果没有数据，生成一些模拟数据
      mediaTypeData.value = [
        { name: '视频', value: 1 },
        { name: '图片', value: 2 },
        { name: '音频', value: 1 }
      ]
    }
  } catch (error) {
    console.error('❌ 加载媒体类型分布失败:', error)
    mediaTypeData.value = []
  }
}

// 加载热门媒体
const loadTopMedia = async () => {
  loading.value = true
  try {
    const response = await getManageMedia({
      sort_by: sortBy.value,
      ordering: 'desc',
      page: 1
    })
    
    // 取前10条
    topMediaList.value = response.results.slice(0, 10)
  } catch (error) {
    console.error('加载热门媒体失败:', error)
    ElMessage.error('加载热门媒体失败')
  } finally {
    loading.value = false
  }
}

// 从后端API加载统计概览
const loadStats = async () => {
  try {
    const data = await getDashboardStats()
    
    // 使用后端返回的总体统计数据
    if (data.overview) {
      totalMediaCount.value = data.overview.total_media || 0
      totalViews.value = data.overview.total_views || 0
      totalLikes.value = data.overview.total_likes || 0
      totalComments.value = data.overview.total_comments || 0
    }
    
    console.log('✅ 统计数据加载成功:', data.overview)
  } catch (error) {
    console.error('❌ 加载统计数据失败:', error)
    // 保持默认值0
  }
}

const viewDetail = (media: MediaItem) => {
  router.push(`/media/detail/${media.friendly_token}`)
}

onMounted(async () => {
  console.log('📊 开始加载媒体数据分析...')
  await loadStats()
  await loadViewsTrend()
  await loadMediaTypeDistribution()
  await loadTopMedia()
  console.log('✅ 媒体数据分析加载完成')
})
</script>

<style scoped lang="scss">
.analytics-container {
  padding: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;

  .stat-content {
    flex: 1;

    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: var(--el-text-color-primary);
      line-height: 1.2;
    }

    .stat-label {
      font-size: 14px;
      color: var(--el-text-color-secondary);
      margin-top: 4px;
    }
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-slot {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-lighter);
  color: var(--el-text-color-secondary);

  .el-icon {
    font-size: 24px;
  }
}
</style>
