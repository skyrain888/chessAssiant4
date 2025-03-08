<template>
  <div class="home-container">
    <a-card class="welcome-card">
      <template #title>
        <div class="welcome-header">
          <h2>欢迎使用家长助手</h2>
          <p>面向学生家长的工具集合平台</p>
        </div>
      </template>
      
      <div class="feature-grid">
        <a-card class="feature-card" hoverable @click="router.push('/chess')">
          <template #cover>
            <div class="feature-icon">
              <i class="icon-chess"></i>
            </div>
          </template>
          <a-card-meta title="国际象棋工具">
            <template #description>
              <p>上传、管理和练习国际象棋棋谱</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="feature-card" hoverable>
          <template #cover>
            <div class="feature-icon">
              <i class="icon-coming-soon"></i>
            </div>
          </template>
          <a-card-meta title="即将推出">
            <template #description>
              <p>更多实用工具正在开发中</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="feature-card" hoverable>
          <template #cover>
            <div class="feature-icon">
              <i class="icon-coming-soon"></i>
            </div>
          </template>
          <a-card-meta title="即将推出">
            <template #description>
              <p>更多实用工具正在开发中</p>
            </template>
          </a-card-meta>
        </a-card>
      </div>
    </a-card>
    
    <a-card class="info-card">
      <template #title>关于家长助手</template>
      <p>家长助手是一个面向学生家长的工具集合平台，旨在提供多种实用工具，帮助家长更好地辅导孩子学习。</p>
      <p>目前已实现国际象棋工具模块，支持棋谱上传、识别、查看和练习功能。</p>
      <p>更多功能正在开发中，敬请期待！</p>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 24px;
}

.welcome-header {
  text-align: center;
  margin-bottom: 24px;
}

.welcome-header h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.welcome-header p {
  color: #86909c;
  margin: 0;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.feature-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f2f3f5;
}

.icon-chess::before {
  content: "♞";
  font-size: 64px;
}

.icon-coming-soon::before {
  content: "⏳";
  font-size: 64px;
}

.info-card {
  margin-top: 24px;
}

@media (max-width: 768px) {
  .feature-grid {
    grid-template-columns: 1fr;
  }
}
</style> 