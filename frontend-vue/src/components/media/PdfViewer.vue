<template>
  <div class="pdf-viewer">
    <div class="pdf-toolbar">
      <div class="toolbar-left">
        <el-button-group>
          <el-button :disabled="currentPage <= 1" @click="prevPage" :icon="ArrowLeft">
            上一页
          </el-button>
          <el-button :disabled="currentPage >= totalPages" @click="nextPage" :icon="ArrowRight">
            下一页
          </el-button>
        </el-button-group>
        
        <div class="page-info">
          <el-input-number 
            v-model="currentPage" 
            :min="1" 
            :max="totalPages"
            controls-position="right"
            size="small"
            @change="renderPage"
            style="width: 100px;"
          />
          <span class="page-total"> / {{ totalPages }}</span>
        </div>
      </div>
      
      <div class="toolbar-center">
        <el-button-group>
          <el-button @click="zoomOut" :icon="ZoomOut" :disabled="scale <= 0.5">
            缩小
          </el-button>
          <el-button @click="resetZoom" :icon="FullScreen">
            {{ Math.round(scale * 100) }}%
          </el-button>
          <el-button @click="zoomIn" :icon="ZoomIn" :disabled="scale >= 3">
            放大
          </el-button>
        </el-button-group>
      </div>
      
      <div class="toolbar-right">
        <el-button @click="rotate" :icon="RefreshRight">
          旋转
        </el-button>
        <el-button @click="download" :icon="Download" type="primary">
          下载
        </el-button>
      </div>
    </div>
    
    <div class="pdf-container" ref="containerRef">
      <div v-if="loading" class="pdf-loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="error" class="pdf-error">
        <el-icon><WarningFilled /></el-icon>
        <p>{{ error }}</p>
      </div>
      
      <canvas 
        v-else
        ref="canvasRef" 
        class="pdf-canvas"
        :style="{
          transform: `rotate(${rotation}deg)`,
          transformOrigin: 'center'
        }"
      />
    </div>
    
    <!-- 缩略图侧边栏 -->
    <div v-if="showThumbnails && totalPages > 1" class="pdf-thumbnails">
      <div class="thumbnail-header">
        <h4>页面缩略图</h4>
        <el-button 
          :icon="Close" 
          circle 
          size="small" 
          @click="showThumbnails = false"
        />
      </div>
      <div class="thumbnail-list">
        <div 
          v-for="page in totalPages" 
          :key="page"
          class="thumbnail-item"
          :class="{ active: page === currentPage }"
          @click="goToPage(page)"
        >
          <div class="thumbnail-number">{{ page }}</div>
        </div>
      </div>
    </div>
    
    <el-button 
      v-if="totalPages > 1 && !showThumbnails"
      class="thumbnail-toggle"
      :icon="Menu"
      circle
      @click="showThumbnails = true"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { 
  ArrowLeft, 
  ArrowRight, 
  ZoomIn, 
  ZoomOut,
  FullScreen,
  RefreshRight,
  Download,
  Loading,
  WarningFilled,
  Close,
  Menu
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Props {
  src: string
  filename?: string
}

const props = defineProps<Props>()

const loading = ref(true)
const error = ref('')
const currentPage = ref(1)
const totalPages = ref(0)
const scale = ref(1.0)
const rotation = ref(0)
const showThumbnails = ref(false)

const canvasRef = ref<HTMLCanvasElement | null>(null)
const containerRef = ref<HTMLElement | null>(null)

let pdfDoc: any = null
let renderTask: any = null

// 加载PDF.js库
async function loadPDFJS() {
  try {
    // 使用CDN加载PDF.js
    const pdfjsLib = (window as any).pdfjsLib
    if (!pdfjsLib) {
      // 动态加载PDF.js
      const script = document.createElement('script')
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js'
      script.onload = () => {
        const lib = (window as any).pdfjsLib
        lib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'
        loadPDF()
      }
      document.head.appendChild(script)
    } else {
      pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js'
      loadPDF()
    }
  } catch (err) {
    error.value = 'PDF.js 加载失败'
    loading.value = false
  }
}

// 加载PDF文档
async function loadPDF() {
  try {
    const pdfjsLib = (window as any).pdfjsLib
    if (!pdfjsLib) {
      error.value = 'PDF.js 库未加载'
      loading.value = false
      return
    }
    
    const loadingTask = pdfjsLib.getDocument(props.src)
    pdfDoc = await loadingTask.promise
    totalPages.value = pdfDoc.numPages
    
    await renderPage(1)
    loading.value = false
  } catch (err) {
    console.error('PDF加载失败:', err)
    error.value = 'PDF文件加载失败，请检查文件是否有效'
    loading.value = false
  }
}

// 渲染页面
async function renderPage(pageNum?: number) {
  if (!pdfDoc || !canvasRef.value) return
  
  if (pageNum !== undefined) {
    currentPage.value = pageNum
  }
  
  try {
    // 取消之前的渲染任务
    if (renderTask) {
      renderTask.cancel()
    }
    
    const page = await pdfDoc.getPage(currentPage.value)
    const canvas = canvasRef.value
    const context = canvas.getContext('2d')
    
    const viewport = page.getViewport({ scale: scale.value })
    
    canvas.height = viewport.height
    canvas.width = viewport.width
    
    const renderContext = {
      canvasContext: context,
      viewport: viewport
    }
    
    renderTask = page.render(renderContext)
    await renderTask.promise
    renderTask = null
  } catch (err: any) {
    if (err.name !== 'RenderingCancelledException') {
      console.error('页面渲染失败:', err)
    }
  }
}

// 翻页功能
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    renderPage()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    renderPage()
  }
}

