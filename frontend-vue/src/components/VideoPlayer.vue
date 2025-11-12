<script setup lang="ts">
import Hls from 'hls.js'
import { onMounted, onBeforeUnmount, ref, watch, computed } from 'vue'
import { MediaAPI } from '@/api'
import { 
  VideoPlay, 
  VideoPause, 
  Mic, 
  Mute, 
  FullScreen,
  Setting,
  Monitor
} from '@element-plus/icons-vue'

const props = defineProps<{
  src?: string | null
  hls?: string | null
  poster?: string | null
  autoplay?: boolean
  controls?: boolean
  mediaToken?: string  // 媒体token，用于记录观看
}>()

const videoRef = ref<HTMLVideoElement | null>(null)
let hlsInstance: Hls | null = null
const hasRecordedWatch = ref(false)  // 标记是否已记录观看

// 播放控制状态
const isPlaying = ref(false)
const isMuted = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const buffered = ref(0)
const volume = ref(1)
const isFullscreen = ref(false)
const showControls = ref(false)  // 默认隐藏控制栏
const showSpeedMenu = ref(false)
const showQualityMenu = ref(false)

// 控制栏自动隐藏计时器
let hideControlsTimer: number | null = null

// 进度条拖动状态（提前声明，因为在 hideControls 中需要用到）
const isDragging = ref(false)

// 显示控制栏并设置自动隐藏
const showControlsTemporarily = () => {
  showControls.value = true
  
  // 清除之前的计时器
  if (hideControlsTimer) {
    clearTimeout(hideControlsTimer)
  }
  
  // 3秒后自动隐藏（仅在播放时）
  if (isPlaying.value) {
    hideControlsTimer = window.setTimeout(() => {
      showControls.value = false
    }, 3000)
  }
}

// 隐藏控制栏
const hideControls = () => {
  // 如果正在拖动进度条，不隐藏
  if (isDragging.value) return
  
  showControls.value = false
  if (hideControlsTimer) {
    clearTimeout(hideControlsTimer)
    hideControlsTimer = null
  }
}

// 处理视频容器鼠标移动
const handleContainerMouseMove = () => {
  showControlsTemporarily()
}

// 处理视频容器鼠标离开
const handleContainerMouseLeave = () => {
  hideControls()
}

// 播放速度选项
const playbackRates = [0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
const currentPlaybackRate = ref(1)

// 画质选项（如果HLS支持多个level）
const qualityLevels = ref<{ level: number; height: number; label: string }[]>([])
const currentQuality = ref(-1) // -1表示自动

const isHls = computed(() => !!props.hls && props.hls.endsWith('.m3u8'))

// 记录观看历史
const recordWatch = async () => {
  if (hasRecordedWatch.value || !props.mediaToken) {
    return  // 已记录过或没有token，不重复记录
  }
  
  try {
    hasRecordedWatch.value = true
    await MediaAPI.createUserMediaAction(props.mediaToken, 'watch')
    console.log('✅ 已记录观看历史')
  } catch (error) {
    console.error('❌ 记录观看历史失败:', error)
    hasRecordedWatch.value = false  // 失败时重置，允许重试
  }
}

// 播放控制函数
const togglePlay = () => {
  const video = videoRef.value
  if (!video) return
  
  if (video.paused) {
    video.play()
  } else {
    video.pause()
  }
}

const toggleMute = () => {
  const video = videoRef.value
  if (!video) return
  
  video.muted = !video.muted
  isMuted.value = video.muted
}

const setVolume = (val: number) => {
  const video = videoRef.value
  if (!video) return
  
  volume.value = val
  video.volume = val
  isMuted.value = val === 0
}

const setPlaybackRate = (rate: number) => {
  const video = videoRef.value
  if (!video) return
  
  video.playbackRate = rate
  currentPlaybackRate.value = rate
  showSpeedMenu.value = false
}

const setQuality = (level: number) => {
  if (!hlsInstance) return
  
  hlsInstance.currentLevel = level
  currentQuality.value = level
  showQualityMenu.value = false
}

const seekTo = (time: number) => {
  const video = videoRef.value
  if (!video) return
  
  video.currentTime = time
}

const toggleFullscreen = async () => {
  const video = videoRef.value
  if (!video) return
  
  try {
    if (!document.fullscreenElement) {
      await video.requestFullscreen()
      isFullscreen.value = true
    } else {
      await document.exitFullscreen()
      isFullscreen.value = false
    }
  } catch (error) {
    console.error('全屏切换失败:', error)
  }
}

// 画中画模式
const togglePictureInPicture = async () => {
  const video = videoRef.value
  if (!video) return
  
  try {
    if (document.pictureInPictureElement) {
      await document.exitPictureInPicture()
    } else {
      await video.requestPictureInPicture()
    }
  } catch (error) {
    console.error('画中画切换失败:', error)
  }
}

// 检查是否支持画中画
const supportsPictureInPicture = computed(() => {
  return 'pictureInPicture' in document
})

// 计算进度百分比
const playedPercent = computed(() => {
  if (!duration.value || !isFinite(duration.value)) return 0
  return (currentTime.value / duration.value) * 100
})

const bufferedPercent = computed(() => {
  if (!duration.value || !isFinite(duration.value)) return 0
  return (buffered.value / duration.value) * 100
})

// 进度条拖动相关状态（isDragging 已在前面声明）
const hoverTime = ref(0)
const hoverPercent = ref(0)
const showHoverTime = ref(false)

// 计算悬停位置的时间
const calculateTimeFromPosition = (event: MouseEvent, element: HTMLElement): number => {
  const rect = element.getBoundingClientRect()
  const percent = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width))
  return percent * duration.value
}

