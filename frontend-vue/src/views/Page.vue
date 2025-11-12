<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const page = ref<any>(null)

const pageSlug = computed(() => String(route.params.slug || ''))

async function loadPage() {
  if (!pageSlug.value) return
  
  loading.value = true
  try {
    // 这里应该调用页面详情API
    // const pageData = await PageAPI.getPage(pageSlug.value)
    
    // 模拟页面数据
    page.value = {
      title: '关于我们',
      description: `
        <div>
          <h2>欢迎来到我们的平台</h2>
          <p>这是一个专业的媒体内容管理平台，为用户提供优质的视频、音频和图片分享服务。</p>
          
          <h3>我们的使命</h3>
          <p>致力于为创作者和观众搭建一个安全、友好、高效的内容分享平台。</p>
          
          <h3>平台特色</h3>
          <ul>
            <li>高质量的媒体播放体验</li>
            <li>强大的内容管理功能</li>
            <li>完善的用户权限系统</li>
            <li>友好的社区互动环境</li>
          </ul>
          
          <h3>联系我们</h3>
          <p>如果您有任何问题或建议，请随时与我们联系。</p>
        </div>
      `
    }
  } catch (error) {
    console.error('加载页面失败:', error)
    page.value = null
  } finally {
    loading.value = false
  }
}

onMounted(loadPage)
</script>

<template>
  <div class="page-container">
    <div v-if="loading" class="loading-container">
      <el-skeleton :rows="8" animated />
    </div>

    <!-- 对应后端模板的 custom-page-wrapper -->
    <div v-else-if="page" class="custom-page-wrapper">
      
      <!-- 对应后端模板的页面标题 -->
      <h1>{{ page.title }}</h1>
      
      <!-- 对应后端模板的页面内容 (safe过滤器) -->
      <div class="page-content" v-html="page.description"></div>
      
    </div>

    <!-- 页面不存在 -->
    <div v-else class="page-not-found">
      <el-result
        icon="warning"
        title="页面不存在"
        sub-title="找不到指定的页面内容"
      >
        <template #extra>
          <el-button type="primary" @click="router.push('/')">
            返回首页
          </el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.loading-container {
  padding: 40px;
}

/* 对应后端模板的 custom-page-wrapper 样式 */
.custom-page-wrapper {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  line-height: 1.6;
}

.custom-page-wrapper h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--mc-text-primary);
  margin: 0 0 32px 0;
  text-align: center;
  border-bottom: 2px solid var(--el-color-primary);
  padding-bottom: 16px;
}

.page-content {
  color: var(--mc-text-primary);
}

/* 页面内容样式 */
.page-content :deep(h2) {
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin: 32px 0 16px 0;
  border-left: 4px solid var(--el-color-primary);
  padding-left: 16px;
}

.page-content :deep(h3) {
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin: 24px 0 12px 0;
}

.page-content :deep(h4) {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--mc-text-primary);
  margin: 20px 0 10px 0;
}

.page-content :deep(p) {
  margin: 16px 0;
  line-height: 1.7;
  color: var(--mc-text-secondary);
}

.page-content :deep(ul),
.page-content :deep(ol) {
  margin: 16px 0;
  padding-left: 24px;
}

.page-content :deep(li) {
  margin: 8px 0;
  line-height: 1.6;
  color: var(--mc-text-secondary);
}

.page-content :deep(blockquote) {
  margin: 20px 0;
  padding: 16px 20px;
  background: var(--mc-bg-secondary);
  border-left: 4px solid var(--el-color-primary);
  border-radius: 4px;
}

.page-content :deep(blockquote p) {
  margin: 0;
  font-style: italic;
  color: var(--mc-text-primary);
}

.page-content :deep(code) {
  background: var(--mc-bg-secondary);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.page-content :deep(pre) {
  background: var(--mc-bg-secondary);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 16px 0;
}

.page-content :deep(pre code) {
  background: none;
  padding: 0;
}

.page-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.page-content :deep(th),
.page-content :deep(td) {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--el-border-color-light);
}

.page-content :deep(th) {
  background: var(--mc-bg-secondary);
  font-weight: 600;
  color: var(--mc-text-primary);
}

.page-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.page-content :deep(a) {
  color: var(--el-color-primary);
  text-decoration: none;
}

.page-content :deep(a:hover) {
  text-decoration: underline;
}

.page-not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-container {
    padding: 12px;
  }
  
  .custom-page-wrapper {
    padding: 24px;
  }
  
  .custom-page-wrapper h1 {
    font-size: 2rem;
  }
  
  .page-content :deep(h2) {
    font-size: 1.5rem;
  }
  
  .page-content :deep(h3) {
    font-size: 1.3rem;
  }
  
  .page-content :deep(h4) {
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .custom-page-wrapper {
    padding: 16px;
  }
  
  .custom-page-wrapper h1 {
    font-size: 1.8rem;
  }
  
  .page-content :deep(ul),
  .page-content :deep(ol) {
    padding-left: 20px;
  }
  
  .page-content :deep(blockquote) {
    padding: 12px 16px;
  }
  
  .page-content :deep(th),
  .page-content :deep(td) {
    padding: 8px;
    font-size: 0.9rem;
  }
}
</style>
