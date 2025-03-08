<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1>404</h1>
      <h2>页面不存在</h2>
      <p>抱歉，您访问的页面不存在或已被移除</p>
      <a-button type="primary" @click="goHome">返回首页</a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

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
  min-height: 80vh;
}

.not-found-content {
  text-align: center;
}

.not-found-content h1 {
  font-size: 72px;
  font-weight: 700;
  color: #165DFF;
  margin: 0;
  line-height: 1.2;
}

.not-found-content h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 16px 0;
}

.not-found-content p {
  color: #86909c;
  margin-bottom: 24px;
}
</style> 