// 处理进度条悬停
const handleProgressHover = (event: MouseEvent) => {
  const progressBar = event.currentTarget as HTMLElement
  const time = calculateTimeFromPosition(event, progressBar)
  hoverTime.value = time
  
  const rect = progressBar.getBoundingClientRect()
  hoverPercent.value = Math.max(0, Math.min(100, ((event.clientX - rect.left) / rect.width) * 100))
  showHoverTime.value = true
}

// 处理进度条离开
const handleProgressLeave = () => {
  if (!isDragging.value) {
    showHoverTime.value = false
  }
}

// 处理进度条点击
const handleProgressClick = (event: MouseEvent) => {
  if (isDragging.value) return
  
  const progressBar = event.currentTarget as HTMLElement
  const newTime = calculateTimeFromPosition(event, progressBar)
  
  if (isFinite(newTime)) {
    seekTo(newTime)
  }
}

// 处理进度条拖动开始
const handleProgressMouseDown = (event: MouseEvent) => {
  isDragging.value = true
  const progressBar = event.currentTarget as HTMLElement
  const newTime = calculateTimeFromPosition(event, progressBar)
  
  if (isFinite(newTime)) {
    seekTo(newTime)
  }
  
  // 添加全局鼠标移动和松开事件
  document.addEventListener('mousemove', handleProgressMouseMove)
  document.addEventListener('mouseup', handleProgressMouseUp)
}

// 处理进度条拖动中
const handleProgressMouseMove = (event: MouseEvent) => {
  if (!isDragging.value) return
  
  const progressBarContainer = document.querySelector('.progress-bar') as HTMLElement
  if (!progressBarContainer) return
  
  const newTime = calculateTimeFromPosition(event, progressBarContainer)
  
  if (isFinite(newTime)) {
    seekTo(newTime)
  }
  
  // 更新悬停提示位置
  const rect = progressBarContainer.getBoundingClientRect()
  hoverPercent.value = Math.max(0, Math.min(100, ((event.clientX - rect.left) / rect.width) * 100))
  hoverTime.value = newTime
}

// 处理进度条拖动结束
const handleProgressMouseUp = () => {
  isDragging.value = false
  showHoverTime.value = false
  
  // 移除全局事件监听
  document.removeEventListener('mousemove', handleProgressMouseMove)
  document.removeEventListener('mouseup', handleProgressMouseUp)
}

// 更新视频状态
const updateVideoState = () => {
  const video = videoRef.value
  if (!video) return
  
  isPlaying.value = !video.paused
  currentTime.value = video.currentTime
  duration.value = video.duration
  
  // 更新缓冲进度
  if (video.buffered.length > 0) {
    buffered.value = video.buffered.end(video.buffered.length - 1)
  }
}

