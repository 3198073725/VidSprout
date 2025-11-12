<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Tag } from '@/api'

interface Props {
  title: string
  items: Tag[]
}

defineProps<Props>()

const router = useRouter()

const handleTagClick = (tag: Tag) => {
  router.push({ name: 'search', query: { q: tag.title } })
}
</script>

<template>
  <div class="tag-section">
    <h2 class="section-title">{{ title }}</h2>
    <div class="tag-list">
      <el-tag
        v-for="tag in items"
        :key="tag.id"
        class="tag-item"
        type="info"
        @click="handleTagClick(tag)"
      >
        {{ tag.title }}
      </el-tag>
    </div>
  </div>
</template>

<style scoped>
.tag-section {
  margin-top: 32px;
  padding: 20px 0;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  padding: 8px 16px;
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .tag-section {
    margin-top: 24px;
    padding: 16px 0;
  }
  
  .section-title {
    font-size: 18px;
  }
  
  .tag-list {
    gap: 8px;
  }
  
  .tag-item {
    font-size: 13px;
    padding: 6px 12px;
  }
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .section-title {
  color: #ffffff;
}

[data-theme="dark"] .tag-item {
  background: #2a2a2a;
  border-color: #404040;
  color: #cccccc;
}

[data-theme="dark"] .tag-item:hover {
  background: #333;
  border-color: #4a9eff;
  color: #ffffff;
}
</style>

