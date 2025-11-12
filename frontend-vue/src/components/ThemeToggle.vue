<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Moon, Sunny } from '@element-plus/icons-vue'

const theme = ref<'light' | 'dark'>('light')

onMounted(() => {
  // 从 localStorage 加载主题
  const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
  if (savedTheme) {
    theme.value = savedTheme
    applyTheme(savedTheme)
  } else {
    // 检测系统主题
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    theme.value = prefersDark ? 'dark' : 'light'
    applyTheme(theme.value)
  }
})

function toggleTheme() {
  theme.value = theme.value === 'light' ? 'dark' : 'light'
  applyTheme(theme.value)
  localStorage.setItem('theme', theme.value)
}

function applyTheme(newTheme: 'light' | 'dark') {
  document.documentElement.setAttribute('data-theme', newTheme)
  
  // 设置 CSS 变量
  if (newTheme === 'dark') {
    // 暗色模式
    document.body.style.backgroundColor = '#1a1a1a'
    document.body.style.color = '#ffffff'
    
    document.documentElement.style.setProperty('--mc-bg-primary', '#1a1a1a')
    document.documentElement.style.setProperty('--mc-bg-secondary', '#2a2a2a')
    document.documentElement.style.setProperty('--mc-text-primary', '#ffffff')
    document.documentElement.style.setProperty('--mc-text-secondary', '#cccccc')
    document.documentElement.style.setProperty('--mc-border-color', '#404040')
    
    // Element Plus 暗色模式
    document.documentElement.classList.add('dark')
    
    // 追加更多样式
    document.documentElement.style.setProperty('--el-bg-color', '#1a1a1a')
    document.documentElement.style.setProperty('--el-bg-color-page', '#0a0a0a')
    document.documentElement.style.setProperty('--el-text-color-primary', '#ffffff')
    document.documentElement.style.setProperty('--el-text-color-regular', '#cccccc')
    document.documentElement.style.setProperty('--el-border-color', '#404040')
  } else {
    // 亮色模式
    document.body.style.backgroundColor = '#ffffff'
    document.body.style.color = '#333333'
    
    document.documentElement.style.setProperty('--mc-bg-primary', '#ffffff')
    document.documentElement.style.setProperty('--mc-bg-secondary', '#f5f5f5')
    document.documentElement.style.setProperty('--mc-text-primary', '#333333')
    document.documentElement.style.setProperty('--mc-text-secondary', '#666666')
    document.documentElement.style.setProperty('--mc-border-color', '#e0e0e0')
    
    // 移除暗色模式
    document.documentElement.classList.remove('dark')
    
    // 重置 Element Plus 样式
    document.documentElement.style.removeProperty('--el-bg-color')
    document.documentElement.style.removeProperty('--el-bg-color-page')
    document.documentElement.style.removeProperty('--el-text-color-primary')
    document.documentElement.style.removeProperty('--el-text-color-regular')
    document.documentElement.style.removeProperty('--el-border-color')
  }
}
</script>

<template>
  <el-button 
    circle 
    @click="toggleTheme"
    :title="theme === 'light' ? '切换到暗色模式' : '切换到亮色模式'"
  >
    <el-icon v-if="theme === 'light'"><Moon /></el-icon>
    <el-icon v-else><Sunny /></el-icon>
  </el-button>
</template>

<style scoped>
.el-button {
  transition: all 0.3s ease;
}
</style>