// 格式化时间显示
const formatTime = (seconds: number): string => {
  if (!isFinite(seconds) || isNaN(seconds)) return '00:00'
  
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

// 键盘快捷键处理
const handleKeyDown = (event: KeyboardEvent) => {
  const video = videoRef.value
  if (!video) return
  
  // 如果用户在输入框中，不处理快捷键
  const target = event.target as HTMLElement
  if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
    return
  }
  
  switch (event.code) {
    case 'Space':
      event.preventDefault()
      togglePlay()
      break
    case 'KeyK':
      event.preventDefault()
      togglePlay()
      break
    case 'ArrowLeft':
      event.preventDefault()
      seekTo(Math.max(0, currentTime.value - 10))
      break
    case 'ArrowRight':
      event.preventDefault()
      seekTo(Math.min(duration.value, currentTime.value + 10))
      break
    case 'KeyJ':
      event.preventDefault()
      seekTo(Math.max(0, currentTime.value - 10))
      break
    case 'KeyL':
      event.preventDefault()
      seekTo(Math.min(duration.value, currentTime.value + 10))
      break
    case 'ArrowUp':
      event.preventDefault()
      setVolume(Math.min(1, volume.value + 0.1))
      break
    case 'ArrowDown':
      event.preventDefault()
      setVolume(Math.max(0, volume.value - 0.1))
      break
    case 'KeyM':
      event.preventDefault()
      toggleMute()
      break
    case 'KeyF':
      event.preventDefault()
      toggleFullscreen()
      break
    case 'KeyP':
      event.preventDefault()
      if (supportsPictureInPicture.value) {
        togglePictureInPicture()
      }
      break
    case 'Digit0':
    case 'Numpad0':
      event.preventDefault()
      seekTo(0)
      break
    case 'Digit1':
    case 'Numpad1':
      event.preventDefault()
      seekTo(duration.value * 0.1)
      break
    case 'Digit2':
    case 'Numpad2':
      event.preventDefault()
      seekTo(duration.value * 0.2)
      break
    case 'Digit3':
    case 'Numpad3':
      event.preventDefault()
      seekTo(duration.value * 0.3)
      break
    case 'Digit4':
    case 'Numpad4':
      event.preventDefault()
      seekTo(duration.value * 0.4)
      break
    case 'Digit5':
    case 'Numpad5':
      event.preventDefault()
      seekTo(duration.value * 0.5)
      break
    case 'Digit6':
    case 'Numpad6':
      event.preventDefault()
      seekTo(duration.value * 0.6)
      break
    case 'Digit7':
    case 'Numpad7':
      event.preventDefault()
      seekTo(duration.value * 0.7)
      break
    case 'Digit8':
    case 'Numpad8':
      event.preventDefault()
      seekTo(duration.value * 0.8)
      break
    case 'Digit9':
    case 'Numpad9':
      event.preventDefault()
      seekTo(duration.value * 0.9)
      break
    case 'Home':
      event.preventDefault()
      seekTo(0)
      break
    case 'End':
      event.preventDefault()
      seekTo(duration.value)
      break
  }
}

function destroy() {
  if (hlsInstance) {
    hlsInstance.destroy()
    hlsInstance = null
  }
  
  // 清理事件监听
  const video = videoRef.value
  if (video) {
    video.removeEventListener('play', recordWatch)
    video.removeEventListener('timeupdate', updateVideoState)
    video.removeEventListener('loadedmetadata', updateVideoState)
    video.removeEventListener('progress', updateVideoState)
  }
  
  // 清理键盘事件监听
  document.removeEventListener('keydown', handleKeyDown)
}

