<template>
  <a href="#main-content" class="skip-link">
    跳转到主内容
  </a>
</template>

<script setup lang="ts">
// 这是一个可访问性组件，为键盘用户提供跳过导航的链接
</script>

<style scoped>
.skip-link {
  position: absolute;
  top: -40px;
  left: 6px;
  background: #000;
  color: #fff;
  padding: 8px;
  text-decoration: none;
  border-radius: 0 0 4px 4px;
  z-index: 1000;
  transition: top 0.3s;
  font-size: 14px;
}

.skip-link:focus {
  top: 0;
  outline: 2px solid #fff;
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .skip-link {
    transition: none;
  }
}
</style>