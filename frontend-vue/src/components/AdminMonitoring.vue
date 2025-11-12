<template>
  <div class="admin-monitoring">
    <el-card class="monitoring-card">
      <template #header>
        <div class="card-header">
          <span>系统监控</span>
          <el-tag :type="systemStatus.type">{{ systemStatus.text }}</el-tag>
        </div>
      </template>
      
      <div class="monitoring-content">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="metric-card">
              <div class="metric-header">
                <el-icon><Monitor /></el-icon>
                <span>服务器状态</span>
              </div>
              <div class="metric-value" :class="serverStatus.class">
                {{ serverStatus.value }}%
              </div>
              <div class="metric-label">CPU使用率</div>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="metric-card">
              <div class="metric-header">
                <el-icon><Coin /></el-icon>
                <span>内存使用</span>
              </div>
              <div class="metric-value" :class="memoryStatus.class">
                {{ memoryStatus.value }}%
              </div>
              <div class="metric-label">内存使用率</div>
            </div>
          </el-col>
          
          <el-col :span="8">
            <div class="metric-card">
              <div class="metric-header">
                <el-icon><DataLine /></el-icon>
                <span>磁盘空间</span>
              </div>
              <div class="metric-value" :class="diskStatus.class">
                {{ diskStatus.value }}%
              </div>
              <div class="metric-label">磁盘使用率</div>
            </div>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <div class="alerts-section">
          <div class="section-header">
            <h4>系统告警</h4>
            <el-button size="small" @click="refreshMonitoring">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
          
          <el-alert
            v-for="alert in activeAlerts"
            :key="alert.id"
            :title="alert.title"
            :type="alert.type"
            :description="alert.description"
            :closable="false"
            class="alert-item"
          />
          
          <el-empty
            v-if="activeAlerts.length === 0"
            description="暂无告警信息"
            :image-size="60"
          />
        </div>
        
        <el-divider />
        
        <div class="performance-section">
          <div class="section-header">
            <h4>性能指标</h4>
            <el-select v-model="timeRange" size="small" style="width: 120px">
              <el-option label="最近1小时" value="1h" />
              <el-option label="最近6小时" value="6h" />
              <el-option label="最近24小时" value="24h" />
              <el-option label="最近7天" value="7d" />
            </el-select>
          </div>
          
          <div class="chart-container">
            <canvas ref="performanceChart"></canvas>
          </div>
        </div>
      </div>
    </el-card>
    
    <!-- 告警设置对话框 -->
    <el-dialog
      v-model="alertSettings.visible"
      title="告警设置"
      width="600px"
    >
      <el-form :model="alertSettings.form" label-width="120px">
        <el-form-item label="CPU阈值">
          <el-slider
            v-model="alertSettings.form.cpuThreshold"
            :min="50"
            :max="100"
            :step="5"
            show-input
          />
        </el-form-item>
        
        <el-form-item label="内存阈值">
          <el-slider
            v-model="alertSettings.form.memoryThreshold"
            :min="50"
            :max="100"
            :step="5"
            show-input
          />
        </el-form-item>
        
        <el-form-item label="磁盘阈值">
          <el-slider
            v-model="alertSettings.form.diskThreshold"
            :min="70"
            :max="100"
            :step="5"
            show-input
          />
        </el-form-item>
        
        <el-form-item label="告警通知">
          <el-switch v-model="alertSettings.form.enableNotifications" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="alertSettings.visible = false">取消</el-button>
        <el-button type="primary" @click="saveAlertSettings">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Monitor, Coin, DataLine, Refresh, Setting } from '@element-plus/icons-vue'
import Chart from 'chart.js/auto'
import { AdminAPI } from '@/api'

interface MetricStatus {
  value: number
  class: string
}

interface SystemAlert {
  id: string
  title: string
  type: 'success' | 'warning' | 'error' | 'info'
  description: string
  timestamp: number
}

interface PerformanceData {
  timestamp: number
  cpu: number
  memory: number
  disk: number
  requests: number
}

const systemStatus = ref({
  type: 'success' as 'success' | 'warning' | 'error',
  text: '系统正常运行'
})

const serverStatus = ref<MetricStatus>({
  value: 0,
  class: 'status-normal'
})

const memoryStatus = ref<MetricStatus>({
  value: 0,
  class: 'status-normal'
})

const diskStatus = ref<MetricStatus>({
  value: 0,
  class: 'status-normal'
})

const activeAlerts = ref<SystemAlert[]>([])
const timeRange = ref('1h')
const performanceChart = ref<HTMLCanvasElement>()
let performanceChartInstance: Chart | null = null

const alertSettings = ref({
  visible: false,
  form: {
    cpuThreshold: 80,
    memoryThreshold: 85,
    diskThreshold: 90,
    enableNotifications: true
  }
})

