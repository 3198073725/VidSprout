<template>
  <div class="admin-stats-charts">
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户增长趋势</span>
              <el-tag type="info">{{ userGrowthStats.totalUsers }} 总用户</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <canvas ref="userGrowthChart"></canvas>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>媒体上传量统计</span>
              <el-tag type="info">{{ mediaUploadStats.totalMedia }} 总媒体</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <canvas ref="mediaUploadChart"></canvas>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户活跃度分析</span>
              <el-tag type="success">{{ activityStats.activeUsers }} 活跃用户</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <canvas ref="activityChart"></canvas>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>媒体类型分布</span>
              <el-tag type="warning">{{ mediaTypeStats.total }} 总计</el-tag>
            </div>
          </template>
          <div class="chart-container">
            <canvas ref="mediaTypeChart"></canvas>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="chart-row">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>系统概览</span>
              <el-button-group>
                <el-button size="small" @click="refreshStats">
                  <el-icon><Refresh /></el-icon>
                  刷新
                </el-button>
                <el-button size="small" @click="exportStats">
                  <el-icon><Download /></el-icon>
                  导出
                </el-button>
              </el-button-group>
            </div>
          </template>
          <div class="stats-grid">
            <el-row :gutter="20">
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-value">{{ overviewStats.totalUsers }}</div>
                  <div class="stat-label">总用户数</div>
                  <div class="stat-change" :class="{ positive: overviewStats.userGrowth > 0 }">
                    <el-icon><Top /></el-icon>
                    {{ Math.abs(overviewStats.userGrowth) }}%
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-value">{{ overviewStats.totalMedia }}</div>
                  <div class="stat-label">总媒体数</div>
                  <div class="stat-change" :class="{ positive: overviewStats.mediaGrowth > 0 }">
                    <el-icon><Top /></el-icon>
                    {{ Math.abs(overviewStats.mediaGrowth) }}%
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-value">{{ overviewStats.totalComments }}</div>
                  <div class="stat-label">总评论数</div>
                  <div class="stat-change" :class="{ positive: overviewStats.commentGrowth > 0 }">
                    <el-icon><Top /></el-icon>
                    {{ Math.abs(overviewStats.commentGrowth) }}%
                  </div>
                </div>
              </el-col>
              <el-col :span="6">
                <div class="stat-item">
                  <div class="stat-value">{{ overviewStats.activeUsers }}</div>
                  <div class="stat-label">活跃用户</div>
                  <div class="stat-change" :class="{ positive: overviewStats.activityGrowth > 0 }">
                    <el-icon><Top /></el-icon>
                    {{ Math.abs(overviewStats.activityGrowth) }}%
                  </div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, Download, Top } from '@element-plus/icons-vue'
import { AdminAPI } from '@/api'
import Chart from 'chart.js/auto'

interface StatsData {
  userGrowth: any[]
  mediaUpload: any[]
  activity: any[]
  mediaType: any[]
  overview: any
}

const props = defineProps<{
  statsData?: StatsData
}>()

const emit = defineEmits<{
  refresh: []
  export: []
}>()

// Chart refs
const userGrowthChart = ref<HTMLCanvasElement>()
const mediaUploadChart = ref<HTMLCanvasElement>()
const activityChart = ref<HTMLCanvasElement>()
const mediaTypeChart = ref<HTMLCanvasElement>()

// Chart instances
let userGrowthChartInstance: Chart | null = null
let mediaUploadChartInstance: Chart | null = null
let activityChartInstance: Chart | null = null
let mediaTypeChartInstance: Chart | null = null

// Stats data
const userGrowthStats = ref({
  totalUsers: 0,
  data: [] as any[]
})

const mediaUploadStats = ref({
  totalMedia: 0,
  data: [] as any[]
})

const activityStats = ref({
  activeUsers: 0,
  data: [] as any[]
})

const mediaTypeStats = ref({
  total: 0,
  data: [] as any[]
})

const overviewStats = ref({
  totalUsers: 0,
  totalMedia: 0,
  totalComments: 0,
  activeUsers: 0,
  userGrowth: 0,
  mediaGrowth: 0,
  commentGrowth: 0,
  activityGrowth: 0
})

