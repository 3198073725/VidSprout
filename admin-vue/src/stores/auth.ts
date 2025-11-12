import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import http from '@/api/http'
import type { UserProfile } from '@/api/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string>(localStorage.getItem('admin_token') || '')
  const profile = ref<UserProfile | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => {
    if (!profile.value) return false
    return profile.value.is_superuser || profile.value.is_staff || 
           profile.value.is_manager || profile.value.is_editor || false
  })

  // 登录
  async function login(username: string, password: string) {
    // MediaCMS 登录 API 使用 FormData
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    
    const response: any = await http.post('/v1/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // 保存 token
    token.value = response.token
    localStorage.setItem('admin_token', token.value)
    http.defaults.headers.common['Authorization'] = `Token ${token.value}`
    
    // 获取完整的用户信息
    await loadProfile()
    
    return response
  }

  // 登出
  function logout() {
    token.value = ''
    profile.value = null
    localStorage.removeItem('admin_token')
    delete http.defaults.headers.common['Authorization']
  }

  // 加载用户信息
  async function loadProfile() {
    if (!token.value) return
    
    try {
      const response = await http.get('/v1/admin/whoami')
      profile.value = response as UserProfile
    } catch (error) {
      logout()
      throw error
    }
  }

  // 初始化
  if (token.value) {
    http.defaults.headers.common['Authorization'] = `Token ${token.value}`
    loadProfile()
  }

  return {
    token,
    profile,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    loadProfile
  }
})

