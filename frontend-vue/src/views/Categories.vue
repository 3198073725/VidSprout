<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { MiscAPI } from '@/api'
import type { Category } from '@/api'

const router = useRouter()
const loading = ref(false)
const categories = ref<Category[]>([])

async function loadCategories() {
  loading.value = true
  try {
    // 添加SEO元数据
    document.title = 'Categories - Short Video Platform'
    
    // 添加结构化数据
    const existingScript = document.querySelector('script[type="application/ld+json"]')
    if (existingScript) {
      existingScript.remove()
    }
    
    const script = document.createElement('script')
    script.type = 'application/ld+json'
    script.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "Short Video Platform",
        "item": {
          "@type": "WebPage",
          "@id": window.location.origin
        }
      }, {
        "@type": "ListItem",
        "position": 2,
        "name": "Categories",
        "item": {
          "@type": "WebPage",
          "@id": window.location.origin + "/categories"
        }
      }]
    })
    document.head.appendChild(script)
    
    // 加载分类数据
    categories.value = await MiscAPI.listCategories()
  } catch (error) {
    console.error('加载分类失败:', error)
  } finally {
    loading.value = false
  }
}

function viewCategory(category: Category) {
  // 跳转到该分类的媒体页面
  router.push({ name: 'search', query: { category: category.title } })
}

onMounted(loadCategories)
</script>

<template>
  <div class="categories-container">
    <!-- 对应后端模板的 <div id="page-categories"></div> -->
    <div id="page-categories">
      <div class="page-header">
        <h1>分类</h1>
      </div>

      <el-skeleton :loading="loading" animated>
        <template #template>
          <div class="categories-skeleton">
            <el-skeleton-item 
              v-for="n in 12" 
              :key="n"
              variant="rect" 
              style="width: 200px; height: 120px; margin: 8px"
            />
          </div>
        </template>

        <template #default>
          <div v-if="categories.length" class="categories-content">
            <!-- 分类网格 -->
            <div class="categories-grid">
              <div 
                v-for="category in categories" 
                :key="category.title"
                class="category-card"
                @click="viewCategory(category)"
              >
                <div class="category-icon">
                  <el-icon size="32"><Folder /></el-icon>
                </div>
                <div class="category-info">
                  <h3 class="category-title">{{ category.title }}</h3>
                  <div class="category-description" v-if="category.description">
                    {{ category.description }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <el-empty 
            v-else 
            description="暂无分类"
            :image-size="120"
          />
        </template>
      </el-skeleton>
    </div>
  </div>
</template>

<style scoped>
.categories-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 对应后端模板的 page-categories 样式 */
#page-categories {
  width: 100%;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.categories-skeleton {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
}

.categories-content {
  min-height: 400px;
}

/* 分类网格布局 */
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.category-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.category-icon {
  margin-bottom: 16px;
  color: #409eff;
}

.category-info {
  width: 100%;
}

.category-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.category-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .categories-container {
    padding: 16px;
  }
  
  .page-header h1 {
    font-size: 2rem;
  }
  
  .categories-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    padding: 16px 0;
  }
  
  .category-card {
    padding: 20px;
  }
  
  .category-title {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .categories-container {
    padding: 12px;
  }
  
  .categories-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
  
  .category-card {
    padding: 16px;
  }
  
  .category-title {
    font-size: 15px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .categories-container {
  background: #0a0a0a;
  color: #ffffff;
}

[data-theme="dark"] .page-header h1 {
  color: #ffffff;
}

[data-theme="dark"] .category-card {
  background: #1a1a1a;
  border: 1px solid #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .category-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
  border-color: #4a9eff;
}

[data-theme="dark"] .category-icon {
  color: #4a9eff;
}

[data-theme="dark"] .category-title {
  color: #ffffff;
}

[data-theme="dark"] .category-description {
  color: #999;
}
</style>
