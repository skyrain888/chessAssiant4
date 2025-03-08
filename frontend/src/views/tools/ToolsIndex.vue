<template>
  <div class="tools-container">
    <a-card class="tools-card">
      <template #title>工具中心</template>
      
      <div class="tools-grid">
        <a-card class="tool-card" hoverable @click="router.push('/chess')">
          <template #cover>
            <div class="tool-icon">
              <i class="icon-chess"></i>
            </div>
          </template>
          <a-card-meta title="国际象棋工具">
            <template #description>
              <p>上传、管理和练习国际象棋棋谱</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="tool-card" hoverable>
          <template #cover>
            <div class="tool-icon">
              <i class="icon-coming-soon"></i>
            </div>
          </template>
          <a-card-meta title="即将推出">
            <template #description>
              <p>更多实用工具正在开发中</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="tool-card" hoverable>
          <template #cover>
            <div class="tool-icon">
              <i class="icon-coming-soon"></i>
            </div>
          </template>
          <a-card-meta title="即将推出">
            <template #description>
              <p>更多实用工具正在开发中</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="tool-card" hoverable>
          <template #cover>
            <div class="tool-icon">
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
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.tools-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.tools-card {
  margin-bottom: 24px;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.tool-card {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.tool-card:hover {
  transform: translateY(-5px);
}

.tool-icon {
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
</style> 