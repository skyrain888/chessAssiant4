<template>
  <div class="chess-container">
    <a-card class="chess-card">
      <template #title>国际象棋工具</template>
      
      <p class="chess-intro">
        欢迎使用国际象棋工具，这是一个专为学习和练习国际象棋设计的工具集合。
        您可以上传、管理和练习国际象棋棋谱，提高您的棋艺水平。
      </p>
      
      <a-divider />
      
      <div class="chess-features">
        <a-card class="feature-card" hoverable @click="router.push('/chess/list')">
          <template #cover>
            <div class="feature-icon">
              <i class="icon-list"></i>
            </div>
          </template>
          <a-card-meta title="棋谱列表">
            <template #description>
              <p>查看和管理您上传的所有棋谱</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="feature-card" hoverable @click="router.push('/chess/upload')">
          <template #cover>
            <div class="feature-icon">
              <i class="icon-upload"></i>
            </div>
          </template>
          <a-card-meta title="上传棋谱">
            <template #description>
              <p>上传新的国际象棋棋谱文件</p>
            </template>
          </a-card-meta>
        </a-card>
        
        <a-card class="feature-card" hoverable @click="handlePracticeClick">
          <template #cover>
            <div class="feature-icon">
              <i class="icon-practice"></i>
            </div>
          </template>
          <a-card-meta title="棋谱练习">
            <template #description>
              <p>练习和复盘您的棋谱</p>
            </template>
          </a-card-meta>
        </a-card>
      </div>
      
      <a-divider />
      
      <div class="chess-info">
        <h3>关于国际象棋工具</h3>
        <p>
          国际象棋工具支持上传PGN格式的棋谱文件，并提供棋谱查看、分析和练习功能。
          您可以通过练习模式测试自己的棋艺水平，系统会记录您的练习进度和正确率。
        </p>
        <p>
          如果您是新手，建议先从基础棋谱开始练习，逐步提高难度。
          如果您已经有一定棋艺基础，可以尝试更高级的棋谱和战术练习。
        </p>
      </div>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Message } from '@arco-design/web-vue'

const router = useRouter()
const userStore = useUserStore()

// 处理练习点击
const handlePracticeClick = () => {
  if (!userStore.isLoggedIn) {
    Message.warning('请先登录后再使用练习功能')
    router.push('/login?redirect=/chess/list')
    return
  }
  
  router.push('/chess/list')
}
</script>

<style scoped>
.chess-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.chess-card {
  margin-bottom: 24px;
}

.chess-intro {
  font-size: 16px;
  line-height: 1.6;
  color: #4e5969;
}

.chess-features {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin: 24px 0;
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

.icon-list::before {
  content: "📋";
  font-size: 48px;
}

.icon-upload::before {
  content: "📤";
  font-size: 48px;
}

.icon-practice::before {
  content: "🎮";
  font-size: 48px;
}

.chess-info {
  margin-top: 24px;
}

.chess-info h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
}

.chess-info p {
  font-size: 14px;
  line-height: 1.6;
  color: #4e5969;
  margin-bottom: 12px;
}
</style> 