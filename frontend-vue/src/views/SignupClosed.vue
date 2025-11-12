<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToLogin() {
  router.push('/login')
}

function goToHome() {
  router.push('/')
}

function contactSupport() {
  router.push('/contact')
}
</script>

<template>
  <div class="signup-closed-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>注册已关闭</h1>
        
        <!-- 对应后端模板的说明文字 -->
        <div class="signup-closed-content">
          <el-result
            icon="warning"
            title="注册暂时关闭"
            sub-title="很抱歉，注册功能目前已关闭。"
          >
            <template #extra>
              <div class="action-buttons">
                <el-button type="primary" @click="goToLogin">
                  已有账户？登录
                </el-button>
                <el-button @click="contactSupport">
                  联系客服
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
              <h3>关于注册关闭</h3>
            </template>
            
            <div class="explanation-content">
              <p>我们很抱歉通知您，新用户注册功能目前暂时关闭。这可能是由于以下原因：</p>
              
              <div class="reasons-list">
                <div class="reason-item">
                  <el-icon class="reason-icon"><Tools /></el-icon>
                  <div class="reason-content">
                    <h4>系统维护</h4>
                    <p>我们正在进行系统升级和维护，以提供更好的服务体验。</p>
                  </div>
                </div>
                
                <div class="reason-item">
                  <el-icon class="reason-icon"><UserFilled /></el-icon>
                  <div class="reason-content">
                    <h4>用户容量限制</h4>
                    <p>为了保证现有用户的服务质量，我们暂时限制新用户注册。</p>
                  </div>
                </div>
                
                <div class="reason-item">
                  <el-icon class="reason-icon"><Setting /></el-icon>
                  <div class="reason-content">
                    <h4>功能完善</h4>
                    <p>我们正在完善平台功能，为新用户提供更完整的体验。</p>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 替代方案 */
          <el-card class="alternatives-card" shadow="never">
            <template #header>
              <h3>您可以尝试</h3>
            </template>
            
            <div class="alternatives-content">
              <div class="alternative-item">
                <el-icon class="alt-icon"><Clock /></el-icon>
                <div class="alt-content">
                  <h4>稍后再试</h4>
                  <p>请稍后再次访问，我们会尽快重新开放注册功能。</p>
                </div>
              </div>
              
              <div class="alternative-item">
                <el-icon class="alt-icon"><Message /></el-icon>
                <div class="alt-content">
                  <h4>联系客服</h4>
                  <p>如有特殊需求，请联系我们的客服团队寻求帮助。</p>
                </div>
              </div>
              
              <div class="alternative-item">
                <el-icon class="alt-icon"><Bell /></el-icon>
                <div class="alt-content">
                  <h4>关注更新</h4>
                  <p>关注我们的官方渠道，第一时间了解注册开放信息。</p>
                </div>
              </div>
            </div>
          </el-card>
          
          <!-- 现有用户登录 -->
          <el-card class="existing-users-card" shadow="never">
            <template #header>
              <h3>已有账户？</h3>
            </template>
            
            <div class="existing-users-content">
              <p>如果您已经拥有账户，可以直接登录使用平台的所有功能。</p>
              
              <div class="login-benefits">
                <h4>登录后您可以：</h4>
                <ul>
                  <li>上传和管理媒体内容</li>
                  <li>创建和编辑播放列表</li>
                  <li>参与社区讨论和互动</li>
                  <li>享受个性化推荐</li>
                  <li>使用高级功能和工具</li>
                </ul>
              </div>
              
              <div class="login-action">
                <el-button type="primary" size="large" @click="goToLogin">
                  立即登录
                </el-button>
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
              <p>如果您有任何疑问或特殊需求，请不要犹豫联系我们的客服团队。</p>
              <div class="contact-actions">
                <el-button size="small" @click="contactSupport">
                  联系客服
                </el-button>
                <el-button size="small" @click="router.push('/about')">
                  关于我们
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
.signup-closed-container {
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

.signup-closed-content {
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
.alternatives-card,
.existing-users-card {
  margin-top: 8px;
}

.explanation-card :deep(.el-card__header),
.alternatives-card :deep(.el-card__header),
.existing-users-card :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.explanation-card :deep(.el-card__header h3),
.alternatives-card :deep(.el-card__header h3),
.existing-users-card :deep(.el-card__header h3) {
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
  color: var(--el-color-warning);
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

.alternatives-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.alternative-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.alt-icon {
  font-size: 18px;
  color: var(--el-color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.alt-content {
  flex: 1;
}

.alt-content h4 {
  margin: 0 0 6px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.alt-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
}

.existing-users-content p {
  margin: 0 0 20px 0;
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.login-benefits h4 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.login-benefits ul {
  margin: 0 0 20px 0;
  padding-left: 20px;
  color: var(--mc-text-secondary);
}

.login-benefits li {
  margin-bottom: 6px;
  line-height: 1.4;
}

.login-action {
  text-align: center;
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
  .signup-closed-container {
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
  .alternative-item {
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
  .alt-content h4 {
    font-size: 0.95rem;
  }
  
  .reason-content p,
  .alt-content p {
    font-size: 0.85rem;
  }
}
</style>
