<template>
  <div class="virtual-scroll-container" ref="containerRef" @scroll="handleScroll">
    <div class="virtual-scroll-spacer" :style="spacerStyle"></div>
    <div class="virtual-scroll-content" :style="contentStyle">
      <slot :items="visibleItems" />
    </div>
  </div>
</template>

<script setup lang="ts" generic="T">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

interface Props {
  items: T[]
  itemHeight: number
  containerHeight?: number
  bufferSize?: number
  keyField?: string
}

const props = withDefaults(defineProps<Props>(), {
  containerHeight: 400,
  bufferSize: 5,
  keyField: 'id'
})

const emit = defineEmits<{
  scroll: [event: Event]
  visibleRangeChange: [start: number, end: number]
}>()

const containerRef = ref<HTMLElement>()
const scrollTop = ref(0)
const containerHeight = ref(props.containerHeight)

const totalHeight = computed(() => props.items.length * props.itemHeight)

const startIndex = computed(() => {
  const index = Math.floor(scrollTop.value / props.itemHeight)
  return Math.max(0, index - props.bufferSize)
})

const endIndex = computed(() => {
  const index = Math.ceil((scrollTop.value + containerHeight.value) / props.itemHeight)
  return Math.min(props.items.length, index + props.bufferSize)
})

const visibleItems = computed(() => {
  return props.items.slice(startIndex.value, endIndex.value)
})

const spacerStyle = computed(() => ({
  height: `${totalHeight.value}px`
}))

const contentStyle = computed(() => ({
  transform: `translateY(${startIndex.value * props.itemHeight}px)`,
  willChange: 'transform'
}))

const handleScroll = (event: Event) => {
  const target = event.target as HTMLElement
  scrollTop.value = target.scrollTop
  emit('scroll', event)
  emit('visibleRangeChange', startIndex.value, endIndex.value)
}

const updateContainerHeight = () => {
  if (containerRef.value) {
    containerHeight.value = containerRef.value.clientHeight
  }
}

const scrollToIndex = (index: number) => {
  if (containerRef.value) {
    const scrollPosition = index * props.itemHeight
    containerRef.value.scrollTop = scrollPosition
  }
}

const scrollToItem = (item: T) => {
  const index = props.items.findIndex(i => 
    (i as any)[props.keyField] === (item as any)[props.keyField]
  )
  if (index !== -1) {
    scrollToIndex(index)
  }
}

watch(visibleItems, () => {
  nextTick(() => {
    emit('visibleRangeChange', startIndex.value, endIndex.value)
  })
})

onMounted(() => {
  updateContainerHeight()
  window.addEventListener('resize', updateContainerHeight)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateContainerHeight)
})

defineExpose({
  scrollToIndex,
  scrollToItem,
  updateContainerHeight
})
</script>

<style scoped>
.virtual-scroll-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}

.virtual-scroll-spacer {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  pointer-events: none;
}

.virtual-scroll-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
}
</style>