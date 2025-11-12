<script setup lang="ts">
import { InfoFilled, Platform, VideoCamera, User, Picture, Headset, Search, Share, Check } from '@element-plus/icons-vue'
</script>

<template>
  <section class="home-sec about-page">
    <div class="home-sec-head">
      <div class="home-sec-title">关于 MediaCMS</div>
    </div>
    
    <el-card class="about-hero">
      <div class="hero-content">
        <h1 class="platform-name">
          <el-icon class="logo-icon"><Platform /></el-icon>
          MediaCMS 媒体内容管理系统
        </h1>
        <p class="platform-desc">开源、高效、功能强大的媒体内容平台</p>
        <div class="tag-group">
          <el-tag type="primary" size="large">v1.0.0</el-tag>
          <el-tag type="success" size="large">开源项目</el-tag>
        </div>
      </div>
    </el-card>

    <el-row :gutter="20" class="feature-cards">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon" :size="32"><VideoCamera /></el-icon>
              <h3>视频管理</h3>
            </div>
          </template>
          <p>支持多种视频格式上传、自动转码、在线编辑。提供视频分类、标签和隐私设置。</p>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon" :size="32"><Picture /></el-icon>
              <h3>图片音频</h3>
            </div>
          </template>
          <p>支持图片展示、缩放旋转功能。音频播放、PDF 文档在线预览。</p>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon" :size="32"><Search /></el-icon>
              <h3>智能搜索</h3>
            </div>
          </template>
          <p>强大的全文搜索功能，支持中文分词。可按分类、标签、作者筛选。</p>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card shadow="hover" class="feature-card">
          <template #header>
            <div class="feature-header">
              <el-icon class="feature-icon" :size="32"><User /></el-icon>
              <h3>用户系统</h3>
            </div>
          </template>
          <p>完善的用户中心、播放列表管理、观看历史、点赞收藏等功能。</p>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="tech-stack">
      <template #header>
        <h3>技术栈</h3>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="前端框架">Vue 3 + TypeScript</el-descriptions-item>
        <el-descriptions-item label="UI 组件库">Element Plus</el-descriptions-item>
        <el-descriptions-item label="状态管理">Pinia</el-descriptions-item>
        <el-descriptions-item label="路由">Vue Router 4</el-descriptions-item>
        <el-descriptions-item label="后端框架">Django 4 + Django REST Framework</el-descriptions-item>
        <el-descriptions-item label="数据库">PostgreSQL</el-descriptions-item>
        <el-descriptions-item label="视频处理">FFmpeg</el-descriptions-item>
        <el-descriptions-item label="任务队列">Celery + Redis</el-descriptions-item>
        <el-descriptions-item label="PDF 预览">PDF.js</el-descriptions-item>
        <el-descriptions-item label="搜索引擎">PostgreSQL Full Text Search</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="features-list">
      <template #header>
        <h3>主要功能</h3>
      </template>
      <el-row :gutter="16">
        <el-col :xs="24" :sm="12">
          <ul class="feature-list">
            <li><el-icon><Check /></el-icon> 媒体上传与自动转码</li>
            <li><el-icon><Check /></el-icon> 视频、音频、图片、PDF 支持</li>
            <li><el-icon><Check /></el-icon> 分类和标签管理</li>
            <li><el-icon><Check /></el-icon> 隐私设置（公开/私密/链接）</li>
            <li><el-icon><Check /></el-icon> 播放列表管理</li>
            <li><el-icon><Check /></el-icon> 评论系统（支持回复）</li>
            <li><el-icon><Check /></el-icon> 点赞和收藏功能</li>
          </ul>
        </el-col>
        <el-col :xs="24" :sm="12">
          <ul class="feature-list">
            <li><el-icon><Check /></el-icon> 观看历史记录</li>
            <li><el-icon><Check /></el-icon> 智能推荐算法</li>
            <li><el-icon><Check /></el-icon> 全文搜索（支持中文）</li>
            <li><el-icon><Check /></el-icon> 用户主页</li>
            <li><el-icon><Check /></el-icon> 夜间模式</li>
            <li><el-icon><Check /></el-icon> 响应式设计</li>
            <li><el-icon><Check /></el-icon> RESTful API</li>
          </ul>
        </el-col>
      </el-row>
    </el-card>
  </section>
</template>

<style scoped>
.about-page {
  max-width: 1000px;
  margin: 0 auto;
}

.about-hero {
  text-align: center;
  margin-bottom: 32px;
}

.hero-content {
  padding: 40px 20px;
}

.platform-name {
  font-size: 36px;
  font-weight: 700;
  color: var(--el-color-primary);
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

[data-theme="dark"] .platform-name {
  color: #4a9eff;
}

.logo-icon {
  font-size: 42px;
}

.platform-desc {
  font-size: 18px;
  color: var(--el-text-color-secondary);
  margin-bottom: 24px;
}

[data-theme="dark"] .platform-desc {
  color: #cccccc;
}

.tag-group {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.feature-cards {
  margin-bottom: 32px;
}

.feature-card {
  height: 100%;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

[data-theme="dark"] .feature-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.feature-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

[data-theme="dark"] .feature-header h3 {
  color: #ffffff;
}

.feature-icon {
  color: var(--el-color-primary);
}

[data-theme="dark"] .feature-icon {
  color: #4a9eff;
}

.feature-card p {
  color: var(--el-text-color-secondary);
  line-height: 1.6;
  margin: 0;
}

[data-theme="dark"] .feature-card p {
  color: #cccccc;
}

.tech-stack {
  margin-bottom: 32px;
}

.tech-stack h3,
.features-list h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

[data-theme="dark"] .tech-stack h3,
[data-theme="dark"] .features-list h3 {
  color: #ffffff;
}

.features-list .feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.features-list .feature-list li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--el-border-color-lighter);
  color: var(--el-text-color-regular);
  font-size: 15px;
}

.features-list .feature-list li:last-child {
  border-bottom: none;
}

.features-list .feature-list li .el-icon {
  color: var(--el-color-success);
  font-size: 18px;
  flex-shrink: 0;
}

/* 暗色模式 - 卡片 */
[data-theme="dark"] .about-hero :deep(.el-card),
[data-theme="dark"] .feature-cards :deep(.el-card),
[data-theme="dark"] .tech-stack :deep(.el-card),
[data-theme="dark"] .features-list :deep(.el-card) {
  background: #1a1a1a !important;
  border-color: #333 !important;
}

[data-theme="dark"] .about-hero :deep(.el-card__body),
[data-theme="dark"] .feature-cards :deep(.el-card__body),
[data-theme="dark"] .tech-stack :deep(.el-card__body),
[data-theme="dark"] .features-list :deep(.el-card__body) {
  background: #1a1a1a !important;
}

[data-theme="dark"] .about-hero :deep(.el-card__header),
[data-theme="dark"] .feature-cards :deep(.el-card__header),
[data-theme="dark"] .tech-stack :deep(.el-card__header),
[data-theme="dark"] .features-list :deep(.el-card__header) {
  background: #1a1a1a !important;
  border-color: #333 !important;
}

[data-theme="dark"] .features-list .feature-list li {
  border-bottom-color: #333;
  color: #cccccc;
}

[data-theme="dark"] .features-list .feature-list li .el-icon {
  color: #67c23a;
}

@media (max-width: 768px) {
  .platform-name {
    font-size: 24px;
  }
  
  .platform-desc {
    font-size: 16px;
  }
  
  .feature-cards :deep(.el-col) {
    margin-bottom: 16px;
  }
  
  .features-list :deep(.el-col) {
    margin-bottom: 20px;
  }
}
</style>
