<template>
  <div class="login-status-container">
    <el-dropdown trigger="click" @command="handleCommand">
      <div class="user-info">
        <el-avatar :size="32" :src="auth.profile?.thumbnail_url" class="user-avatar">
          <el-icon><User /></el-icon>
        </el-avatar>
        <span class="username">{{ auth.profile?.name || auth.profile?.username }}</span>
        <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
      </div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="profile">
            <el-icon><User /></el-icon>
            个人资料
          </el-dropdown-item>
          <el-dropdown-item command="devices" divided>
            <el-icon><Monitor /></el-icon>
            设备管理
          </el-dropdown-item>
          <el-dropdown-item command="settings">
            <el-icon><Setting /></el-icon>
            账号设置
          </el-dropdown-item>
          <el-dropdown-item command="logout" divided>
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>

    <!-- 设备管理对话框 -->
    <el-dialog
      v-model="devicesDialogVisible"
      title="设备管理"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="devices-list">
        <el-alert
          v-if="auth.rememberMe"
          title="已启用自动登录"
          type="info"
          :closable="false"
          class="remember-me-alert"
        >
          您的账号已启用自动登录功能，可以在多个设备上保持登录状态。
        </el-alert>
        
        <div v-if="devices.length === 0" class="no-devices">
          <el-empty description="暂无设备信息" />
        </div>
        
        <div v-else class="device-items">
          <div v-for="device in devices" :key="device.id" class="device-item">
            <div class="device-info">
              <el-icon class="device-icon">
                <Monitor v-if="device.device_type === 'desktop'" />
                <Iphone v-else-if="device.device_type === 'mobile'" />
                <Monitor v-else />
              </el-icon>
              <div class="device-details">
                <div class="device-name">{{ getDeviceName(device) }}</div>
                <div class="device-meta">
                  {{ device.login_time }} · {{ device.ip_address }}
                </div>
              </div>
            </div>
            <el-button
              type="danger"
              size="small"
              link
              @click="revokeDevice(device.id)"
            >
              移除
            </el-button>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="devicesDialogVisible = false">关闭</el-button>
          <el-button type="danger" @click="revokeAllDevices">
            移除所有设备
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Device } from '@/api/types'
import {
  User,
  ArrowDown,
  Monitor,
  Iphone,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const auth = useAuthStore()

const devicesDialogVisible = ref(false)
const devices = ref<Device[]>([])

// 获取设备名称
const getDeviceName = (device: Device) => {
  const deviceTypeMap = {
    desktop: '电脑',
    mobile: '手机',
    tablet: '平板'
  }
  return `${deviceTypeMap[device.device_type] || '未知设备'} - ${device.user_agent?.slice(0, 50) || '未知浏览器'}`
}

// 处理菜单命令
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push(`/user/${auth.profile?.username}`)
      break
    case 'devices':
      showDevicesDialog()
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 显示设备管理对话框
const showDevicesDialog = async () => {
  devicesDialogVisible.value = true
  // 这里可以加载用户的设备信息
  // await loadDevices()
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？这将清除所有设备的自动登录状态。',
      '确认退出',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    auth.logout()
    ElMessage.success('已退出登录')
    router.push('/')
  } catch {
    // 用户取消
  }
}

// 移除设备
const revokeDevice = async (deviceId: string) => {
  try {
    await ElMessageBox.confirm(
      '确定要移除这个设备的登录状态吗？',
      '确认移除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里调用API移除设备
    // await revokeDeviceAPI(deviceId)
    ElMessage.success('设备已移除')
  } catch {
    // 用户取消
  }
}

// 移除所有设备
const revokeAllDevices = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要移除所有设备的登录状态吗？您需要重新登录。',
      '确认移除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 这里调用API移除所有设备
    // await revokeAllDevicesAPI()
    ElMessage.success('所有设备已移除')
    devicesDialogVisible.value = false
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.login-status-container {
  display: inline-block;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: var(--el-fill-color-light);
}

.user-avatar {
  margin-right: 8px;
}

.username {
  margin-right: 4px;
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.dropdown-icon {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.remember-me-alert {
  margin-bottom: 16px;
}

.devices-list {
  max-height: 400px;
  overflow-y: auto;
}

.device-items {
  border: 1px solid var(--el-border-color-lighter);
  border-radius: 6px;
  overflow: hidden;
}

.device-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid var(--el-border-color-lighter);
}

.device-item:last-child {
  border-bottom: none;
}

.device-info {
  display: flex;
  align-items: center;
  flex: 1;
}

.device-icon {
  font-size: 24px;
  color: var(--el-color-primary);
  margin-right: 12px;
}

.device-details {
  flex: 1;
}

.device-name {
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.device-meta {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.no-devices {
  padding: 40px 0;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
}
</style>