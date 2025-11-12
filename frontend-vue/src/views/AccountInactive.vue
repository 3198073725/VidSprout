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

function contactSupport() {
  router.push('/contact')
}

function goToHome() {
  router.push('/')
}
</script>

<template>
  <div class="account-inactive-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>账户已停用</h1>
        
        <!-- 对应后端模板的说明文字 -->
        <div class="account-inactive-content">
          <el-result
            icon="error"
            title="账户状态异常"
            sub-title="此账户已被停用。"
          >
            <template #extra>
              <div class="action-buttons">
                <el-button type="primary" @click="contactSupport">
                  联系客服
                </el-button>
                <el-button @click="logout">
                  退出登录
                </el-button>
                <el-button @click="goToHome">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>
          
          <!-- 详细说明 -->
          <el-card class="explanation-card" shadow="never">
            <template #header>
              <h3>关于账户停用</h3>
            </template>
            
            <div class="explanation-content">
              <p>您的账户目前处于停用状态，无法正常使用平台功能。账户可能因以下原因被停用：</p>
              
              <div class="reasons-list">
                <div class="reason-item">
                  <el-icon class="reason-icon"><Warning /></el-icon>
                  <div class="reason-content">
                    <h4>违反社区规则</h4>
                    <p>账户可能因违反平台的社区准则或使用条款而被暂时停用。</p>
                  </div>
                </div>
                
                <div class="reason-item">
                  <el-icon class="reason-icon"><Lock /></el-icon>
                  <div class="reason-content">
                    <h4>安全原因</h4>
                    <p>为了保护账户安全，系统可能会暂时停用存在安全风险的账户。</p>
                  </div>
                </div>
                
                <div class="reason-item">
                  <el-icon class="reason-icon"><DocumentRemove /></el-icon>
                  <div class="reason-content">
                    <h4>内容违规</h4>
                    <p>上传的内容可能违反了平台的内容政策和版权规定。</p>
                  </div>
                </div>
                
                <div class="reason-item">
                  <el-icon class="reason-icon"><UserFilled /></el-icon>
                  <div class="reason-content">
                    <h4>用户举报</h4>
                    <p>账户可能因多次被其他用户举报而被暂时停用以进行调查。</p>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 解决方案 -->
          <el-card class="solutions-card" shadow="never">
            <template #header>
              <h3>如何恢复账户</h3>
            </template>
            
            <div class="solutions-content">
              <div class="solution-steps">
                <div class="step-item">
                  <div class="step-number">1</div>
                  <div class="step-content">
                    <h4>联系客服</h4>
                    <p>立即联系我们的客服团队，说明您的情况并请求账户恢复。</p>
                  </div>
                </div>
                
                <div class="step-item">
                  <div class="step-number">2</div>
                  <div class="step-content">
                    <h4>提供信息</h4>
                    <p>根据客服要求提供必要的身份验证信息和相关证明材料。</p>
                  </div>
                </div>
                
                <div class="step-item">
                  <div class="step-number">3</div>
                  <div class="step-content">
                    <h4>等待审核</h4>
                    <p>我们的团队将审核您的申请，并在1-3个工作日内给出回复。</p>
                  </div>
                </div>
                
                <div class="step-item">
                  <div class="step-number">4</div>
                  <div class="step-content">
                    <h4>账户恢复</h4>
                    <p>审核通过后，您的账户将被重新激活，可以正常使用。</p>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 重要提醒 -->
          <el-card class="important-notes" shadow="never">
            <template #header>
              <h3>重要提醒</h3>
            </template>
            
            <div class="notes-content">
              <div class="note-item">
                <el-icon class="note-icon"><InfoFilled /></el-icon>
                <div class="note-text">
                  <strong>保持耐心</strong>
                  <p>账户恢复需要一定的审核时间，请耐心等待我们的回复。</p>
                </div>
              </div>
              
              <div class="note-item">
                <el-icon class="note-icon"><DocumentChecked /></el-icon>
                <div class="note-text">
                  <strong>遵守规则</strong>
                  <p>账户恢复后，请严格遵守平台的使用条款和社区准则。</p>
                </div>
              </div>
              
              <div class="note-item">
                <el-icon class="note-icon"><Shield /></el-icon>
                <div class="note-text">
                  <strong>账户安全</strong>
                  <p>定期更新密码，保护账户安全，避免再次被停用。</p>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 联系支持 -->
          <div class="contact-support">
            <el-alert
              title="立即寻求帮助"
              type="warning"
              :closable="false"
            >
              <p>如果您认为账户被错误停用，或者需要了解具体的停用原因，请立即联系我们的客服团队。</p>
              <div class="contact-actions">
                <el-button type="primary" size="small" @click="contactSupport">
                  联系客服
                </el-button>
                <el-button size="small" @click="router.push('/about')">
                  查看条款
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
.account-inactive-container {
  max-width: 700px;
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

.account-inactive-content {
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

.explanation-card,
.solutions-card,
.important-notes {
  margin-top: 8px;
}

.explanation-card :deep(.el-card__header),
.solutions-card :deep(.el-card__header),
.important-notes :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.explanation-card :deep(.el-card__header h3),
.solutions-card :deep(.el-card__header h3),
.important-notes :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.explanation-content p {
  margin: 0 0 20px 0;
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.reasons-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reason-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.reason-icon {
  font-size: 20px;
  color: var(--el-color-danger);
  flex-shrink: 0;
  margin-top: 2px;
}

.reason-content {
  flex: 1;
}

.reason-content h4 {
  margin: 0 0 6px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.reason-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
}

.solution-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--el-color-primary);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-content h4 {
  margin: 0 0 8px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.step-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.5;
}

.notes-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.note-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.note-icon {
  font-size: 18px;
  color: var(--el-color-warning);
  flex-shrink: 0;
  margin-top: 2px;
}

.note-text {
  flex: 1;
}

.note-text strong {
  display: block;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin-bottom: 4px;
}

.note-text p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
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
  .account-inactive-container {
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
  
  .reason-item,
  .step-item,
  .note-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
  }
  
  .contact-actions {
    flex-direction: column;
  }
  
  .contact-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .reason-content h4,
  .step-content h4,
  .note-text strong {
    font-size: 0.95rem;
  }
  
  .reason-content p,
  .step-content p,
  .note-text p {
    font-size: 0.85rem;
  }
}
</style>
