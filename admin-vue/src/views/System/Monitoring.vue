<template>
  <div class="monitoring-container">
    <!-- 系统状态概览 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #409eff20; color: #409eff;">
              <el-icon :size="28"><Cpu /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">CPU 使用率</div>
              <div class="stat-value">{{ systemInfo.cpu }}%</div>
              <el-progress 
                :percentage="systemInfo.cpu" 
                :color="getStatusColor(systemInfo.cpu)"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #67c23a20; color: #67c23a;">
              <el-icon :size="28"><Memo /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">内存使用率</div>
              <div class="stat-value">{{ systemInfo.memory }}%</div>
              <el-progress 
                :percentage="systemInfo.memory" 
                :color="getStatusColor(systemInfo.memory)"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #e6a23c20; color: #e6a23c;">
              <el-icon :size="28"><FolderOpened /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">磁盘使用率</div>
              <div class="stat-value">{{ systemInfo.disk }}%</div>
              <el-progress 
                :percentage="systemInfo.disk" 
                :color="getStatusColor(systemInfo.disk)"
                :show-text="false"
              />
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :lg="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: #f56c6c20; color: #f56c6c;">
              <el-icon><Connection /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">网络流量</div>
              <div class="stat-value">{{ systemInfo.network }} MB</div>
              <div class="network-detail">
                <span>↑ {{ systemInfo.uploadSpeed }} MB</span>
                <span>↓ {{ systemInfo.downloadSpeed }} MB</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详细信息 -->
    <el-row :gutter="20">
      <el-col :xs="24" :lg="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统资源趋势</span>
              <div>
                <el-tag size="small" type="info" style="margin-right: 10px">
                  每5秒自动刷新
                </el-tag>
                <el-button size="small" @click="loadMonitoringData">
                  <el-icon><RefreshRight /></el-icon>
                  手动刷新
                </el-button>
              </div>
            </div>
          </template>
          <LineChart :data="trendData" height="350px" title="" />
        </el-card>
      </el-col>

      <el-col :xs="24" :lg="8">
        <el-card>
          <template #header>
            <span>系统信息</span>
          </template>
          <el-descriptions :column="1" border>
            <el-descriptions-item label="操作系统">
              {{ systemDetails.os }}
            </el-descriptions-item>
            <el-descriptions-item label="主机名">
              {{ systemDetails.hostname }}
            </el-descriptions-item>
            <el-descriptions-item label="Python 版本">
              {{ systemDetails.pythonVersion }}
            </el-descriptions-item>
            <el-descriptions-item label="Django 版本">
              {{ systemDetails.djangoVersion }}
            </el-descriptions-item>
            <el-descriptions-item label="运行时间">
              {{ systemDetails.uptime }}
            </el-descriptions-item>
            <el-descriptions-item label="数据库">
              {{ systemDetails.database }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <!-- 进程信息 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>运行中的进程（Top 10）</span>
              <el-button size="small" @click="loadMonitoringData">
                <el-icon><RefreshRight /></el-icon>
                刷新
              </el-button>
            </div>
          </template>
          <el-table :data="processes" style="width: 100%">
            <el-table-column prop="pid" label="PID" width="80" />
            <el-table-column prop="name" label="进程名称" min-width="200" />
            <el-table-column prop="cpu" label="CPU" width="100">
              <template #default="{ row }">
                {{ row.cpu }}%
              </template>
            </el-table-column>
            <el-table-column prop="memory" label="内存" width="100">
              <template #default="{ row }">
                {{ row.memory }}%
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status === 'running' ? 'success' : 'info'" size="small">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import LineChart from '@/components/charts/LineChart.vue'
import { getMonitoring, type SystemMonitoring } from '@/api/system'

const systemInfo = ref({
  cpu: 0,
  memory: 0,
  disk: 0,
  network: 0,
  uploadSpeed: 0,
  downloadSpeed: 0
})

const systemDetails = ref({
  os: '加载中...',
  hostname: '加载中...',
  pythonVersion: '加载中...',
  djangoVersion: '加载中...',
  uptime: '加载中...',
  database: '加载中...'
})

const trendData = ref<Array<{ date: string; count: number }>>([])

const processes = ref<Array<{
  pid: number
  name: string
  cpu: number
  memory: number
  status: string
}>>([])

let refreshTimer: number | null = null

const getStatusColor = (value: number) => {
  if (value < 60) return '#67c23a'
  if (value < 80) return '#e6a23c'
  return '#f56c6c'
}

const loadMonitoringData = async () => {
  try {
    console.log('📊 加载系统监控数据...')
    
    const data = await getMonitoring()
    
    console.log('✅ 系统监控数据加载成功:', data)
    
    // 更新系统信息
    systemInfo.value = data.systemInfo
    systemDetails.value = data.systemDetails
    processes.value = data.processes
    trendData.value = data.trendData
    
  } catch (error) {
    console.error('❌ 加载监控数据失败:', error)
    ElMessage.error('加载监控数据失败')
  }
}

onMounted(() => {
  // 首次加载
  loadMonitoringData()
  
  // 每5秒刷新一次
  refreshTimer = window.setInterval(() => {
    loadMonitoringData()
  }, 5000)
  
  console.log('✅ 系统监控已启动，每5秒自动刷新')
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    console.log('✅ 系统监控已停止')
  }
})
</script>

<style scoped lang="scss">
.monitoring-container {
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
  width: 56px;
  height: 56px;
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
  font-size: 13px;
  color: #909399;
  margin-bottom: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.network-detail {
  display: flex;
  gap: 16px;
  font-size: 12px;
  color: #606266;
  margin-top: 4px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

[data-theme='dark'] {
  .stat-value {
    color: #ffffff;
  }
}
</style>