// 模拟监控数据
const performanceData = ref<PerformanceData[]>([])

// 生成模拟数据
function generateMockData() {
  const now = Date.now()
  const data: PerformanceData[] = []
  
  for (let i = 0; i < 60; i++) {
    data.push({
      timestamp: now - (59 - i) * 60000, // 每分钟一个数据点
      cpu: Math.random() * 30 + 20, // 20-50%
      memory: Math.random() * 20 + 40, // 40-60%
      disk: Math.random() * 10 + 60, // 60-70%
      requests: Math.random() * 100 + 50 // 50-150 requests/min
    })
  }
  
  return data
}

// 更新系统状态
function updateSystemStatus() {
  const cpu = serverStatus.value.value
  const memory = memoryStatus.value.value
  const disk = diskStatus.value.value
  
  if (cpu > alertSettings.value.form.cpuThreshold || 
      memory > alertSettings.value.form.memoryThreshold || 
      disk > alertSettings.value.form.diskThreshold) {
    systemStatus.value = {
      type: 'error',
      text: '系统负载过高'
    }
  } else if (cpu > 60 || memory > 70 || disk > 80) {
    systemStatus.value = {
      type: 'warning',
      text: '系统负载较高'
    }
  } else {
    systemStatus.value = {
      type: 'success',
      text: '系统正常运行'
    }
  }
}

// 检查告警
function checkAlerts() {
  const alerts: SystemAlert[] = []
  
  if (serverStatus.value.value > alertSettings.value.form.cpuThreshold) {
    alerts.push({
      id: 'cpu-high',
      title: 'CPU使用率过高',
      type: 'error',
      description: `CPU使用率达到 ${serverStatus.value.value}%，超过阈值 ${alertSettings.value.form.cpuThreshold}%`,
      timestamp: Date.now()
    })
  }
  
  if (memoryStatus.value.value > alertSettings.value.form.memoryThreshold) {
    alerts.push({
      id: 'memory-high',
      title: '内存使用率过高',
      type: 'error',
      description: `内存使用率达到 ${memoryStatus.value.value}%，超过阈值 ${alertSettings.value.form.memoryThreshold}%`,
      timestamp: Date.now()
    })
  }
  
  if (diskStatus.value.value > alertSettings.value.form.diskThreshold) {
    alerts.push({
      id: 'disk-high',
      title: '磁盘使用率过高',
      type: 'warning',
      description: `磁盘使用率达到 ${diskStatus.value.value}%，超过阈值 ${alertSettings.value.form.diskThreshold}%`,
      timestamp: Date.now()
    })
  }
  
  activeAlerts.value = alerts
}

// 刷新监控数据
async function refreshMonitoring() {
  try {
    // 获取系统监控数据
    const monitoringData = await AdminAPI.getSystemMonitoring()
    
    // 更新系统指标
    serverStatus.value = {
      value: Math.round(monitoringData.system.cpu_percent),
      class: monitoringData.system.cpu_percent > 80 ? 'status-error' :
             monitoringData.system.cpu_percent > 60 ? 'status-warning' : 'status-normal'
    }
    
    memoryStatus.value = {
      value: Math.round(monitoringData.system.memory_percent),
      class: monitoringData.system.memory_percent > 85 ? 'status-error' :
             monitoringData.system.memory_percent > 70 ? 'status-warning' : 'status-normal'
    }
    
    diskStatus.value = {
      value: Math.round(monitoringData.system.disk_percent),
      class: monitoringData.system.disk_percent > 90 ? 'status-error' :
             monitoringData.system.disk_percent > 80 ? 'status-warning' : 'status-normal'
    }
    
    // 更新性能数据
    if (monitoringData.history && monitoringData.history.length > 0) {
      performanceData.value = monitoringData.history.map((item: any) => ({
        timestamp: new Date(item.timestamp).getTime(),
        cpu: item.cpu,
        memory: item.memory,
        disk: item.disk,
        requests: Math.random() * 100 + 50 // 模拟请求数
      }))
    } else {
      // 如果没有历史数据，使用模拟数据
      performanceData.value = generateMockData()
    }
    
    updateSystemStatus()
    checkAlerts()
    
    // 更新图表
    updatePerformanceChart()
    
    ElMessage.success('监控数据已刷新')
  } catch (error) {
    console.error('获取监控数据失败:', error)
    // 使用模拟数据作为后备
    const mockData = generateMockData()
    performanceData.value = mockData
    
    const latest = mockData[mockData.length - 1]
    if (latest) {
      serverStatus.value = {
        value: Math.round(latest.cpu),
        class: latest.cpu > 80 ? 'status-error' : latest.cpu > 60 ? 'status-warning' : 'status-normal'
      }
      
      memoryStatus.value = {
        value: Math.round(latest.memory),
        class: latest.memory > 85 ? 'status-error' : latest.memory > 70 ? 'status-warning' : 'status-normal'
      }
      
      diskStatus.value = {
        value: Math.round(latest.disk),
        class: latest.disk > 90 ? 'status-error' : latest.disk > 80 ? 'status-warning' : 'status-normal'
      }
    }
    
    updateSystemStatus()
    checkAlerts()
    updatePerformanceChart()
    
    ElMessage.warning('使用模拟数据，请检查API连接')
  }
}

