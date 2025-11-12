<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

// 对应后端模板的用户登录状态检查
const isLoggedIn = computed(() => auth.token)

function goToLogin() {
  router.push('/login')
}

function goToHome() {
  router.push('/')
}
</script>

<template>
  <div class="password-reset-done-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>密码重置</h1>

        <!-- 对应后端模板的 {% if user.is_authenticated %} 条件 -->
        <div v-if="isLoggedIn" class="already-logged-in">
          <el-alert
            title="您已经登录"
            type="info"
            :closable="false"
            show-icon
          >
            <p>您当前已经登录到系统中。如果您想重置其他账户的密码，请先退出当前账户。</p>
          </el-alert>
        </div>

        <!-- 对应后端模板的主要内容 -->
        <div class="reset-done-content">
          <el-result
            icon="success"
            title="密码重置邮件已发送"
            sub-title="我们已经向您发送了一封邮件。如果您在几分钟内没有收到邮件，请联系我们。"
          >
            <template #extra>
              <div class="action-buttons">
                <el-button type="primary" @click="goToLogin">
                  前往登录
                </el-button>
                <el-button @click="goToHome">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>

          <!-- 额外的帮助信息 -->
          <el-card class="help-info" shadow="never">
            <template #header>
              <h3>接下来该怎么做？</h3>
            </template>
            
            <div class="help-steps">
              <div class="help-step">
                <div class="step-number">1</div>
                <div class="step-content">
                  <h4>检查您的邮箱</h4>
                  <p>查看收件箱和垃圾邮件文件夹，寻找来自我们的密码重置邮件。</p>
                </div>
              </div>
              
              <div class="help-step">
                <div class="step-number">2</div>
                <div class="step-content">
                  <h4>点击重置链接</h4>
                  <p>在邮件中找到"重置密码"按钮或链接，点击进入密码重置页面。</p>
                </div>
              </div>
              
              <div class="help-step">
                <div class="step-number">3</div>
                <div class="step-content">
                  <h4>设置新密码</h4>
                  <p>输入您的新密码，确认后即可使用新密码登录系统。</p>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 常见问题 -->
          <el-card class="faq-section" shadow="never">
            <template #header>
              <h3>常见问题</h3>
            </template>
            
            <el-collapse>
              <el-collapse-item title="没有收到重置邮件怎么办？" name="1">
                <p>请检查以下几点：</p>
                <ul>
                  <li>确认邮箱地址输入正确</li>
                  <li>检查垃圾邮件文件夹</li>
                  <li>等待几分钟，邮件可能会延迟到达</li>
                  <li>如果仍未收到，请联系客服</li>
                </ul>
              </el-collapse-item>
              
              <el-collapse-item title="重置链接过期了怎么办？" name="2">
                <p>密码重置链接有时效性，通常在24小时内有效。如果链接过期，请重新申请密码重置。</p>
              </el-collapse-item>
              
              <el-collapse-item title="可以重新发送重置邮件吗？" name="3">
                <p>可以的。如果您没有收到邮件，可以返回密码重置页面重新提交申请。</p>
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
              <p>如果您在密码重置过程中遇到任何问题，请联系我们的客服团队。</p>
              <div class="contact-actions">
                <el-button size="small" @click="router.push('/contact')">
                  联系客服
                </el-button>
                <el-button size="small" @click="router.push('/password-reset')">
                  重新申请重置
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
.password-reset-done-container {
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

.already-logged-in {
  margin-bottom: 24px;
}

.reset-done-content {
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

.help-info,
.faq-section {
  margin-top: 8px;
}

.help-info :deep(.el-card__header),
.faq-section :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.help-info :deep(.el-card__header h3),
.faq-section :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.help-steps {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.help-step {
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

.faq-section :deep(.el-collapse-item__header) {
  font-weight: 600;
  color: var(--mc-text-primary);
}

.faq-section :deep(.el-collapse-item__content) {
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.faq-section ul {
  margin: 8px 0;
  padding-left: 20px;
}

.faq-section li {
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
  .password-reset-done-container {
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
  
  .help-step {
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
