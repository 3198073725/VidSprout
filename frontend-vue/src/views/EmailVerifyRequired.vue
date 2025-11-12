<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToEmailManage() {
  router.push('/email')
}

function goToContact() {
  router.push('/contact')
}

function goToHome() {
  router.push('/')
}
</script>

<template>
  <div class="email-verify-required-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>验证您的邮箱地址</h1>
        
        <!-- 对应后端模板的说明文字 -->
        <div class="verify-required-content">
          <el-result
            icon="warning"
            title="需要验证邮箱"
            sub-title="网站的这部分功能需要我们验证您的身份。"
          >
            <template #extra>
              <div class="action-buttons">
                <el-button type="primary" @click="goToEmailManage">
                  管理邮箱
                </el-button>
                <el-button @click="goToContact">
                  联系客服
                </el-button>
                <el-button @click="goToHome">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>
          
          <!-- 对应后端模板的详细说明 -->
          <el-card class="explanation-card" shadow="never">
            <template #header>
              <h3>为什么需要验证邮箱？</h3>
            </template>
            
            <div class="explanation-content">
              <!-- 对应后端模板的第一段说明 -->
              <p>
                网站的这部分功能需要我们验证您的身份。为此，我们需要您验证邮箱地址的所有权。
              </p>
              
              <!-- 对应后端模板的第二段说明 -->
              <p>
                我们已经向您发送了一封验证邮件。请点击邮件中的链接。如果您在几分钟内没有收到邮件，请联系我们。
              </p>
              
              <!-- 对应后端模板的注意事项 -->
              <el-alert
                type="info"
                :closable="false"
                show-icon
              >
                <template #title>
                  <strong>注意：</strong>您仍然可以 
                  <el-button type="text" @click="goToEmailManage">
                    更改您的邮箱地址
                  </el-button>
                </template>
              </el-alert>
            </div>
          </el-card>
          
          <!-- 验证步骤指南 -->
          <el-card class="steps-card" shadow="never">
            <template #header>
              <h3>验证步骤</h3>
            </template>
            
            <div class="verification-steps">
              <div class="step-item">
                <div class="step-icon">
                  <el-icon><Message /></el-icon>
                </div>
                <div class="step-content">
                  <h4>检查邮箱</h4>
                  <p>查看您的收件箱和垃圾邮件文件夹，寻找验证邮件</p>
                </div>
              </div>
              
              <div class="step-item">
                <div class="step-icon">
                  <el-icon><Link /></el-icon>
                </div>
                <div class="step-content">
                  <h4>点击链接</h4>
                  <p>点击邮件中的验证链接完成验证过程</p>
                </div>
              </div>
              
              <div class="step-item">
                <div class="step-icon">
                  <el-icon><Check /></el-icon>
                </div>
                <div class="step-content">
                  <h4>验证完成</h4>
                  <p>验证成功后即可访问所有功能</p>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 验证的好处 -->
          <el-card class="benefits-card" shadow="never">
            <template #header>
              <h3>验证邮箱的好处</h3>
            </template>
            
            <div class="benefits-list">
              <div class="benefit-item">
                <el-icon class="benefit-icon"><Shield /></el-icon>
                <div class="benefit-content">
                  <h4>提高安全性</h4>
                  <p>验证邮箱有助于保护您的账户安全，防止未授权访问</p>
                </div>
              </div>
              
              <div class="benefit-item">
                <el-icon class="benefit-icon"><Bell /></el-icon>
                <div class="benefit-content">
                  <h4>接收通知</h4>
                  <p>获取重要的系统通知、更新信息和安全提醒</p>
                </div>
              </div>
              
              <div class="benefit-item">
                <el-icon class="benefit-icon"><Key /></el-icon>
                <div class="benefit-content">
                  <h4>密码重置</h4>
                  <p>忘记密码时可以通过邮箱快速重置密码</p>
                </div>
              </div>
              
              <div class="benefit-item">
                <el-icon class="benefit-icon"><Star /></el-icon>
                <div class="benefit-content">
                  <h4>完整功能</h4>
                  <p>解锁平台的所有功能和服务</p>
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
                <p>请尝试以下解决方案：</p>
                <ul>
                  <li>检查垃圾邮件文件夹</li>
                  <li>确认邮箱地址正确</li>
                  <li>等待几分钟后重试</li>
                  <li>联系客服获取帮助</li>
                </ul>
              </el-collapse-item>
              
              <el-collapse-item title="可以使用其他邮箱吗？" name="2">
                <p>是的，您可以在邮箱管理页面添加或更改邮箱地址。建议使用您经常查看的邮箱。</p>
              </el-collapse-item>
              
              <el-collapse-item title="验证链接过期了怎么办？" name="3">
                <p>如果验证链接过期，您可以在邮箱管理页面重新发送验证邮件。</p>
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
              <p>如果您在邮箱验证过程中遇到任何问题，我们的客服团队随时为您提供帮助。</p>
              <div class="contact-actions">
                <el-button size="small" @click="goToContact">
                  联系客服
                </el-button>
                <el-button size="small" @click="goToEmailManage">
                  管理邮箱地址
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
.email-verify-required-container {
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

.verify-required-content {
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
.steps-card,
.benefits-card,
.faq-card {
  margin-top: 8px;
}

.explanation-card :deep(.el-card__header),
.steps-card :deep(.el-card__header),
.benefits-card :deep(.el-card__header),
.faq-card :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.explanation-card :deep(.el-card__header h3),
.steps-card :deep(.el-card__header h3),
.benefits-card :deep(.el-card__header h3),
.faq-card :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.explanation-content p {
  margin: 0 0 16px 0;
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.explanation-content p:last-of-type {
  margin-bottom: 20px;
}

.verification-steps {
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
  background: var(--el-color-primary-light-8);
  color: var(--el-color-primary);
  border-radius: 50%;
  flex-shrink: 0;
  font-size: 18px;
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

.benefits-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.benefit-icon {
  font-size: 20px;
  color: var(--el-color-success);
  flex-shrink: 0;
  margin-top: 2px;
}

.benefit-content {
  flex: 1;
}

.benefit-content h4 {
  margin: 0 0 6px 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.benefit-content p {
  margin: 0;
  font-size: 0.85rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
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
  .email-verify-required-container {
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
  
  .benefits-list {
    grid-template-columns: 1fr;
  }
  
  .benefit-item {
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
  .benefit-content h4 {
    font-size: 0.9rem;
  }
  
  .step-content p,
  .benefit-content p {
    font-size: 0.8rem;
  }
}
</style>
