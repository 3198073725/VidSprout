import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
  const sidebarCollapsed = ref(false)
  const size = ref<'default' | 'small' | 'large'>('default')
  const theme = ref<'light' | 'dark'>('light')

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function setSidebarCollapsed(value: boolean) {
    sidebarCollapsed.value = value
  }

  function setSize(newSize: 'default' | 'small' | 'large') {
    size.value = newSize
  }

  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    document.documentElement.classList.toggle('dark')
    document.documentElement.setAttribute('data-theme', theme.value)
  }

  return {
    sidebarCollapsed,
    size,
    theme,
    toggleSidebar,
    setSidebarCollapsed,
    setSize,
    toggleTheme
  }
})

