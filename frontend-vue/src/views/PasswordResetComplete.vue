<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToLogin() {
  router.push('/login')
}

function goToHome() {
  router.push('/')
}
</script>

<template>
  <div class="password-reset-complete-container">
    <!-- 对应后端模板的 user-action-form-wrap 结构 -->
    <div class="user-action-form-wrap">
      <div class="user-action-form-inner">
        
        <!-- 对应后端模板的标题 -->
        <h1>密码修改</h1>
        
        <!-- 对应后端模板的成功信息 -->
        <div class="reset-complete-content">
          <el-result
            icon="success"
            title="密码修改成功"
            sub-title="您的密码已经成功修改。"
          >
            <template #extra>
              <div class="action-buttons">
                <el-button type="primary" size="large" @click="goToLogin">
                  立即登录
                </el-button>
                <el-button size="large" @click="goToHome">
                  返回首页
                </el-button>
              </div>
            </template>
          </el-result>
          
          <!-- 成功提示信息 -->
          <el-card class="success-info" shadow="never">
            <template #header>
              <h3>密码修改完成</h3>
            </template>
            
            <div class="info-content">
              <p>恭喜！您的密码已经成功修改。现在您可以使用新密码登录系统。</p>
              
              <div class="next-steps">
                <h4>接下来您可以：</h4>
                <ul>
                  <li>使用新密码立即登录</li>
                  <li>浏览平台内容</li>
                  <li>上传和管理您的媒体</li>
                  <li>参与社区互动</li>
                </ul>
              </div>
            </div>
          </el-card>
          
          <!-- 安全提醒 -->
          <el-card class="security-tips" shadow="never">
            <template #header>
              <h3>安全提醒</h3>
            </template>
            
            <div class="tips-content">
              <div class="tip-item">
                <el-icon class="tip-icon"><Lock /></el-icon>
                <div class="tip-text">
                  <strong>保护您的新密码</strong>
                  <p>请妥善保管您的新密码，不要与他人分享。</p>
                </div>
              </div>
              
              <div class="tip-item">
                <el-icon class="tip-icon"><Shield /></el-icon>
                <div class="tip-text">
                  <strong>定期更换密码</strong>
                  <p>建议您定期更换密码以保持账户安全。</p>
                </div>
              </div>
              
              <div class="tip-item">
                <el-icon class="tip-icon"><Warning /></el-icon>
                <div class="tip-text">
                  <strong>注意异常活动</strong>
                  <p>如发现账户有异常活动，请立即联系客服。</p>
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
              <p>如果您在使用过程中遇到任何问题，我们的客服团队随时为您提供帮助。</p>
              <div class="contact-actions">
                <el-button size="small" @click="router.push('/contact')">
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
.password-reset-complete-container {
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

.reset-complete-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.success-info,
.security-tips {
  margin-top: 8px;
}

.success-info :deep(.el-card__header),
.security-tips :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.success-info :deep(.el-card__header h3),
.security-tips :deep(.el-card__header h3) {
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

.next-steps h4 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.next-steps ul {
  margin: 0;
  padding-left: 20px;
  color: var(--mc-text-secondary);
}

.next-steps li {
  margin-bottom: 6px;
  line-height: 1.4;
}

.tips-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.tip-icon {
  font-size: 20px;
  color: var(--el-color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.tip-text {
  flex: 1;
}

.tip-text strong {
  display: block;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin-bottom: 4px;
}

.tip-text p {
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
  .password-reset-complete-container {
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
  
  .tip-item {
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
  .tip-text strong {
    font-size: 0.95rem;
  }
  
  .tip-text p {
    font-size: 0.85rem;
  }
}
</style>
