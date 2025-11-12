<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Message, Location } from '@element-plus/icons-vue'
import { submitContactForm } from '@/api/misc'

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const submitting = ref(false)

function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

async function submitForm() {
  if (!form.value.name.trim()) {
    ElMessage.warning('请输入姓名')
    return
  }
  
  if (!form.value.email.trim() || !validateEmail(form.value.email)) {
    ElMessage.warning('请输入有效的邮箱地址')
    return
  }
  
  if (!form.value.message.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }
  
  submitting.value = true
  
  try {
    await submitContactForm(form.value)
    
    ElMessage.success('消息已发送，我们会尽快回复您！')
    
    // 重置表单
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    }
  } catch (error) {
    console.error('联系表单提交失败:', error)
    // 如果后端接口未实现，使用备用方案（mailto）
    const mailtoLink = `mailto:mediacms@126.com?subject=${encodeURIComponent(form.value.subject || '网站联系')}&body=${encodeURIComponent(`姓名: ${form.value.name}\n邮箱: ${form.value.email}\n\n${form.value.message}`)}`
    window.location.href = mailtoLink
    ElMessage.info('将打开您的邮件客户端')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="home-sec contact-page">
    <div class="home-sec-head">
      <div class="home-sec-title">联系我们</div>
    </div>
    
    <el-row :gutter="32">
      <el-col :xs="24" :md="12">
        <el-card class="contact-form-card">
          <template #header>
            <h3>发送消息</h3>
          </template>
          
          <el-form :model="form" label-position="top">
            <el-form-item label="姓名" required>
              <el-input 
                v-model="form.name" 
                placeholder="请输入您的姓名"
                :prefix-icon="Message"
              />
            </el-form-item>
            
            <el-form-item label="邮箱" required>
              <el-input 
                v-model="form.email" 
                type="email"
                placeholder="example@email.com"
                :prefix-icon="Message"
              />
            </el-form-item>
            
            <el-form-item label="主题">
              <el-input 
                v-model="form.subject" 
                placeholder="请简述您的问题"
              />
            </el-form-item>
            
            <el-form-item label="消息" required>
              <el-input 
                v-model="form.message" 
                type="textarea"
                :rows="6"
                placeholder="请详细描述您的问题或建议..."
                maxlength="500"
                show-word-limit
              />
            </el-form-item>
            
            <el-form-item>
              <el-button 
                type="primary" 
                size="large"
                :loading="submitting"
                @click="submitForm"
                style="width: 100%"
              >
                {{ submitting ? '发送中...' : '发送消息' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :md="12">
        <el-card class="contact-info-card">
          <template #header>
            <h3>联系方式</h3>
          </template>
          
          <div class="contact-methods">
            <div class="contact-item">
              <el-icon class="contact-icon" :size="24"><Message /></el-icon>
              <div class="contact-details">
                <h4>邮箱</h4>
                <p class="contact-value">mediacms@126.com</p>
                <p class="contact-hint">技术支持和一般咨询</p>
              </div>
            </div>
            
            <el-divider />
            
            
            <div class="contact-item">
              <el-icon class="contact-icon" :size="24"><Location /></el-icon>
              <div class="contact-details">
                <h4>地址</h4>
                <p class="contact-value">为用户IP指定的地址</p>
                <p class="contact-hint">基于您的网络位置动态显示</p>
              </div>
            </div>
          </div>
        </el-card>
        
        <el-alert
          title="温馨提示"
          type="info"
          :closable="false"
          style="margin-top: 20px"
        >
          我们通常会在24小时内回复您的消息。如果您有紧急问题，请通过电话联系我们。
        </el-alert>
      </el-col>
    </el-row>
  </section>
</template>

<style scoped>
.contact-page {
  max-width: 1200px;
  margin: 0 auto;
}

.contact-form-card h3,
.contact-info-card h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.contact-methods {
  padding: 8px 0;
}

.contact-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 8px 0;
}

.contact-icon {
  color: var(--el-color-primary);
  flex-shrink: 0;
  margin-top: 4px;
}

[data-theme="dark"] .contact-icon {
  color: #4a9eff;
}

.contact-details h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

[data-theme="dark"] .contact-details h4 {
  color: #ffffff;
}

.contact-details p {
  margin: 4px 0;
  font-size: 14px;
}

.contact-details .contact-value {
  color: var(--el-text-color-primary);
  font-weight: 500;
}

.contact-details .contact-hint {
  color: var(--el-text-color-secondary);
  font-size: 13px;
}

[data-theme="dark"] .contact-details .contact-value {
  color: #e5e7eb;
}

[data-theme="dark"] .contact-details .contact-hint {
  color: #909399;
}

/* 暗色模式 - 卡片 */
[data-theme="dark"] .contact-form-card :deep(.el-card),
[data-theme="dark"] .contact-info-card :deep(.el-card) {
  background: #1a1a1a !important;
  border-color: #333 !important;
}

[data-theme="dark"] .contact-form-card :deep(.el-card__header),
[data-theme="dark"] .contact-info-card :deep(.el-card__header) {
  background: #1a1a1a !important;
  border-color: #333 !important;
  color: #ffffff;
}

[data-theme="dark"] .contact-form-card :deep(.el-card__body),
[data-theme="dark"] .contact-info-card :deep(.el-card__body) {
  background: #1a1a1a !important;
}

[data-theme="dark"] .contact-form-card h3,
[data-theme="dark"] .contact-info-card h3 {
  color: #ffffff;
}

/* 暗色模式 - Alert 提示框 */
[data-theme="dark"] :deep(.el-alert) {
  background: #262626 !important;
  border-color: #404040 !important;
}

[data-theme="dark"] :deep(.el-alert__title),
[data-theme="dark"] :deep(.el-alert__description) {
  color: #cccccc !important;
}

[data-theme="dark"] :deep(.el-alert--info) {
  background: #1a3a52 !important;
}

/* 暗色模式 - 表单元素 */
[data-theme="dark"] :deep(.el-form-item__label) {
  color: #cccccc;
}

[data-theme="dark"] :deep(.el-input__wrapper) {
  background-color: #262626;
  border-color: #404040;
}

[data-theme="dark"] :deep(.el-input__inner) {
  color: #ffffff;
  background-color: transparent;
}

[data-theme="dark"] :deep(.el-textarea__inner) {
  background-color: #262626;
  border-color: #404040;
  color: #ffffff;
}

[data-theme="dark"] :deep(.el-divider) {
  border-color: #333;
}

@media (max-width: 768px) {
  .contact-page :deep(.el-col) {
    margin-bottom: 20px;
  }
}
</style>
