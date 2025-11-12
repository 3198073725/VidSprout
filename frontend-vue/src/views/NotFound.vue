<script setup lang="ts">
import { useRouter } from 'vue-router'
import { 
  House, Search, Back, Menu, 
  Clock, Star, Grid, PriceTag, User, Upload 
} from '@element-plus/icons-vue'

const router = useRouter()

const popularLinks = [
  { path: '/latest', label: '最新内容', icon: Clock },
  { path: '/featured', label: '精选内容', icon: Star },
  { path: '/categories', label: '分类浏览', icon: Grid },
  { path: '/tags', label: '标签云', icon: PriceTag },
  { path: '/members', label: '社区成员', icon: User },
  { path: '/upload', label: '上传内容', icon: Upload }
]

function goHome() {
  router.push('/')
}

function goBack() {
  router.go(-1)
}

function searchContent() {
  router.push('/search')
}
</script>

<template>
  <div class="not-found-container">
    <!-- 对应后端模板的简洁结构，但增强用户体验 -->
    <div class="not-found-content">
      
      <!-- 主要错误信息 -->
      <el-result
        icon="error"
        title="404"
        sub-title="您迷路了！页面未找到"
      >
        <template #extra>
          <div class="action-buttons">
            <el-button type="primary" size="large" @click="goHome">
              返回首页
            </el-button>
            <el-button size="large" @click="goBack">
              返回上页
            </el-button>
            <el-button size="large" @click="searchContent">
              搜索内容
            </el-button>
          </div>
        </template>
      </el-result>
      
      <!-- 对应后端模板的 "you are lost!" 信息，但更友好 -->
      <div class="lost-message">
        <h2>看起来您迷路了！</h2>
        <p>您访问的页面可能已被移动、删除，或者您输入了错误的网址。</p>
      </div>
      
      <!-- 帮助建议 -->
      <el-card class="help-suggestions" shadow="never">
        <template #header>
          <h3>您可以尝试：</h3>
        </template>
        
        <div class="suggestions-list">
          <div class="suggestion-item">
            <el-icon class="suggestion-icon"><House /></el-icon>
            <div class="suggestion-content">
              <h4>返回首页</h4>
              <p>从首页重新开始浏览</p>
            </div>
          </div>
          
          <div class="suggestion-item">
            <el-icon class="suggestion-icon"><Search /></el-icon>
            <div class="suggestion-content">
              <h4>搜索内容</h4>
              <p>使用搜索功能找到您需要的内容</p>
            </div>
          </div>
          
          <div class="suggestion-item">
            <el-icon class="suggestion-icon"><Back /></el-icon>
            <div class="suggestion-content">
              <h4>返回上一页</h4>
              <p>回到您之前访问的页面</p>
            </div>
          </div>
          
          <div class="suggestion-item">
            <el-icon class="suggestion-icon"><Menu /></el-icon>
            <div class="suggestion-content">
              <h4>浏览分类</h4>
              <p>查看不同类别的内容</p>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 热门链接 -->
      <el-card class="popular-links" shadow="never">
        <template #header>
          <h3>热门页面</h3>
        </template>
        
        <div class="links-grid">
          <el-button 
            v-for="link in popularLinks" 
            :key="link.path"
            class="link-button"
            @click="router.push(link.path)"
          >
            <component :is="link.icon" />
            {{ link.label }}
          </el-button>
        </div>
      </el-card>
      
      <!-- 联系支持 -->
      <div class="contact-support">
        <el-alert
          title="仍然需要帮助？"
          type="info"
          :closable="false"
        >
          <p>如果您认为这是一个错误，或者需要其他帮助，请联系我们的客服团队。</p>
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
</template>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.not-found-content {
  max-width: 800px;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.not-found-content :deep(.el-result) {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.not-found-content :deep(.el-result__title) {
  font-size: 4rem;
  font-weight: 700;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.not-found-content :deep(.el-result__subtitle) {
  font-size: 1.2rem;
  color: var(--mc-text-secondary);
  margin-top: 16px;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 24px;
}

.lost-message {
  text-align: center;
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.lost-message h2 {
  margin: 0 0 16px 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.lost-message p {
  margin: 0;
  font-size: 1rem;
  color: var(--mc-text-secondary);
  line-height: 1.6;
}

.help-suggestions,
.popular-links {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.help-suggestions :deep(.el-card__header),
.popular-links :deep(.el-card__header) {
  padding: 20px 24px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.help-suggestions :deep(.el-card__header h3),
.popular-links :deep(.el-card__header h3) {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.suggestions-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 24px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.suggestion-icon {
  font-size: 20px;
  color: var(--el-color-primary);
  flex-shrink: 0;
  margin-top: 2px;
}

.suggestion-content {
  flex: 1;
}

.suggestion-content h4 {
  margin: 0 0 6px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--mc-text-primary);
}

.suggestion-content p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--mc-text-secondary);
  line-height: 1.4;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  padding: 24px;
}

.link-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  height: auto;
  border: 1px solid var(--el-border-color-light);
  background: var(--mc-bg-secondary);
  transition: all 0.3s ease;
}

.link-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: var(--el-color-primary);
}

.link-button :deep(svg) {
  width: 24px;
  height: 24px;
}

.contact-support {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.contact-actions {
  margin-top: 16px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .not-found-container {
    padding: 12px;
    align-items: flex-start;
    padding-top: 40px;
  }
  
  .not-found-content :deep(.el-result) {
    padding: 24px;
  }
  
  .not-found-content :deep(.el-result__title) {
    font-size: 3rem;
  }
  
  .not-found-content :deep(.el-result__subtitle) {
    font-size: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .action-buttons .el-button {
    width: 100%;
  }
  
  .lost-message {
    padding: 20px;
  }
  
  .lost-message h2 {
    font-size: 1.3rem;
  }
  
  .suggestions-list {
    grid-template-columns: 1fr;
    padding: 16px;
  }
  
  .links-grid {
    grid-template-columns: repeat(2, 1fr);
    padding: 16px;
  }
  
  .contact-support {
    padding: 16px;
  }
  
  .contact-actions {
    flex-direction: column;
  }
  
  .contact-actions .el-button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .not-found-content :deep(.el-result__title) {
    font-size: 2.5rem;
  }
  
  .links-grid {
    grid-template-columns: 1fr;
  }
  
  .suggestion-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
  }
}
</style>