function setup() {
  const video = videoRef.value
  if (!video) {
    console.error('❌ VideoPlayer: video元素未找到')
    return
  }

  console.log('🎬 VideoPlayer 开始设置:')
  console.log('  - HLS URL:', props.hls)
  console.log('  - 直接源URL:', props.src)
  console.log('  - 海报:', props.poster)
  console.log('  - 是否HLS:', isHls.value)
  console.log('  - HLS支持:', Hls.isSupported())
  console.log('  - 自动播放:', props.autoplay)
  console.log('  - 媒体Token:', props.mediaToken)
  
  // 监听播放事件，记录观看历史
  video.addEventListener('play', recordWatch, { once: false })
  video.addEventListener('timeupdate', updateVideoState)
  video.addEventListener('loadedmetadata', updateVideoState)
  video.addEventListener('progress', updateVideoState)
  video.addEventListener('volumechange', () => {
    if (video) {
      volume.value = video.volume
      isMuted.value = video.muted
    }
  })

  // 检查源URL是否是GIF文件（后端转码问题导致）
  const isGif = props.src?.toLowerCase().endsWith('.gif')
  if (isGif) {
    console.warn('⚠️ 检测到预览URL是GIF文件，这不是有效的视频格式')
    console.warn('⚠️ 这通常意味着视频转码未完成或配置问题')
    console.log('💡 将尝试使用其他可用源')
  }

  // 自动播放处理函数
  const handleAutoplay = async () => {
    if (props.autoplay && video) {
      try {
        // 尝试直接播放
        await video.play()
        console.log('✅ 视频自动播放成功')
      } catch (error) {
        // 如果失败，尝试静音后播放（浏览器策略要求）
        console.warn('⚠️ 自动播放失败，尝试静音播放:', error)
        video.muted = true
        try {
          await video.play()
          console.log('✅ 视频静音自动播放成功')
        } catch (mutedError) {
          console.error('❌ 静音自动播放也失败:', mutedError)
        }
      }
    }
  }

  if (isHls.value && Hls.isSupported() && props.hls) {
    console.log('✅ 使用HLS.js播放')
    destroy()
    hlsInstance = new Hls({
      debug: true,
      enableWorker: true
    })
    hlsInstance.loadSource(props.hls)
    hlsInstance.attachMedia(video)
    
    hlsInstance.on(Hls.Events.MANIFEST_PARSED, () => {
      console.log('✅ HLS manifest 解析成功')
      
      // 获取可用的画质级别
      const levels = hlsInstance!.levels
      if (levels && levels.length > 1) {
        qualityLevels.value = levels.map((level, index) => ({
          level: index,
          height: level.height,
          label: `${level.height}p`
        }))
        console.log('✅ 可用画质:', qualityLevels.value)
      }
      
      // HLS准备就绪后自动播放
      handleAutoplay()
    })
    
    hlsInstance.on(Hls.Events.ERROR, (event, data) => {
      console.error('❌ HLS播放错误:', data)
      if (data.fatal) {
        console.error('❌ 致命错误，类型:', data.type)
      }
    })
  } else if (props.hls && video.canPlayType('application/vnd.apple.mpegurl')) {
    console.log('✅ 使用Safari原生HLS播放')
    video.src = props.hls
    
    // Safari原生HLS加载完成后自动播放
    video.onloadeddata = () => {
      console.log('✅ 视频数据加载成功')
      handleAutoplay()
    }
  } else if (props.src && !isGif) {
    console.log('✅ 使用直接源播放:', props.src)
    video.src = props.src
    
    video.onerror = (e) => {
      console.error('❌ 视频加载错误:', e)
      console.error('  - 错误代码:', video.error?.code)
      console.error('  - 错误消息:', video.error?.message)
    }
    
    video.onloadeddata = () => {
      console.log('✅ 视频数据加载成功')
      handleAutoplay()
    }
  } else {
    console.warn('⚠️ 没有可用的视频源（HLS和预览URL都不可用）')
    console.log('💡 建议：')
    console.log('  1. 检查后端转码配置')
    console.log('  2. 确认 DO_NOT_TRANSCODE_VIDEO 设置')
    console.log('  3. 等待视频转码完成')
  }
}

onMounted(() => {
  setup()
  // 添加键盘事件监听
  document.addEventListener('keydown', handleKeyDown)
})

watch(() => [props.hls, props.src].join('|'), () => {
  destroy()
  setup()
})

onBeforeUnmount(() => {
  destroy()
  // 清理可能残留的拖动事件监听器
  document.removeEventListener('mousemove', handleProgressMouseMove)
  document.removeEventListener('mouseup', handleProgressMouseUp)
  // 清理控制栏隐藏计时器
  if (hideControlsTimer) {
    clearTimeout(hideControlsTimer)
  }
})
</script>

