<script setup lang="ts">
/* eslint-disable vue/multi-word-component-names */
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createUser } from '@/api/users'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const form = ref({ username: '', password: '', email: '', name: '' })
const loading = ref(false)

async function onSubmit() {
  if (!form.value.username) {
    ElMessage.error('请输入用户名')
    return
  }
  if (!form.value.password) {
    ElMessage.error('请输入密码')
    return
  }
  
  loading.value = true
  try {
    // 注册用户，后端会返回 token
    const result = await createUser({
      username: form.value.username,
      password: form.value.password,
      email: form.value.email || undefined,
      name: form.value.name || undefined,
    })
    
    console.log('注册成功，返回数据:', result)
    
    // 使用返回的 token 自动登录
    if (result && typeof result === 'object' && 'token' in result) {
      // 保存 token
      authStore.token = result.token as string
      localStorage.setItem('token', result.token as string)
      localStorage.setItem('rememberMe', 'true')
      
      // 获取用户信息
      await authStore.fetchProfile()
      
      const displayName = ('name' in result ? result.name : '') || ('username' in result ? result.username : '新用户')
      ElMessage.success(`欢迎，${displayName}！注册成功`)
      
      // 跳转到首页
      router.push('/')
    } else {
      // 如果没有返回 token，跳转到登录页
      ElMessage.success('注册成功！请使用用户名和密码登录')
      router.push('/login')
    }
  } catch (error: unknown) {
    console.error('Register error:', error)
    // 类型保护：检查是否是 Axios 错误
    const e = error as { response?: { data?: Record<string, unknown>; status?: number } }
    const errorData = e?.response?.data
    const status = e?.response?.status
    
    // 处理后端返回的错误信息
    if (status === 403) {
      ElMessage.warning('注册功能需要管理员开启，请联系管理员创建账户')
    } else if (errorData?.username) {
      ElMessage.error('用户名已存在，请使用其他用户名')
    } else if (errorData?.email) {
      ElMessage.error('邮箱已被使用，请使用其他邮箱')
    } else if (errorData?.password) {
      ElMessage.error('密码不符合要求，请检查密码强度')
    } else if (errorData?.detail) {
      ElMessage.error(`注册失败：${errorData.detail}`)
    } else if (status === 500) {
      ElMessage.error('服务器错误，请稍后重试或联系管理员')
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="user-action-form-wrap">
    <div class="user-action-form-inner">
      <h1>注册</h1>
      <p>已经有账户？请 <router-link to="/login">登录</router-link>。</p>
      <el-form :model="form" @submit.prevent label-position="top">
        <el-form-item label="电子邮件:">
          <el-input v-model="form.email" placeholder="Email地址" />
        </el-form-item>
        <el-form-item label="用户名:">
          <el-input v-model="form.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item label="姓名:">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="密码:">
          <el-input v-model="form.password" type="password" placeholder="密码" show-password />
        </el-form-item>
        <ul style="margin: 16px 0; padding-left: 20px; font-size: 14px; color: #666">
          <li>你的密码不能与你的其他个人信息太相似。</li>
          <li>你的密码必须包含至少 7 个字符。</li>
          <li>你的密码不能是一个常见密码。</li>
        </ul>
        <el-form-item>
          <el-button type="success" :loading="loading" :disabled="!form.username || !form.password" @click="onSubmit" style="padding: 12px 32px">注册 &raquo;</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