const goToPage = (page: number) => {
  currentPage.value = page
  renderPage()
  showThumbnails.value = false
}

// 缩放功能
const zoomIn = () => {
  if (scale.value < 3) {
    scale.value = Math.min(scale.value + 0.25, 3)
    renderPage()
  }
}

const zoomOut = () => {
  if (scale.value > 0.5) {
    scale.value = Math.max(scale.value - 0.25, 0.5)
    renderPage()
  }
}

const resetZoom = () => {
  scale.value = 1.0
  renderPage()
}

// 旋转功能
const rotate = () => {
  rotation.value = (rotation.value + 90) % 360
}

// 下载功能
const download = () => {
  const link = document.createElement('a')
  link.href = props.src
  link.download = props.filename || 'document.pdf'
  link.click()
  ElMessage.success('开始下载')
}

// 键盘快捷键
const handleKeydown = (e: KeyboardEvent) => {
  switch (e.key) {
    case 'ArrowLeft':
    case 'PageUp':
      e.preventDefault()
      prevPage()
      break
    case 'ArrowRight':
    case 'PageDown':
      e.preventDefault()
      nextPage()
      break
    case 'Home':
      e.preventDefault()
      goToPage(1)
      break
    case 'End':
      e.preventDefault()
      goToPage(totalPages.value)
      break
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
  }
}

// 监听src变化
watch(() => props.src, () => {
  loading.value = true
  error.value = ''
  currentPage.value = 1
  loadPDFJS()
})

onMounted(() => {
  loadPDFJS()
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  if (renderTask) {
    renderTask.cancel()
  }
})
</script>

<style scoped>
.pdf-viewer {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #f5f5f5;
  position: relative;
}

.pdf-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  flex-shrink: 0;
}

.toolbar-left,
.toolbar-center,
.toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.page-total {
  color: #666;
}

.pdf-container {
  flex: 1;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #e5e5e5;
}

.pdf-loading,
.pdf-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  color: #666;
}

.pdf-loading .el-icon {
  font-size: 48px;
}

.pdf-error {
  color: #f56c6c;
}

.pdf-error .el-icon {
  font-size: 48px;
}

.pdf-canvas {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  background: #fff;
  transition: transform 0.3s ease;
}

.pdf-thumbnails {
  position: absolute;
  right: 0;
  top: 61px;
  bottom: 0;
  width: 200px;
  background: #fff;
  border-left: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.thumbnail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #e4e7ed;
}

.thumbnail-header h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
}

.thumbnail-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.thumbnail-item {
  width: 100%;
  aspect-ratio: 1 / 1.414;
  background: #f5f5f5;
  border: 2px solid #e4e7ed;
  border-radius: 4px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumbnail-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.thumbnail-item.active {
  border-color: #409eff;
  background: #ecf5ff;
}

.thumbnail-number {
  font-size: 24px;
  font-weight: 600;
  color: #999;
}

.thumbnail-toggle {
  position: absolute;
  right: 16px;
  top: 80px;
  z-index: 5;
}

/* 暗黑模式 */
[data-theme="dark"] .pdf-viewer {
  background: #0a0a0a;
}

[data-theme="dark"] .pdf-toolbar {
  background: #1a1a1a;
  border-bottom-color: #333;
}

[data-theme="dark"] .pdf-container {
  background: #141414;
}

[data-theme="dark"] .pdf-thumbnails {
  background: #1a1a1a;
  border-left-color: #333;
}

[data-theme="dark"] .thumbnail-header {
  border-bottom-color: #333;
  color: #fff;
}

[data-theme="dark"] .thumbnail-item {
  background: #2a2a2a;
  border-color: #333;
}

[data-theme="dark"] .thumbnail-item:hover {
  border-color: #409eff;
}

[data-theme="dark"] .thumbnail-item.active {
  border-color: #409eff;
  background: #1a3a5a;
}

[data-theme="dark"] .thumbnail-number {
  color: #666;
}

[data-theme="dark"] .page-total {
  color: #999;
}

/* 响应式 */
@media (max-width: 768px) {
  .pdf-toolbar {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .toolbar-left,
  .toolbar-center,
  .toolbar-right {
    flex: 1 1 100%;
    justify-content: center;
  }
  
  .pdf-thumbnails {
    width: 150px;
  }
}
</style>

