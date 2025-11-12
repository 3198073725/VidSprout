<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { PlaylistsAPI } from '@/api'
import type { PlaylistDetail } from '@/api'
import { ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const loading = ref(false)
const list = ref<PlaylistDetail[]>([])
const dialog = ref(false)
const form = ref<{ title: string; description: string }>({ title: '', description: '' })

// 返回上一页
const handleBack = () => {
  router.back()
}

async function load() {
  loading.value = true
  try {
    const res = await PlaylistsAPI.listPlaylists()
    // API returns Paginated-like object per docs; normalize
    const results = (res as any).results || []
    list.value = results as any
  } finally {
    loading.value = false
  }
}

async function create() {
  if (!form.value.title) return
  await PlaylistsAPI.createPlaylist({ title: form.value.title, description: form.value.description })
  dialog.value = false
  form.value = { title: '', description: '' }
  await load()
}

function open(token: string) {
  router.push({ name: 'playlist-detail', params: { token } })
}

onMounted(load)
</script>

<template>
  <section class="home-sec">
    <div class="home-sec-head">
      <div class="home-sec-left">
        <el-button 
          :icon="ArrowLeft" 
          circle 
          @click="handleBack"
          class="back-button"
          title="返回"
        />
        <div class="home-sec-title">播放列表</div>
      </div>
      <el-button type="primary" @click="dialog = true">新建播放列表</el-button>
    </div>
    <el-skeleton :loading="loading" animated>
      <template #default>
        <div class="items-grid">
          <div v-for="pl in list" :key="pl.url" class="item-thumb" @click="open((pl as any).friendly_token || (pl as any).token || '')">
            <img class="thumb-image" :src="pl.thumbnail_url || ''" alt="thumbnail" />
            <div class="thumb-body">
              <div class="thumb-title">{{ pl.title }}</div>
              <div class="thumb-meta">{{ pl.media_count }} 项</div>
            </div>
          </div>
        </div>
      </template>
    </el-skeleton>

    <el-dialog v-model="dialog" title="新建播放列表" width="480px">
      <el-form @submit.prevent label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :disabled="!form.title" @click="create">创建</el-button>
      </template>
    </el-dialog>
  </section>
</template>

<style scoped>
.home-sec-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.back-button {
  flex-shrink: 0;
}

.home-sec-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
