<script setup lang="ts">
import type { Category } from '@/api'

const props = defineProps<{
  title: string
  items: Category[]
}>()

// 分类中文映射
const categoryMap: Record<string, string> = {
  'Art': '艺术',
  'Documentary': '纪录片',
  'Experimental': '实验',
  'Film': '电影',
  'Music': '音乐',
  'TV': '电视',
  'Animation': '动画',
  'Comedy': '喜剧',
  'Drama': '剧情',
  'Education': '教育',
  'Entertainment': '娱乐',
  'Gaming': '游戏',
  'News': '新闻',
  'Science': '科学',
  'Sports': '体育',
  'Technology': '科技',
  'Travel': '旅游',
  'Other': '其他'
}

function getCategoryName(category: Category): string {
  return categoryMap[category.title] || category.title
}
</script>

<template>
  <section class="home-sec">
    <div class="home-sec-head">
      <div class="home-sec-title">{{ title }}</div>
    </div>
    <div class="home-chip-row">
      <el-tag v-for="c in items" :key="c.title" round style="margin: 4px">{{ getCategoryName(c) }}</el-tag>
    </div>
  </section>
</template>