// 初始化图表
async function initCharts() {
  await nextTick()
  
  // 用户增长图表
  if (userGrowthChart.value) {
    const ctx = userGrowthChart.value.getContext('2d')
    if (ctx) {
      userGrowthChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: userGrowthStats.value.data.map(item => item.date),
          datasets: [{
            label: '新增用户',
            data: userGrowthStats.value.data.map(item => item.count),
            borderColor: '#409EFF',
            backgroundColor: 'rgba(64, 158, 255, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }
  }
  
  // 媒体上传图表
  if (mediaUploadChart.value) {
    const ctx = mediaUploadChart.value.getContext('2d')
    if (ctx) {
      mediaUploadChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: mediaUploadStats.value.data.map(item => item.date),
          datasets: [{
            label: '上传数量',
            data: mediaUploadStats.value.data.map(item => item.count),
            backgroundColor: '#67C23A',
            borderColor: '#67C23A',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }
  }
  
  // 活跃度图表
  if (activityChart.value) {
    const ctx = activityChart.value.getContext('2d')
    if (ctx) {
      activityChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: activityStats.value.data.map(item => item.label),
          datasets: [{
            data: activityStats.value.data.map(item => item.count),
            backgroundColor: [
              '#409EFF',
              '#67C23A',
              '#E6A23C',
              '#F56C6C',
              '#909399'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      })
    }
  }
  
  // 媒体类型图表
  if (mediaTypeChart.value) {
    const ctx = mediaTypeChart.value.getContext('2d')
    if (ctx) {
      mediaTypeChartInstance = new Chart(ctx, {
        type: 'pie',
        data: {
          labels: mediaTypeStats.value.data.map(item => item.type),
          datasets: [{
            data: mediaTypeStats.value.data.map(item => item.count),
            backgroundColor: [
              '#409EFF',
              '#67C23A',
              '#E6A23C',
              '#F56C6C'
            ]
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            }
          }
        }
      })
    }
  }
}

// 更新图表数据
function updateCharts() {
  if (props.statsData) {
    userGrowthStats.value = {
      totalUsers: props.statsData.userGrowth.reduce((sum, item) => sum + item.count, 0),
      data: props.statsData.userGrowth
    }
    
    mediaUploadStats.value = {
      totalMedia: props.statsData.mediaUpload.reduce((sum, item) => sum + item.count, 0),
      data: props.statsData.mediaUpload
    }
    
    activityStats.value = {
      activeUsers: props.statsData.activity.reduce((sum, item) => sum + item.count, 0),
      data: props.statsData.activity
    }
    
    mediaTypeStats.value = {
      total: props.statsData.mediaType.reduce((sum, item) => sum + item.count, 0),
      data: props.statsData.mediaType
    }
    
    overviewStats.value = props.statsData.overview
  }
}

// 刷新统计数据
async function refreshStats() {
  try {
    emit('refresh')
  } catch (error) {
    ElMessage.error('刷新失败')
  }
}

// 导出统计数据
function exportStats() {
  emit('export')
}

// 销毁图表
function destroyCharts() {
  if (userGrowthChartInstance) {
    userGrowthChartInstance.destroy()
    userGrowthChartInstance = null
  }
  if (mediaUploadChartInstance) {
    mediaUploadChartInstance.destroy()
    mediaUploadChartInstance = null
  }
  if (activityChartInstance) {
    activityChartInstance.destroy()
    activityChartInstance = null
  }
  if (mediaTypeChartInstance) {
    mediaTypeChartInstance.destroy()
    mediaTypeChartInstance = null
  }
}

watch(() => props.statsData, () => {
  updateCharts()
  destroyCharts()
  initCharts()
}, { deep: true })

onMounted(() => {
  updateCharts()
  initCharts()
})

onUnmounted(() => {
  destroyCharts()
})
</script>

<style scoped>
.admin-stats-charts {
  padding: 20px;
}

.chart-row {
  margin-bottom: 20px;
}

.chart-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
  position: relative;
}

.stats-grid {
  padding: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-change {
  font-size: 12px;
  color: #f56c6c;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}

.stat-change.positive {
  color: #67c23a;
}

.stat-change.positive .el-icon {
  transform: rotate(0deg);
}

.stat-change:not(.positive) .el-icon {
  transform: rotate(180deg);
}
</style>