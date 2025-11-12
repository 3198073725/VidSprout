<template>
  <div class="lazy-image-container" ref="containerRef">
    <img
      v-if="loaded"
      :src="src"
      :alt="alt"
      :class="['lazy-image', { 'fade-in': loaded }]"
      @load="onImageLoad"
      @error="onImageError"
    />
    <div v-else-if="error" class="image-error">
      <el-icon><Picture /></el-icon>
      <span>加载失败</span>
    </div>
    <div v-else class="image-skeleton">
      <el-icon><Picture /></el-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Picture } from '@element-plus/icons-vue'

interface Props {
  src: string
  alt?: string
  threshold?: number
  rootMargin?: string
}

const props = withDefaults(defineProps<Props>(), {
  alt: '',
  threshold: 0.1,
  rootMargin: '50px'
})

const emit = defineEmits<{
  load: [event: Event]
  error: [event: Event]
}>()

const loaded = ref(false)
const error = ref(false)
const containerRef = ref<HTMLElement>()
let observer: IntersectionObserver | null = null

const onImageLoad = (event: Event) => {
  loaded.value = true
  emit('load', event)
}

const onImageError = (event: Event) => {
  error.value = true
  emit('error', event)
}

const setupIntersectionObserver = () => {
  if (!containerRef.value) return

  const options = {
    root: null,
    rootMargin: props.rootMargin,
    threshold: props.threshold
  }

  observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        loaded.value = true
        cleanup()
      }
    })
  }, options)

  observer.observe(containerRef.value)
}

const cleanup = () => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
}

watch(() => props.src, () => {
  loaded.value = false
  error.value = false
  setupIntersectionObserver()
})

onMounted(() => {
  setupIntersectionObserver()
})

onUnmounted(() => {
  cleanup()
})
</script>

<style scoped>
.lazy-image-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 200px;
  background-color: var(--el-fill-color-lighter);
  display: flex;
  align-items: center;
  justify-content: center;
}

.lazy-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
}

.lazy-image.fade-in {
  opacity: 1;
}

.image-skeleton,
.image-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.image-skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.image-error {
  background-color: var(--el-fill-color-lighter);
}
</style>