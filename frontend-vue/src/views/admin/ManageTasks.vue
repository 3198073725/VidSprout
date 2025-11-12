<template>
  <div class="manage-tasks">
    <div class="header">
      <h1>任务管理</h1>
      <p class="description">实时监控Celery后台任务状态</p>
    </div>

    <!-- 操作工具栏 -->
    <el-card class="toolbar-card" shadow="never">
      <div class="toolbar">
        <el-button type="primary" @click="loadTasks" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <div class="auto-refresh">
          <el-switch 
            v-model="autoRefresh" 
            active-text="自动刷新" 
            @change="handleAutoRefreshChange"
          />
          <span v-if="autoRefresh" class="refresh-interval">
            (每{{ refreshInterval / 1000 }}秒)
          </span>
        </div>
      </div>
    </el-card>

    <!-- 任务统计卡片 -->
    <el-row :gutter="16" class="stats-row">
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card active">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><VideoPlay /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ tasksStats.active }}</div>
              <div class="stat-label">活动任务</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card reserved">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ tasksStats.reserved }}</div>
              <div class="stat-label">保留任务</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="8">
        <el-card shadow="hover" class="stat-card scheduled">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon><Timer /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ tasksStats.scheduled }}</div>
              <div class="stat-label">计划任务</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 活动任务 -->
    <el-card v-if="tasksData.active.tasks.length > 0" class="tasks-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon color="#10b981"><VideoPlay /></el-icon>
            活动任务
          </span>
          <el-tag type="success" size="small">{{ tasksData.active.tasks.length }}</el-tag>
        </div>
      </template>
      <el-table :data="tasksData.active.tasks" style="width: 100%">
        <el-table-column label="序号" type="index" width="60" />
        
        <el-table-column label="任务名称" min-width="150">
          <template #default="{ row }">
            <el-tag :type="getTaskTypeTag(row.name)">{{ row.name }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="任务ID" min-width="180">
          <template #default="{ row }">
            <code class="task-id">{{ row.task_id }}</code>
          </template>
        </el-table-column>

        <el-table-column label="Worker" width="150">
          <template #default="{ row }">
            <span class="worker-name">{{ getWorkerName(row.worker) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="媒体信息" min-width="200" v-if="hasMediaInfo(tasksData.active.tasks)">
          <template #default="{ row }">
            <div v-if="row.info" class="media-info">
              <div v-if="row.info['media title']" class="info-item">
                <el-icon><VideoCamera /></el-icon>
                <span>{{ row.info['media title'] }}</span>
              </div>
              <div v-if="row.info['profile name']" class="info-item profile">
                <el-icon><Setting /></el-icon>
                <span>{{ row.info['profile name'] }}</span>
              </div>
            </div>
            <span v-else class="no-info">-</span>
          </template>
        </el-table-column>

        <el-table-column label="进度" width="120" v-if="hasProgress(tasksData.active.tasks)">
          <template #default="{ row }">
            <div v-if="row.info && row.info['encoding progress'] !== undefined" class="progress-wrapper">
              <el-progress 
                :percentage="row.info['encoding progress']" 
                :color="getProgressColor(row.info['encoding progress'])"
                :stroke-width="8"
              />
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>

        <el-table-column label="开始时间" width="160">
          <template #default="{ row }">
            {{ formatTimestamp(row.time_start) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 保留任务 -->
    <el-card v-if="tasksData.reserved.tasks.length > 0" class="tasks-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon color="#f59e0b"><Clock /></el-icon>
            保留任务
          </span>
          <el-tag type="warning" size="small">{{ tasksData.reserved.tasks.length }}</el-tag>
        </div>
      </template>
      <el-table :data="tasksData.reserved.tasks" style="width: 100%">
        <el-table-column label="序号" type="index" width="60" />
        
        <el-table-column label="任务名称" min-width="150">
          <template #default="{ row }">
            <el-tag :type="getTaskTypeTag(row.name)">{{ row.name }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="任务ID" min-width="180">
          <template #default="{ row }">
            <code class="task-id">{{ row.task_id }}</code>
          </template>
        </el-table-column>

        <el-table-column label="Worker" width="150">
          <template #default="{ row }">
            <span class="worker-name">{{ getWorkerName(row.worker) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="媒体信息" min-width="200" v-if="hasMediaInfo(tasksData.reserved.tasks)">
          <template #default="{ row }">
            <div v-if="row.info" class="media-info">
              <div v-if="row.info['media title']" class="info-item">
                <el-icon><VideoCamera /></el-icon>
                <span>{{ row.info['media title'] }}</span>
              </div>
              <div v-if="row.info['profile name']" class="info-item profile">
                <el-icon><Setting /></el-icon>
                <span>{{ row.info['profile name'] }}</span>
              </div>
            </div>
            <span v-else class="no-info">-</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 计划任务 -->
    <el-card v-if="tasksData.scheduled.tasks.length > 0" class="tasks-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="header-title">
            <el-icon color="#6b7280"><Timer /></el-icon>
            计划任务
          </span>
          <el-tag type="info" size="small">{{ tasksData.scheduled.tasks.length }}</el-tag>
        </div>
      </template>
      <el-table :data="tasksData.scheduled.tasks" style="width: 100%">
        <el-table-column label="序号" type="index" width="60" />
        
        <el-table-column label="任务名称" min-width="150">
          <template #default="{ row }">
            <el-tag :type="getTaskTypeTag(row.name)">{{ row.name }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="任务ID" min-width="180">
          <template #default="{ row }">
            <code class="task-id">{{ row.task_id }}</code>
          </template>
        </el-table-column>

        <el-table-column label="Worker" width="150">
          <template #default="{ row }">
            <span class="worker-name">{{ getWorkerName(row.worker) }}</span>
          </template>
        </el-table-column>

        <el-table-column label="媒体信息" min-width="200" v-if="hasMediaInfo(tasksData.scheduled.tasks)">
          <template #default="{ row }">
            <div v-if="row.info" class="media-info">
              <div v-if="row.info['media title']" class="info-item">
                <el-icon><VideoCamera /></el-icon>
                <span>{{ row.info['media title'] }}</span>
              </div>
              <div v-if="row.info['profile name']" class="info-item profile">
                <el-icon><Setting /></el-icon>
                <span>{{ row.info['profile name'] }}</span>
              </div>
            </div>
            <span v-else class="no-info">-</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 无任务提示 -->
    <el-card v-if="!loading && totalTasks === 0" class="empty-card" shadow="never">
      <el-empty description="当前没有运行中的任务">
        <el-button type="primary" @click="loadTasks">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </el-empty>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Refresh, 
  VideoPlay, 
  Clock, 
  Timer, 
  VideoCamera, 
  Setting 
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import * as AdminAPI from '@/api/admin'
import type { Task } from '@/api/admin'

const router = useRouter()
const auth = useAuthStore()

// 权限检查
const isAdmin = computed(() => {
  const profile = auth.profile as {is_staff?: boolean} | null
  return profile?.is_staff || false
})

// 数据状态
const loading = ref(false)
const tasksData = ref<AdminAPI.TasksResponse>({
  active: { tasks: [] },
  reserved: { tasks: [] },
  scheduled: { tasks: [] },
  task_ids: [],
  media_profile_pairs: []
})

// 自动刷新
const autoRefresh = ref(false)
const refreshInterval = ref(5000) // 5秒
let refreshTimer: number | null = null

// 任务统计
const tasksStats = computed(() => ({
  active: tasksData.value.active.tasks.length,
  reserved: tasksData.value.reserved.tasks.length,
  scheduled: tasksData.value.scheduled.tasks.length
}))

const totalTasks = computed(() => {
  return tasksStats.value.active + tasksStats.value.reserved + tasksStats.value.scheduled
})

// 加载任务列表
async function loadTasks() {
  if (!isAdmin.value) {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
    return
  }

  loading.value = true
  try {
    const response = await AdminAPI.getTasks()
    tasksData.value = response
  } catch (error) {
    console.error('加载任务列表失败:', error)
    ElMessage.error('加载失败，请稍后再试')
  } finally {
    loading.value = false
  }
}

// 处理自动刷新切换
function handleAutoRefreshChange(value: boolean) {
  if (value) {
    startAutoRefresh()
  } else {
    stopAutoRefresh()
  }
}

// 开始自动刷新
function startAutoRefresh() {
  stopAutoRefresh() // 先停止之前的定时器
  refreshTimer = window.setInterval(() => {
    loadTasks()
  }, refreshInterval.value)
}

// 停止自动刷新
function stopAutoRefresh() {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}

// 获取任务类型标签颜色
function getTaskTypeTag(taskName: string): string {
  if (taskName.includes('encode')) return 'primary'
  if (taskName.includes('transcode')) return 'success'
  if (taskName.includes('trim')) return 'warning'
  if (taskName.includes('whisper')) return 'info'
  return 'default'
}

// 获取Worker名称（简化显示）
function getWorkerName(worker: string | undefined): string {
  if (!worker) return '-'
  // worker格式通常是: celery@hostname
  const parts = worker.split('@')
  return parts.length > 1 ? (parts[1] || worker) : worker
}

// 格式化时间戳
function formatTimestamp(timestamp: number | undefined): string {
  if (!timestamp) return '-'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 获取进度条颜色
function getProgressColor(percentage: number): string {
  if (percentage < 30) return '#f56c6c'
  if (percentage < 70) return '#e6a23c'
  return '#67c23a'
}

// 检查是否有媒体信息
function hasMediaInfo(tasks: Task[]): boolean {
  return tasks.some(task => task.info && (task.info['media title'] || task.info['profile name']))
}

// 检查是否有进度信息
function hasProgress(tasks: Task[]): boolean {
  return tasks.some(task => task.info && task.info['encoding progress'] !== undefined)
}

// 初始化和清理
onMounted(() => {
  if (isAdmin.value) {
    loadTasks()
  } else {
    ElMessage.warning('您没有权限访问此页面')
    router.push('/')
  }
})

onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped lang="scss">
.manage-tasks {
  padding: 24px;
  max-width: 1600px;
  margin: 0 auto;

  .header {
    margin-bottom: 24px;

    h1 {
      font-size: 28px;
      font-weight: 600;
      color: #1f2937;
      margin: 0 0 8px 0;
    }

    .description {
      font-size: 14px;
      color: #6b7280;
      margin: 0;
    }
  }

  .toolbar-card {
    margin-bottom: 16px;

    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .auto-refresh {
        display: flex;
        align-items: center;
        gap: 8px;

        .refresh-interval {
          font-size: 13px;
          color: #6b7280;
        }
      }
    }
  }

  .stats-row {
    margin-bottom: 24px;

    .stat-card {
      margin-bottom: 16px;

      .stat-content {
        display: flex;
        align-items: center;
        gap: 16px;

        .stat-icon {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 24px;
        }

        .stat-info {
          flex: 1;

          .stat-value {
            font-size: 32px;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 4px;
          }

          .stat-label {
            font-size: 14px;
            color: #6b7280;
          }
        }
      }

      &.active {
        .stat-icon {
          background-color: #d1fae5;
          color: #10b981;
        }
        .stat-value {
          color: #10b981;
        }
      }

      &.reserved {
        .stat-icon {
          background-color: #fef3c7;
          color: #f59e0b;
        }
        .stat-value {
          color: #f59e0b;
        }
      }

      &.scheduled {
        .stat-icon {
          background-color: #e5e7eb;
          color: #6b7280;
        }
        .stat-value {
          color: #6b7280;
        }
      }
    }
  }

  .tasks-card {
    margin-bottom: 24px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .header-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;
        font-weight: 600;
        color: #1f2937;
      }
    }

    .task-id {
      font-family: 'Courier New', monospace;
      font-size: 12px;
      color: #6b7280;
      background-color: #f3f4f6;
      padding: 2px 6px;
      border-radius: 4px;
    }

    .worker-name {
      font-size: 13px;
      color: #374151;
      font-weight: 500;
    }

    .media-info {
      .info-item {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
        font-size: 13px;
        color: #374151;

        &:last-child {
          margin-bottom: 0;
        }

        &.profile {
          color: #6b7280;
          font-size: 12px;
        }

        .el-icon {
          font-size: 14px;
        }
      }
    }

    .no-info {
      color: #9ca3af;
    }

    .progress-wrapper {
      padding: 0 8px;
    }
  }

  .empty-card {
    margin-top: 48px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .manage-tasks {
    padding: 16px;

    .header h1 {
      font-size: 24px;
    }

    .toolbar-card {
      .toolbar {
        flex-direction: column;
        gap: 12px;
        align-items: stretch;
      }
    }

    .stats-row {
      .stat-card {
        .stat-content {
          .stat-icon {
            width: 40px;
            height: 40px;
            font-size: 20px;
          }

          .stat-info {
            .stat-value {
              font-size: 24px;
            }
          }
        }
      }
    }

    .tasks-card {
      :deep(.el-table) {
        font-size: 12px;

        .task-id {
          font-size: 10px;
        }
      }
    }
  }
}
</style>
