<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToEmailManage() {
  router.push('/email')
}

function goToLogin() {
  router.push('/login')
}

function goToHome() {
  router.push('/')
}
</script>

<template>
  <div class="verification-sent-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>验证您的邮箱地址</h1>
        
        <!-- 对应后端模板的说明文字 -->
        <div class="verification-content">
          <el-result
            icon="success"
            title="验证邮件已发送"
            sub-title="我们已向您发送了一封验证邮件。请点击邮件中的链接来完成注册流程。"
          >
            <template #extra>
              <div class="action-buttons">
                <el-button type="primary" @click="goToLogin">
                  前往登录
                </el-button>
                <el-button @click="goToEmailManage">
                  管理邮箱
                </el-button>
                <el-button @click="goToHome">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>
          
          <!-- 对应后端模板的联系提示 -->
          <el-alert
            title="没有收到邮件？"
            type="info"
            :closable="false"
            show-icon
          >
            <p>如果您在几分钟内没有收到邮件，请联系我们。</p>
          </el-alert>
          
          <!-- 详细操作指南 -->
          <el-card class="guide-card" shadow="never">
            <template #header>
              <h3>接下来该怎么做？</h3>
            </template>
            
            <div class="guide-steps">
              <div class="guide-step">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h4>检查您的邮箱</h4>
                  <p>查看收件箱和垃圾邮件文件夹，寻找来自我们的验证邮件。</p>
                </div>
              </div>
              
              <div class="guide-step">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h4>点击验证链接</h4>
                  <p>在邮件中找到"验证邮箱"按钮或链接，点击完成验证。</p>
                </div>
              </div>
              
              <div class="guide-step">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h4>完成注册</h4>
                  <p>验证成功后，您就可以正常使用平台的所有功能了。</p>
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
              <el-collapse-item title="没有收到验证邮件怎么办？" name="1">
                <p>请检查以下几点：</p>
                <ul>
                  <li>确认邮箱地址输入正确</li>
                  <li>检查垃圾邮件文件夹</li>
                  <li>等待几分钟，邮件可能会延迟到达</li>
                  <li>检查邮箱是否已满</li>
                </ul>
              </el-collapse-item>
              
              <el-collapse-item title="验证链接过期了怎么办？" name="2">
                <p>验证链接通常在24-48小时内有效。如果链接过期，您可以在邮箱管理页面重新发送验证邮件。</p>
              </el-collapse-item>
              
              <el-collapse-item title="可以更改邮箱地址吗？" name="3">
                <p>是的，您可以在邮箱管理页面添加新的邮箱地址或修改现有的邮箱地址。</p>
              </el-collapse-item>
              
              <el-collapse-item title="验证邮箱有什么好处？" name="4">
                <p>验证邮箱后，您可以：</p>
                <ul>
                  <li>接收重要的系统通知</li>
                  <li>使用密码重置功能</li>
                  <li>享受完整的平台功能</li>
                  <li>提高账户安全性</li>
                </ul>
              </el-collapse-item>
            </el-collapse>
          </el-card>
          
          <!-- 重要提醒 -->
          <el-card class="reminder-card" shadow="never">
            <template #header>
              <h3>重要提醒</h3>
            </template>
            
            <div class="reminder-content">
              <div class="reminder-item">
                <el-icon class="reminder-icon"><Warning /></el-icon>
                <div class="reminder-text">
                  <strong>验证链接仅能使用一次</strong>
                  <p>点击验证链接后，该链接将失效。如需重新验证，请申请新的验证邮件。</p>
                </div>
              </div>
              
              <div class="reminder-item">
                <el-icon class="reminder-icon"><Clock /></el-icon>
                <div class="reminder-text">
                  <strong>验证链接有时效性</strong>
                  <p>为了安全起见，验证链接会在一定时间后过期。请尽快完成验证。</p>
                </div>
              </div>
              
              <div class="reminder-item">
                <el-icon class="reminder-icon"><Lock /></el-icon>
                <div class="reminder-text">
                  <strong>保护您的邮箱安全</strong>
                  <p>请确保您的邮箱账户安全，避免他人代为验证或访问您的邮件。</p>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 联系支持 -->
          <div class="contact-support">
            <el-alert
              title="需要帮助？"
              type="info"
              :closable="false"
            >
              <p>如果您在邮箱验证过程中遇到任何问题，请联系我们的客服团队。</p>
              <div class="contact-actions">
                <el-button size="small" @click="router.push('/contact')">
                  联系客服
                </el-button>
                <el-button size="small" @click="goToEmailManage">
                  重新发送验证邮件
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
.verification-sent-container {
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

.verification-content {
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

.guide-card,
.faq-card,
.reminder-card {
  margin-top: 8px;
}

.guide-card :deep(.el-card__header),
.faq-card :deep(.el-card__header),
.reminder-card :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.guide-card :deep(.el-card__header h3),
.faq-card :deep(.el-card__header h3),
.reminder-card :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.guide-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.guide-step {
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

.faq-card :deep(.el-collapse-item__header) {
  font-weight: 600;
  color: var(--mc-text-primary);
}

.faq-card :deep(.el-collapse-item__content) {
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.faq-card ul {
  margin: 8px 0;
  padding-left: 20px;
}

.faq-card li {
  margin-bottom: 4px;
}

.reminder-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.reminder-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.reminder-icon {
  font-size: 20px;
  color: var(--el-color-warning);
  flex-shrink: 0;
  margin-top: 2px;
}

.reminder-text {
  flex: 1;
}

.reminder-text strong {
  display: block;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin-bottom: 4px;
}

.reminder-text p {
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
  .verification-sent-container {
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
  
  .guide-step {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 12px;
  }
  
  .reminder-item {
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
  .step-content h4,
  .reminder-text strong {
    font-size: 0.95rem;
  }
  
  .step-content p,
  .reminder-text p {
    font-size: 0.85rem;
  }
}
</style>
