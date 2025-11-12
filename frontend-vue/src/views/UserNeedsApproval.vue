<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

async function logout() {
  try {
    await auth.logout()
    router.push('/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}
</script>

<template>
  <div class="user-needs-approval-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>账户等待审批</h1>
        
        <!-- 对应后端模板的说明文字 -->
        <div class="approval-content">
          <el-result
            icon="warning"
            title="账户审批中"
            sub-title="您的账户目前正在等待管理员审批。"
          >
            <template #extra>
              <div class="action-buttons">
                <!-- 对应后端模板的退出链接 -->
                <el-button type="primary" @click="logout">
                  退出登录
                </el-button>
                <el-button @click="router.push('/')">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>
          
          <!-- 详细说明信息 -->
          <el-card class="info-card" shadow="never">
            <template #header>
              <h3>关于账户审批</h3>
            </template>
            
            <div class="info-content">
              <p>您的账户注册已成功提交，但需要管理员审批后才能正常使用平台功能。</p>
              
              <div class="approval-steps">
                <div class="step-item">
                  <div class="step-icon completed">
                    <el-icon><Check /></el-icon>
                  </div>
                  <div class="step-content">
                    <h4>账户注册</h4>
                    <p>您已成功注册账户</p>
                  </div>
                </div>
                
                <div class="step-item">
                  <div class="step-icon current">
                    <el-icon><Clock /></el-icon>
                  </div>
                  <div class="step-content">
                    <h4>等待审批</h4>
                    <p>管理员正在审核您的账户</p>
                  </div>
                </div>
                
                <div class="step-item">
                  <div class="step-icon pending">
                    <el-icon><User /></el-icon>
                  </div>
                  <div class="step-content">
                    <h4>账户激活</h4>
                    <p>审批通过后即可正常使用</p>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 常见问题 -->
          <el-card class="faq-card" shadow="never">
            <template #header>
              <h3>常见问题</h3>
            </template>
            
            <el-collapse>
              <el-collapse-item title="审批需要多长时间？" name="1">
                <p>通常情况下，管理员会在1-3个工作日内完成审批。具体时间可能因申请数量而有所不同。</p>
              </el-collapse-item>
              
              <el-collapse-item title="如何知道审批结果？" name="2">
                <p>审批完成后，系统会向您的注册邮箱发送通知邮件。您也可以尝试重新登录来检查账户状态。</p>
              </el-collapse-item>
              
              <el-collapse-item title="审批被拒绝怎么办？" name="3">
                <p>如果审批被拒绝，您会收到相应的邮件通知和拒绝原因。您可以根据反馈修正信息后重新申请。</p>
              </el-collapse-item>
              
              <el-collapse-item title="可以联系管理员吗？" name="4">
                <p>如果您有特殊情况或疑问，可以通过客服渠道联系管理员进行咨询。</p>
              </el-collapse-item>
            </el-collapse>
          </el-card>
          
          <!-- 联系支持 -->
          <div class="contact-support">
            <el-alert
              title="需要帮助？"
              type="info"
              :closable="false"
            >
              <p>如果您对审批流程有任何疑问，或者等待时间过长，请联系我们的客服团队。</p>
              <div class="contact-actions">
                <el-button size="small" @click="router.push('/contact')">
                  联系客服
                </el-button>
              </div>
            </el-alert>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.user-needs-approval-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

/* 对应后端模板的 user-action-form-wrap 样式 */
.user-action-form-wrap {
  display: flex;
  justify-content: center;
}

.user-action-form-inner {
  width: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 32px;
}

.user-action-form-inner h1 {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 24px 0;
}

.approval-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.info-card,
.faq-card {
  margin-top: 8px;
}

.info-card :deep(.el-card__header),
.faq-card :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.info-card :deep(.el-card__header h3),
.faq-card :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.info-content p {
  margin: 0 0 20px 0;
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.approval-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.step-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  font-size: 18px;
}

.step-icon.completed {
  background: var(--el-color-success);
  color: white;
}

.step-icon.current {
  background: var(--el-color-warning);
  color: white;
  animation: pulse 2s infinite;
}

.step-icon.pending {
  background: var(--el-color-info-light-8);
  color: var(--el-color-info);
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin: 0 0 4px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.step-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
}

.faq-card :deep(.el-collapse-item__header) {
  font-weight: 600;
  color: var(--mc-text-primary);
}

.faq-card :deep(.el-collapse-item__content) {
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.contact-support {
  margin-top: 8px;
}

.contact-actions {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-needs-approval-container {
    padding: 12px;
  }
  
  .user-action-form-inner {
    padding: 20px;
    margin: 0 -4px;
  }
  
  .user-action-form-inner h1 {
    font-size: 1.5rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button {
    width: 100%;
  }
  
  .step-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 12px;
  }
  
  .contact-actions {
    flex-direction: column;
  }
  
  .contact-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .step-content h4 {
    font-size: 0.95rem;
  }
  
  .step-content p {
    font-size: 0.85rem;
  }
}
</style>
