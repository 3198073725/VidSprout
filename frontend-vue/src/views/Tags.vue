<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { MiscAPI } from '@/api'
import type { Tag, Paginated } from '@/api'

const router = useRouter()
const loading = ref(false)
const page = ref(1)
const data = ref<Paginated<Tag> | null>(null)

async function load(p = 1) {
  loading.value = true
  try {
    page.value = p
    data.value = await MiscAPI.listTags({ page: p })
  } finally {
    loading.value = false
  }
}

function goToTag(tag: Tag) {
  // 使用搜索页面并传入标签参数
  router.push({ name: 'search', query: { q: tag.title, type: 'tag' } })
}

onMounted(() => load(1))
</script>

<template>
  <section class="home-sec">
    <div class="home-sec-head">
      <div class="home-sec-title">标签</div>
      <span class="tag-count" v-if="data?.count">共 {{ data.count }} 个标签</span>
    </div>
    <el-skeleton :loading="loading" animated>
      <template #default>
        <div class="tags-container">
          <div class="home-chip-row">
            <el-tag 
              v-for="t in (data?.results || [])" 
              :key="t.title" 
              type="success" 
              size="large"
              effect="plain"
              class="tag-item"
              @click="goToTag(t)"
            >
              <span class="tag-name">{{ t.title }}</span>
              <el-icon class="tag-icon"><ArrowRight /></el-icon>
            </el-tag>
          </div>
        </div>
        
        <!-- 分页 -->
        <el-pagination
          v-if="data && data.count > 20"
          v-model:current-page="page"
          :page-size="20"
          :total="data.count"
          layout="prev, pager, next"
          @current-change="load"
          style="margin-top: 24px; justify-content: center"
        />
      </template>
    </el-skeleton>
  </section>
</template>

<style scoped>
.home-sec-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.tag-count {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

[data-theme="dark"] .tag-count {
  color: #999;
}

.tags-container {
  min-height: 200px;
}

.tag-item {
  cursor: pointer;
  margin: 6px;
  padding: 8px 16px;
  font-size: 15px;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.tag-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
}

.tag-name {
  font-weight: 500;
}

.tag-icon {
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tag-item:hover .tag-icon {
  opacity: 1;
}

/* ===============================================
   夜间模式样式
   =============================================== */
[data-theme="dark"] .home-sec-title {
  color: #ffffff;
}

[data-theme="dark"] .tag-count {
  color: #999;
}

[data-theme="dark"] .tag-item {
  background: #2a2a2a;
  border-color: #404040;
  color: #cccccc;
}

[data-theme="dark"] .tag-item:hover {
  background: #333;
  border-color: #2ecc71;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(46, 204, 113, 0.4);
}

[data-theme="dark"] .tag-name {
  color: #cccccc;
}

[data-theme="dark"] .tag-item:hover .tag-name {
  color: #ffffff;
}
</style>