<template>
  <div 
    class="video-player-container"
    @mousemove="handleContainerMouseMove"
    @mouseleave="handleContainerMouseLeave"
  >
    <video
      ref="videoRef"
      :poster="poster || undefined"
      :autoplay="autoplay ?? false"
      :controls="false"
      class="video-element"
      @click="togglePlay"
    />
    
    <!-- 自定义控制栏 -->
    <div 
      v-show="showControls" 
      class="custom-controls"
    >
      <!-- 进度条 -->
      <div class="progress-bar-container">
        <div 
          class="progress-bar" 
          @click="handleProgressClick"
          @mousedown="handleProgressMouseDown"
          @mousemove="handleProgressHover"
          @mouseleave="handleProgressLeave"
        >
          <div class="progress-buffered" :style="{ width: bufferedPercent + '%' }"></div>
          <div class="progress-played" :style="{ width: playedPercent + '%' }"></div>
          <div class="progress-handle" :style="{ left: playedPercent + '%' }"></div>
          
          <!-- 悬停时间提示 -->
          <div 
            v-show="showHoverTime" 
            class="progress-time-tooltip"
            :style="{ left: hoverPercent + '%' }"
          >
            {{ formatTime(hoverTime) }}
          </div>
        </div>
      </div>
      
      <!-- 控制按钮栏 -->
      <div class="controls-bar">
        <div class="controls-left">
          <!-- 播放/暂停 -->
          <button class="control-btn" @click="togglePlay">
            <el-icon v-if="isPlaying"><VideoPause /></el-icon>
            <el-icon v-else><VideoPlay /></el-icon>
          </button>
          
          <!-- 音量 -->
          <div class="volume-control">
            <button class="control-btn" @click="toggleMute">
              <el-icon v-if="isMuted || volume === 0"><Mute /></el-icon>
              <el-icon v-else><Mic /></el-icon>
            </button>
            <div class="volume-slider">
              <input 
                type="range" 
                min="0" 
                max="1" 
                step="0.1"
                :value="volume"
                @input="(e) => setVolume(parseFloat((e.target as HTMLInputElement).value))"
              />
            </div>
          </div>
          
          <!-- 时间显示 -->
          <span class="time-display">
            {{ formatTime(currentTime) }} / {{ formatTime(duration) }}
          </span>
        </div>
        
        <div class="controls-right">
          <!-- 播放速度 -->
          <div class="speed-control">
            <button class="control-btn" @click="showSpeedMenu = !showSpeedMenu">
              <span class="speed-text">{{ currentPlaybackRate }}x</span>
            </button>
            <div v-show="showSpeedMenu" class="speed-menu">
              <div 
                v-for="rate in playbackRates" 
                :key="rate"
                class="speed-option"
                :class="{ active: currentPlaybackRate === rate }"
                @click="setPlaybackRate(rate)"
              >
                {{ rate }}x
              </div>
            </div>
          </div>
          
          <!-- 画质选择 (HLS) -->
          <div v-if="qualityLevels.length > 1" class="quality-control">
            <button class="control-btn" @click="showQualityMenu = !showQualityMenu">
              <el-icon><Setting /></el-icon>
            </button>
            <div v-show="showQualityMenu" class="quality-menu">
              <div 
                class="quality-option"
                :class="{ active: currentQuality === -1 }"
                @click="setQuality(-1)"
              >
                自动
              </div>
              <div 
                v-for="level in qualityLevels" 
                :key="level.level"
                class="quality-option"
                :class="{ active: currentQuality === level.level }"
                @click="setQuality(level.level)"
              >
                {{ level.label }}
              </div>
            </div>
          </div>
          
          <!-- 画中画 -->
          <button 
            v-if="supportsPictureInPicture" 
            class="control-btn" 
            @click="togglePictureInPicture"
            title="画中画 (P)"
          >
            <el-icon><Monitor /></el-icon>
          </button>
          
          <!-- 全屏 -->
          <button class="control-btn" @click="toggleFullscreen">
            <el-icon><FullScreen /></el-icon>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.video-player-container {
  position: relative;
  width: 100%;
  background: #000;
}

