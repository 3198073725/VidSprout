<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { MediaDetail } from '@/api'

interface Props {
  media: MediaDetail
  activeTab?: string
}

const props = withDefaults(defineProps<Props>(), {
  activeTab: 'metadata'
})

const route = useRoute()
const router = useRouter()

// 获取媒体token
const mediaToken = computed(() => props.media.friendly_token)

// 导航项配置 - 对应后端模板的导航结构
const navItems = computed(() => {
  const items = [
    {
      key: 'metadata',
      label: '元数据',
      route: 'media-edit',
      icon: 'Edit'
    }
  ]
  
  // 只有视频类型才显示视频编辑相关选项
  if (props.media.media_type === 'video') {
    items.push(
      {
        key: 'trim',
        label: '剪辑',
        route: 'video-edit', 
        icon: 'Scissors'
      },
      {
        key: 'subtitles',
        label: '字幕',
        route: 'subtitle-add',
        icon: 'ChatLineRound'
      },
      {
        key: 'chapters',
        label: '章节',
        route: 'chapters-edit',
        icon: 'List'
      }
    )
  }
  
  items.push({
    key: 'publish',
    label: '发布',
    route: 'media-publish',
    icon: 'Share'
  })
  
  return items
})

function navigateTo(item: any) {
  router.push({
    name: item.route,
    params: { token: mediaToken.value }
  })
}

// 检查当前激活的标签
function isActive(key: string) {
  return props.activeTab === key
}
</script>

<template>
  <!-- 对应后端模板的 media-edit-nav 结构 -->
  <div class="media-edit-nav">
    <ul class="nav-list">
      <li 
        v-for="item in navItems" 
        :key="item.key"
        class="nav-item"
      >
        <a 
          href="#"
          :class="['nav-link', { active: isActive(item.key) }]"
          @click.prevent="navigateTo(item)"
        >
          <el-icon class="nav-icon">
            <component :is="item.icon" />
          </el-icon>
          {{ item.label }}
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* 对应后端模板的内联样式，转换为CSS类 */
.media-edit-nav {
  background-color: #f0f0f0;
  padding: 10px 0;
  margin-bottom: 20px;
  border-radius: 8px;
}

.nav-list {
  list-style: none;
  display: flex;
  justify-content: space-around;
  margin: 0;
  padding: 0;
  flex-wrap: wrap;
  gap: 8px;
}

.nav-item {
  display: inline-block;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: #666;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
}

.nav-link:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: #333;
}

.nav-link.active {
  font-weight: bold;
  color: #333;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-bottom: 2px solid #333;
}

.nav-icon {
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-list {
    justify-content: flex-start;
    overflow-x: auto;
    padding: 0 8px;
  }
  
  .nav-item {
    flex-shrink: 0;
  }
  
  .nav-link {
    padding: 6px 12px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .media-edit-nav {
    margin: 0 -12px 20px -12px;
    border-radius: 0;
  }
  
  .nav-list {
    gap: 4px;
  }
  
  .nav-link {
    padding: 6px 10px;
    font-size: 12px;
  }
  
  .nav-icon {
    font-size: 14px;
  }
}
</style>
