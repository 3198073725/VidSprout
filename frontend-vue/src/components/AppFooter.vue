<script setup lang="ts">
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<template>
  <footer class="mc-footer">
    <div class="mc-footer-container">
      <div class="mc-footer-grid">
        <!-- 功能链接 -->
        <div class="mc-footer-column">
          <h4 class="mc-footer-title">功能</h4>
          <ul class="mc-footer-links">
            <li><router-link to="/upload">上传媒体</router-link></li>
            <li><router-link to="/latest">最新视频</router-link></li>
            <li><router-link to="/featured">精选内容</router-link></li>
            <li><router-link to="/categories">分类浏览</router-link></li>
          </ul>
        </div>
        
        <!-- 社区 -->
        <div class="mc-footer-column">
          <h4 class="mc-footer-title">社区</h4>
          <ul class="mc-footer-links">
            <li><router-link to="/members">成员列表</router-link></li>
            <li><router-link to="/tags">标签云</router-link></li>
          </ul>
        </div>
      </div>
      
      <!-- 版权信息 -->
      <div class="mc-footer-bottom">
        <p class="mc-footer-copyright">
          &copy; {{ currentYear }} 短视频平台. All rights reserved.
        </p>
        <p class="mc-footer-powered">
          Powered by <a href="https://github.com/mediacms-io/mediacms" target="_blank" rel="noopener">MediaCMS</a>
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.mc-footer {
  background: var(--mc-bg-secondary, #f5f5f5);
  border-top: 1px solid var(--mc-border-color, #e0e0e0);
  padding: 40px 20px 20px;
  margin-top: 60px;
}

.mc-footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.mc-footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 40px;
  margin-bottom: 40px;
}

.mc-footer-column {
  display: flex;
  flex-direction: column;
}

.mc-footer-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--mc-text-primary, #333);
  margin: 0 0 16px 0;
}

.mc-footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.mc-footer-links li {
  margin-bottom: 12px;
}

.mc-footer-links a {
  color: var(--mc-text-secondary, #666);
  text-decoration: none;
  font-size: 14px;
  transition: color 0.2s;
}

.mc-footer-links a:hover {
  color: var(--mc-primary, #2ecc71);
}

.mc-footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--mc-border-color, #e0e0e0);
}

.mc-footer-copyright,
.mc-footer-powered {
  font-size: 14px;
  color: var(--mc-text-secondary, #666);
  margin: 8px 0;
}

.mc-footer-powered a {
  color: var(--mc-primary, #2ecc71);
  text-decoration: none;
}

.mc-footer-powered a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .mc-footer {
    padding: 30px 16px 16px;
  }
  
  .mc-footer-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

@media (max-width: 480px) {
  .mc-footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