/* 播放时隐藏光标（鼠标不动3秒后） */
.video-player-container.hide-cursor {
  cursor: none;
}

.video-player-container.hide-cursor .video-element {
  cursor: none;
}

.video-element {
  width: 100%;
  height: auto;
  max-height: 85vh;
  background: #000;
  display: block;
  cursor: pointer;
}

/* 自定义控制栏 */
.custom-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, transparent 100%);
  padding: 20px 16px 12px;
  z-index: 10;
  pointer-events: auto;
}

/* 进度条 */
.progress-bar-container {
  margin-bottom: 12px;
}

.progress-bar {
  position: relative;
  width: 100%;
  height: 5px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  cursor: pointer;
  transition: height 0.2s;
  user-select: none;
}

.progress-bar:hover {
  height: 7px;
}

.progress-bar:active {
  cursor: grabbing;
}

.progress-buffered {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 3px;
  transition: width 0.3s;
}

.progress-played {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: #409eff;
  border-radius: 3px;
  transition: width 0.1s;
}

.progress-handle {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 12px;
  height: 12px;
  background: #fff;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.2s;
}

.progress-bar:hover .progress-handle {
  opacity: 1;
}

/* 时间提示 */
.progress-time-tooltip {
  position: absolute;
  bottom: 100%;
  transform: translateX(-50%);
  margin-bottom: 8px;
  padding: 4px 8px;
  background: rgba(28, 28, 28, 0.95);
  color: #fff;
  font-size: 12px;
  border-radius: 4px;
  white-space: nowrap;
  pointer-events: none;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.progress-time-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 4px solid transparent;
  border-top-color: rgba(28, 28, 28, 0.95);
}

/* 控制按钮栏 */
.controls-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.controls-left,
.controls-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.control-btn {
  padding: 4px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  width: 32px;
  height: 32px;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.05);
}

.speed-text {
  font-size: 12px;
  font-weight: 500;
  min-width: 28px;
  text-align: center;
  line-height: 1;
}

/* 音量控制 */
.volume-control {
  display: flex;
  align-items: center;
  gap: 6px;
}

.volume-slider {
  width: 0;
  overflow: hidden;
  transition: width 0.3s;
  display: flex;
  align-items: center;
}

.volume-control:hover .volume-slider {
  width: 70px;
}

.volume-slider input[type="range"] {
  width: 100%;
  height: 3px;
  -webkit-appearance: none;
  appearance: none;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}

.volume-slider input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 10px;
  height: 10px;
  background: #409eff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

.volume-slider input[type="range"]::-moz-range-thumb {
  width: 10px;
  height: 10px;
  background: #409eff;
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);
}

.volume-slider input[type="range"]::-webkit-slider-thumb:hover {
  background: #66b1ff;
  transform: scale(1.2);
}

.volume-slider input[type="range"]::-moz-range-thumb:hover {
  background: #66b1ff;
  transform: scale(1.2);
}

/* 时间显示 */
.time-display {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.9);
  font-variant-numeric: tabular-nums;
  min-width: 90px;
  padding: 0 4px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
  line-height: 20px;
}

/* 速度/画质菜单 */
.speed-control,
.quality-control {
  position: relative;
}

.speed-menu,
.quality-menu {
  position: absolute;
  bottom: 100%;
  right: 0;
  margin-bottom: 8px;
  background: rgba(28, 28, 28, 0.95);
  border-radius: 4px;
  padding: 4px 0;
  min-width: 80px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.speed-option,
.quality-option {
  padding: 8px 16px;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.speed-option:hover,
.quality-option:hover {
  background: rgba(255, 255, 255, 0.1);
}

.speed-option.active,
.quality-option.active {
  color: #409eff;
  background: rgba(64, 158, 255, 0.1);
}

/* 响应式 */
@media (max-width: 768px) {
  .time-display {
    display: none;
  }
  
  .volume-control:hover .volume-slider {
    width: 50px;
  }
  
  .control-btn {
    width: 28px;
    height: 28px;
    padding: 3px;
    font-size: 14px;
  }
  
  .controls-bar {
    gap: 6px;
  }
  
  .controls-left,
  .controls-right {
    gap: 4px;
  }
}
</style>
