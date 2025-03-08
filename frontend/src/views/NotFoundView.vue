<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1 class="text-6xl font-bold text-primary">404</h1>
      <h2 class="text-2xl font-medium mt-4">页面未找到</h2>
      <p class="text-gray-500 mt-2">抱歉，您访问的页面不存在或已被移除。</p>
      <a-button type="primary" class="mt-8" @click="goHome">
        <template #icon>
          <icon-home />
        </template>
        返回首页
      </a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { IconHome } from '@arco-design/web-vue/es/icon'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 60px - 48px);
  padding: 20px;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}
</style> 