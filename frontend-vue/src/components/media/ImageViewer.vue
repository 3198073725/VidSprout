<template>
  <div class="image-viewer">
    <!-- 浮动工具栏 - 鼠标悬停时显示 -->
    <div class="image-toolbar-floating">
      <el-button-group size="small">
        <el-button @click="zoomOut" :icon="ZoomOut" :disabled="scale <= 0.25" circle />
        <el-button @click="resetZoom" circle>{{ Math.round(scale * 100) }}%</el-button>
        <el-button @click="zoomIn" :icon="ZoomIn" :disabled="scale >= 5" circle />
      </el-button-group>
      
      <el-button-group size="small" style="margin-left: 8px;">
        <el-button @click="rotateLeft" :icon="RefreshLeft" circle />
        <el-button @click="rotateRight" :icon="RefreshRight" circle />
      </el-button-group>
      
      <el-button-group size="small" style="margin-left: 8px;">
        <el-button @click="fullscreen" :icon="FullScreen" circle />
        <el-button @click="download" :icon="Download" type="primary" circle />
      </el-button-group>
    </div>
    
    <div 
      ref="containerRef" 
      class="image-container"
      @wheel="handleWheel"
      @mousedown="handleMouseDown"
      @mousemove="handleMouseMove"
      @mouseup="handleMouseUp"
      @mouseleave="handleMouseUp"
    >
      <div v-if="loading" class="image-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
      
      <div v-if="error" class="image-error">
        <el-icon><WarningFilled /></el-icon>
        <p>{{ error }}</p>
      </div>
      
      <img 
        v-show="!loading && !error"
        ref="imageRef"
        :src="src"
        :alt="alt"
        class="image-content"
        :style="imageStyle"
        draggable="false"
        @load="onImageLoad"
        @error="onImageError"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  ZoomIn, 
  ZoomOut,
  FullScreen,
  RefreshLeft,
  RefreshRight,
  Download,
  Loading,
  WarningFilled
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Props {
  src: string
  alt?: string
  filename?: string
}

const props = withDefaults(defineProps<Props>(), {
  alt: '图片',
  filename: 'image.jpg'
})

// 定义事件
const emit = defineEmits<{
  (e: 'load'): void
  (e: 'error'): void
}>()

// 调试日志
console.log('🖼️ ImageViewer 初始化:')
console.log('  - src:', props.src)
console.log('  - alt:', props.alt)
console.log('  - filename:', props.filename)

const loading = ref(true)
const error = ref('')
const scale = ref(1)
const rotation = ref(0)
const translateX = ref(0)
const translateY = ref(0)

const containerRef = ref<HTMLElement | null>(null)
const imageRef = ref<HTMLImageElement | null>(null)

// 拖拽相关
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragStartTranslateX = ref(0)
const dragStartTranslateY = ref(0)

// 图片样式
const imageStyle = computed(() => ({
  transform: `
    scale(${scale.value}) 
    rotate(${rotation.value}deg) 
    translate(${translateX.value}px, ${translateY.value}px)
  `
}))

// 缩放功能
const zoomIn = () => {
  if (scale.value < 5) {
    scale.value = Math.min(scale.value * 1.25, 5)
  }
}

const zoomOut = () => {
  if (scale.value > 0.25) {
    scale.value = Math.max(scale.value / 1.25, 0.25)
  }
}

const resetZoom = () => {
  scale.value = 1
  rotation.value = 0
  translateX.value = 0
  translateY.value = 0
}

// 旋转功能
const rotateLeft = () => {
  rotation.value = (rotation.value - 90) % 360
}

const rotateRight = () => {
  rotation.value = (rotation.value + 90) % 360
}

// 鼠标滚轮缩放
const handleWheel = (e: WheelEvent) => {
  e.preventDefault()
  if (e.deltaY < 0) {
    zoomIn()
  } else {
    zoomOut()
  }
}

// 拖拽功能
const handleMouseDown = (e: MouseEvent) => {
  if (e.button !== 0) return // 只响应左键
  isDragging.value = true
  dragStartX.value = e.clientX
  dragStartY.value = e.clientY
  dragStartTranslateX.value = translateX.value
  dragStartTranslateY.value = translateY.value
}

const handleMouseMove = (e: MouseEvent) => {
  if (!isDragging.value) return
  
  const deltaX = e.clientX - dragStartX.value
  const deltaY = e.clientY - dragStartY.value
  
  translateX.value = dragStartTranslateX.value + deltaX / scale.value
  translateY.value = dragStartTranslateY.value + deltaY / scale.value
}

const handleMouseUp = () => {
  isDragging.value = false
}

// 双击重置
const handleDblClick = () => {
  resetZoom()
}

// 全屏
const fullscreen = () => {
  if (!containerRef.value) return
  
  if (document.fullscreenElement) {
    document.exitFullscreen()
  } else {
    containerRef.value.requestFullscreen().catch(err => {
      ElMessage.error('无法进入全屏模式')
    })
  }
}

// 下载
const download = () => {
  const link = document.createElement('a')
  link.href = props.src
  link.download = props.filename
  link.click()
  ElMessage.success('开始下载')
}

// 图片加载完成
const onImageLoad = () => {
  console.log('✅ 图片加载成功:', props.src)
  loading.value = false
  error.value = ''
  // 触发加载成功事件
  emit('load')
}

// 图片加载失败
const onImageError = (e: Event) => {
  console.error('❌ 图片加载失败:', props.src, e)
  loading.value = false
  error.value = '图片加载失败，请检查图片URL'
  // 触发加载失败事件
  emit('error')
}

// 键盘快捷键
const handleKeydown = (e: KeyboardEvent) => {
  switch (e.key) {
    case '+':
    case '=':
      e.preventDefault()
      zoomIn()
      break
    case '-':
      e.preventDefault()
      zoomOut()
      break
    case '0':
      e.preventDefault()
      resetZoom()
      break
    case 'ArrowLeft':
      e.preventDefault()
      rotateLeft()
      break
    case 'ArrowRight':
      e.preventDefault()
      rotateRight()
      break
    case 'f':
    case 'F':
      e.preventDefault()
      fullscreen()
      break
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  if (containerRef.value) {
    containerRef.value.addEventListener('dblclick', handleDblClick)
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  if (containerRef.value) {
    containerRef.value.removeEventListener('dblclick', handleDblClick)
  }
})
</script>

<style scoped>
.image-viewer {
  position: relative;
  width: 100%;
  min-height: 400px;
  max-height: 85vh;
  background: #0a0a0a;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  overflow: hidden;
}

.image-toolbar-floating {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  display: flex;
  gap: 8px;
  padding: 8px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  opacity: 0.8;
  transition: opacity 0.3s;
}

.image-viewer:hover .image-toolbar-floating {
  opacity: 1;
}

.image-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  user-select: none;
}

.image-loading,
.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #fff;
}

.image-loading .el-icon {
  font-size: 48px;
  color: #fff;
}

.image-error {
  color: #f56c6c;
}

.image-error .el-icon {
  font-size: 48px;
}

.image-content {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.2s ease-out;
  transform-origin: center;
  cursor: grab;
}

.image-content:active {
  cursor: grabbing;
}

/* 响应式 */
@media (max-width: 768px) {
  .image-toolbar-floating {
    top: 8px;
    right: 8px;
    padding: 4px;
  }
}
</style>