// 更新性能图表
async function updatePerformanceChart() {
  await nextTick()
  
  if (!performanceChart.value) return
  
  const ctx = performanceChart.value.getContext('2d')
  if (!ctx) return
  
  // 销毁现有图表
  if (performanceChartInstance) {
    performanceChartInstance.destroy()
    performanceChartInstance = null
  }
  
  // 创建新图表
  performanceChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: performanceData.value.map(d => new Date(d.timestamp).toLocaleTimeString()),
      datasets: [
        {
          label: 'CPU使用率 (%)',
          data: performanceData.value.map(d => d.cpu),
          borderColor: '#409EFF',
          backgroundColor: 'rgba(64, 158, 255, 0.1)',
          tension: 0.4,
          yAxisID: 'y'
        },
        {
          label: '内存使用率 (%)',
          data: performanceData.value.map(d => d.memory),
          borderColor: '#67C23A',
          backgroundColor: 'rgba(103, 194, 58, 0.1)',
          tension: 0.4,
          yAxisID: 'y'
        },
        {
          label: '请求数 (/min)',
          data: performanceData.value.map(d => d.requests),
          borderColor: '#E6A23C',
          backgroundColor: 'rgba(230, 162, 60, 0.1)',
          tension: 0.4,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      scales: {
        x: {
          display: true,
          title: {
            display: true,
            text: '时间'
          }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: '使用率 (%)'
          },
          min: 0,
          max: 100
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: '请求数'
          },
          grid: {
            drawOnChartArea: false,
          },
          min: 0
        }
      }
    }
  })
}

// 保存告警设置
async function saveAlertSettings() {
  try {
    // 保存到后端
    await AdminAPI.updateAlertRules({
      cpu_threshold: alertSettings.value.form.cpuThreshold,
      memory_threshold: alertSettings.value.form.memoryThreshold,
      disk_threshold: alertSettings.value.form.diskThreshold,
      network_threshold: 80, // 默认值
      enable_notifications: alertSettings.value.form.enableNotifications,
      notification_email: '' // 可以从用户信息获取
    })
    
    // 同时保存到本地存储
    localStorage.setItem('adminAlertSettings', JSON.stringify(alertSettings.value.form))
    alertSettings.value.visible = false
    ElMessage.success('告警设置已保存')
    
    // 重新检查告警
    checkAlerts()
  } catch (error) {
    console.error('保存告警设置失败:', error)
    ElMessage.error('保存告警设置失败')
  }
}

// 加载告警设置
async function loadAlertSettings() {
  try {
    // 从后端获取告警规则
    const rules = await AdminAPI.getAlertRules()
    alertSettings.value.form = {
      cpuThreshold: rules.cpu_threshold,
      memoryThreshold: rules.memory_threshold,
      diskThreshold: rules.disk_threshold,
      enableNotifications: rules.enable_notifications
    }
  } catch (error) {
    console.error('从后端加载告警设置失败:', error)
    // 回退到本地存储
    const saved = localStorage.getItem('adminAlertSettings')
    if (saved) {
      try {
        const settings = JSON.parse(saved)
        alertSettings.value.form = { ...alertSettings.value.form, ...settings }
      } catch (error) {
        console.error('加载本地告警设置失败:', error)
      }
    }
  }
}

// 定时刷新
let refreshInterval: number | null = null

onMounted(() => {
  loadAlertSettings()
  refreshMonitoring()
  
  // 每30秒自动刷新
  refreshInterval = window.setInterval(() => {
    refreshMonitoring()
  }, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
  
  if (performanceChartInstance) {
    performanceChartInstance.destroy()
    performanceChartInstance = null
  }
})

watch(timeRange, () => {
  // 根据时间范围重新获取数据
  refreshMonitoring()
})
</script>

<style scoped>
.admin-monitoring {
  padding: 20px;
}

.monitoring-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.monitoring-content {
  padding: 20px 0;
}

.metric-card {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.metric-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #909399;
}

.metric-value {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 12px;
  color: #909399;
}

.status-normal {
  color: #67c23a;
}

.status-warning {
  color: #e6a23c;
}

.status-error {
  color: #f56c6c;
}

.alerts-section {
  margin-top: 30px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h4 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.alert-item {
  margin-bottom: 12px;
}

.performance-section {
  margin-top: 30px;
}

.chart-container {
  height: 300px;
  position: relative;
}

.el-divider {
  margin: 24px 0;
}
</style>