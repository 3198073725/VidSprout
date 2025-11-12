<template>
  <div class="dashboard-container">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: #409eff20; color: #409eff;">
              <el-icon :size="32"><VideoPlay /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">总媒体数</div>
              <div class="stat-value">{{ stats.totalMedia || 0 }}</div>
              <div class="stat-trend success">
                <el-icon><CaretTop /></el-icon>
                <span>+12.5%</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: #67c23a20; color: #67c23a;">
              <el-icon :size="32"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">总用户数</div>
              <div class="stat-value">{{ stats.totalUsers || 0 }}</div>
              <div class="stat-trend success">
                <el-icon><CaretTop /></el-icon>
                <span>+8.3%</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: #e6a23c20; color: #e6a23c;">
              <el-icon :size="32"><View /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">今日观看</div>
              <div class="stat-value">{{ stats.todayViews || 0 }}</div>
              <div class="stat-trend">
                <el-icon><CaretBottom /></el-icon>
                <span>-3.2%</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <div class="stat-icon" style="background: #f56c6c20; color: #f56c6c;">
              <el-icon :size="32"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">待审核</div>
              <div class="stat-value">{{ stats.pendingReview || 0 }}</div>
              <div class="stat-trend danger">
                <el-icon><Warning /></el-icon>
                <span>需处理</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row :gutter="20" class="quick-actions">
      <el-col :xs="24" :lg="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <div class="action-buttons">
            <el-button type="primary" @click="$router.push('/media/list')">
              <el-icon><VideoPlay /></el-icon>
              <span>媒体管理</span>
            </el-button>
            <el-button type="success" @click="$router.push('/users/list')">
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </el-button>
            <el-button type="warning" @click="$router.push('/content/comments')">
              <el-icon><ChatDotRound /></el-icon>
              <span>评论管理</span>
            </el-button>
            <el-button type="info" @click="$router.push('/system/monitoring')">
              <el-icon><Monitor /></el-icon>
              <span>系统监控</span>
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :xs="24" :lg="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>媒体上传趋势（最近30天）</span>
            </div>
          </template>
          <LineChart :data="uploadTrendData" height="320px" />
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="8">
        <el-card>
          <template #header>
            <span>媒体类型分布</span>
          </template>
          <PieChart :data="mediaTypeData" height="320px" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 系统信息 -->
    <el-row :gutter="20">
      <el-col :xs="24" :lg="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统状态</span>
              <el-button type="primary" link @click="$router.push('/system/monitoring')">
                查看详情 <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </template>
          <div class="system-status">
            <div class="status-item">
              <span class="status-label">CPU 使用率</span>
              <el-progress :percentage="systemStatus.cpu" :color="getStatusColor(systemStatus.cpu)" />
            </div>
            <div class="status-item">
              <span class="status-label">内存使用率</span>
              <el-progress :percentage="systemStatus.memory" :color="getStatusColor(systemStatus.memory)" />
            </div>
            <div class="status-item">
              <span class="status-label">磁盘使用率</span>
              <el-progress :percentage="systemStatus.disk" :color="getStatusColor(systemStatus.disk)" />
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :lg="8">
        <el-card>
          <template #header>
            <span>最近活动</span>
          </template>
          <el-empty v-if="!recentActivities.length" description="暂无最近活动" :image-size="80" />
          <el-timeline v-else>
            <el-timeline-item
              v-for="(item, index) in recentActivities"
              :key="index"
              :timestamp="item.time"
              placement="top"
            >
              {{ item.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboardStats } from '@/api/admin'
import LineChart from '@/components/charts/LineChart.vue'
import PieChart from '@/components/charts/PieChart.vue'

const stats = ref({
  totalMedia: 0,
  totalUsers: 0,
  todayViews: 0,
  pendingReview: 0
})

const systemStatus = ref({
  cpu: 0,
  memory: 0,
  disk: 0
})

const recentActivities = ref<Array<{ time: string; content: string }>>([])

// 图表数据
const uploadTrendData = ref<Array<{ date: string; count: number }>>([])
const mediaTypeData = ref<Array<{ type: string; count: number }>>([])

const getStatusColor = (value: number) => {
  if (value < 60) return '#67c23a'
  if (value < 80) return '#e6a23c'
  return '#f56c6c'
}

onMounted(async () => {
  try {
    const data = await getDashboardStats()
    
    // 映射后端返回的数据到前端字段名
    stats.value = {
      totalMedia: data.overview?.total_media || 0,
      totalUsers: data.overview?.total_users || 0,
      todayViews: data.overview?.total_views || 0,
      pendingReview: data.pending?.pending_media || 0
    }

    // 系统状态数据（如果有的话）
    systemStatus.value = {
      cpu: 0,  // 后续会从系统监控 API 获取
      memory: 0,
      disk: 0
    }

    // 处理图表数据 - 媒体上传趋势
    if (data.daily_stats && data.daily_stats.length > 0) {
      uploadTrendData.value = data.daily_stats.map((item: any) => ({
        date: new Date(item.date).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }),
        count: item.media
      }))
    } else {
      uploadTrendData.value = []
    }

    // 处理媒体类型分布
    const typeNameMap: Record<string, string> = {
      'video': '视频',
      'image': '图片',
      'audio': '音频',
      'pdf': 'PDF'
    }
    
    if (data.media_by_type && data.media_by_type.length > 0) {
      mediaTypeData.value = data.media_by_type.map((item: any) => ({
        type: typeNameMap[item.media_type] || item.media_type,
        count: item.count
      }))
    } else {
      mediaTypeData.value = []
    }
  } catch (error) {
    console.error('加载仪表板数据失败:', error)
    // 保持默认值，不生成模拟数据
  }
})
</script>

<style scoped lang="scss">
.dashboard-container {
  padding: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  :deep(.el-card__body) {
    padding: 20px;
  }
}

.stat-content {
  display: flex;
  gap: 16px;
  align-items: center;
}

.stat-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  flex-shrink: 0;
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 12px;
  color: #e6a23c;
  display: flex;
  align-items: center;
  gap: 4px;
  
  &.success { color: #67c23a; }
  &.danger { color: #f56c6c; }
}

.quick-actions {
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;

  .el-button {
    flex: 1;
    min-width: 140px;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.system-status {
  .status-item {
    margin-bottom: 24px;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  .status-label {
    font-size: 14px;
    color: #606266;
    margin-bottom: 8px;
    display: block;
  }
}

[data-theme='dark'] {
  .stat-value {
    color: #ffffff;
  }

  .stat-label {
    color: #909399;
  }
}
</style>

