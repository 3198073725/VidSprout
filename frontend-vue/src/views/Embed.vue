<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { MediaAPI } from '@/api'
import type { MediaDetail } from '@/api'
import VideoPlayer from '@/components/VideoPlayer.vue'

const route = useRoute()

// 从URL参数获取媒体token
const mediaToken = computed(() => String(route.query.m || ''))

const loading = ref(false)
const media = ref<MediaDetail | null>(null)
const error = ref('')

async function loadMedia() {
  if (!mediaToken.value) {
    error.value = '缺少媒体参数'
    return
  }
  
  loading.value = true
  try {
    media.value = await MediaAPI.getMediaDetail(mediaToken.value)
  } catch (err) {
    console.error('加载媒体失败:', err)
    error.value = '媒体加载失败'
  } finally {
    loading.value = false
  }
}

// 根据媒体类型返回合适的播放源
const mediaSource = computed(() => {
  if (!media.value) return null
  
  // 优先使用HLS流
  if (media.value.hls_info?.playlist_url) {
    return {
      type: 'hls',
      url: media.value.hls_info.playlist_url
    }
  }
  
  // 其次使用预览URL
  if (media.value.preview_url) {
    return {
      type: 'video',
      url: media.value.preview_url
    }
  }
  
  // 最后使用原始媒体URL
  if (media.value.original_media_url) {
    return {
      type: 'video', 
      url: media.value.original_media_url
    }
  }
  
  return null
})

const posterImage = computed(() => {
  return media.value?.poster_url || media.value?.thumbnail_url || null
})

onMounted(loadMedia)
</script>

<template>
  <!-- 对应后端模板的 root.html 扩展，简化布局 -->
  <div class="embed-container">
    <!-- 对应后端的 embed.css 样式 -->
    <div v-if="loading" class="embed-loading">
      <el-skeleton animated>
        <el-skeleton-item variant="rect" style="width: 100%; height: 100%" />
      </el-skeleton>
    </div>
    
    <div v-else-if="error" class="embed-error">
      <el-result
        icon="error"
        :title="error"
        sub-title="请检查媒体链接是否正确"
      />
    </div>
    
    <!-- 对应后端模板的 <div id="page-embed"></div> -->
    <div v-else-if="media" id="page-embed" class="embed-content">
      <!-- 视频播放器 -->
      <div v-if="media.media_type === 'video' && mediaSource" class="embed-player">
        <VideoPlayer
          :hls="mediaSource.type === 'hls' ? mediaSource.url : null"
          :src="mediaSource.type === 'video' ? mediaSource.url : null"
          :poster="posterImage"
          :controls="true"
          :autoplay="false"
        />
      </div>
      
      <!-- 音频播放器 -->
      <div v-else-if="media.media_type === 'audio' && mediaSource" class="embed-audio">
        <div class="audio-info">
          <img 
            v-if="posterImage"
            :src="posterImage"
            :alt="media.title"
            class="audio-cover"
          />
          <div class="audio-details">
            <h3>{{ media.title }}</h3>
            <p>{{ media.author_name }}</p>
          </div>
        </div>
        <audio 
          :src="mediaSource.url"
          :poster="posterImage"
          controls
          style="width: 100%"
        />
      </div>
      
      <!-- 图片显示 -->
      <div v-else-if="media.media_type === 'image'" class="embed-image">
        <img 
          :src="media.original_media_url || media.preview_url"
          :alt="media.title"
          style="max-width: 100%; max-height: 100%; object-fit: contain"
        />
      </div>
      
      <!-- 其他类型媒体 -->
      <div v-else class="embed-unsupported">
        <el-result
          icon="warning"
          title="不支持的媒体类型"
          :sub-title="`媒体类型: ${media.media_type || '未知'}`"
        />
      </div>
      
      <!-- 媒体信息 (可选显示) -->
      <div v-if="route.query.info !== 'false'" class="embed-info">
        <h4>{{ media.title }}</h4>
        <p v-if="media.description">{{ media.description }}</p>
        <div class="embed-meta">
          <span>{{ media.author_name }}</span>
          <span>{{ media.views || 0 }} 次观看</span>
        </div>
      </div>
    </div>
    
    <div v-else class="embed-empty">
      <el-result
        icon="info"
        title="未找到媒体"
        sub-title="请提供有效的媒体参数"
      />
    </div>
  </div>
</template>

<style scoped>
/* 对应后端的 embed.css 样式 */
.embed-container {
  width: 100%;
  height: 100vh;
  background: #000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.embed-loading,
.embed-error,
.embed-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.embed-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #000;
}

.embed-player {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
}

.embed-audio {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.audio-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 16px;
}

.audio-cover {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  object-fit: cover;
}

.audio-details h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
}

.audio-details p {
  margin: 0;
  opacity: 0.8;
}

.embed-image {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.embed-unsupported {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
}

.embed-info {
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 16px;
  max-height: 120px;
  overflow-y: auto;
}

.embed-info h4 {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.embed-info p {
  margin: 0 0 8px 0;
  font-size: 0.9rem;
  line-height: 1.4;
  opacity: 0.9;
}

.embed-meta {
  display: flex;
  gap: 16px;
  font-size: 0.8rem;
  opacity: 0.7;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .embed-audio {
    padding: 16px;
  }
  
  .audio-info {
    flex-direction: column;
    text-align: center;
  }
  
  .audio-cover {
    width: 60px;
    height: 60px;
  }
  
  .embed-info {
    padding: 12px;
  }
  
  .embed-meta {
    flex-direction: column;
    gap: 4px;
  }
}

/* 全屏模式 */
@media (max-height: 400px) {
  .embed-info {
    display: none;
  }
}
</style>
