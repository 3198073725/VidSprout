<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { MediaAPI, MiscAPI } from '@/api'
import type { MediaItem, Paginated } from '@/api'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const list = ref<Paginated<MediaItem> | null>(null)
const keyword = ref<string>((route.query.q as string) || '')

async function load() {
  loading.value = true
  try {
    if (keyword.value.trim()) {
      list.value = await MiscAPI.search({ q: keyword.value })
    } else {
      list.value = await MediaAPI.listMedia()
    }
  } finally {
    loading.value = false
  }
}

function openDetail(item: MediaItem) {
  router.push({ name: 'media-detail', params: { token: item.friendly_token } })
}

onMounted(load)

watch(
  () => route.query.q,
  (q) => {
    keyword.value = (q as string) || ''
    load()
  }
)
</script>

<template>
  <el-space direction="vertical" fill style="width:100%">
    <el-input v-model="keyword" placeholder="搜索媒体..." @keyup.enter.native="load">
      <template #append>
        <el-button type="primary" @click="load">搜索</el-button>
      </template>
    </el-input>

    <el-skeleton :loading="loading" animated>
      <template #template>
        <el-skeleton-item variant="image" style="width:100%;height:180px" />
      </template>
      <template #default>
        <div v-if="!keyword && (list?.results?.length ?? 0) === 0" class="mc-hero">
          <div class="mc-hero-title">Welcome to MediaCMS!</div>
          <div class="mc-hero-sub">Start uploading media and sharing your work!</div>
          <el-button type="success" size="large">UPLOAD MEDIA</el-button>
        </div>
        <div class="items-grid">
          <div
            v-for="item in (list?.results || [])"
            :key="item.friendly_token"
            class="item-thumb"
            @click="openDetail(item)"
          >
            <img class="thumb-image" :src="item.thumbnail_url || ''" alt="thumbnail" />
            <div class="thumb-body">
              <div class="thumb-title">{{ item.title }}</div>
              <div class="thumb-meta">{{ item.author_name }} · {{ item.views }} 次观看</div>
            </div>
          </div>
        </div>
      </template>
    </el-skeleton>
  </el-space>
</template>
