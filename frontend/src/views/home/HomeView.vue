<template>
  <div class="home-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="welcome-card">
          <template #title>
            <div class="flex items-center">
              <icon-home class="mr-2" />
              <span>欢迎使用家长助手</span>
            </div>
          </template>
          <div class="welcome-content">
            <h3 class="text-lg font-medium mb-4">{{ welcomeMessage }}</h3>
            <p class="text-gray-500 mb-6">家长助手是一款面向学生家长的工具集合平台，提供多种实用工具，帮助您更好地辅导孩子学习。</p>
            <a-button type="primary" @click="goToTools">
              <template #icon>
                <icon-right />
              </template>
              开始使用
            </a-button>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="24">
        <a-card class="tools-card">
          <template #title>
            <div class="flex items-center">
              <icon-tool class="mr-2" />
              <span>工具推荐</span>
            </div>
          </template>
          <a-row :gutter="[16, 16]">
            <a-col :span="8" v-for="tool in tools" :key="tool.id">
              <a-card class="tool-item" hoverable @click="navigateTo(tool.path)">
                <template #cover>
                  <div class="tool-icon flex justify-center items-center py-4">
                    <component :is="tool.icon" :style="{ fontSize: '48px', color: tool.color }" />
                  </div>
                </template>
                <a-card-meta :title="tool.name">
                  <template #description>
                    <p class="text-gray-500">{{ tool.description }}</p>
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import {
  IconHome,
  IconTool,
  IconRight,
  IconChess,
  IconCalendar,
  IconBook
} from '@arco-design/web-vue/es/icon'

// 路由
const router = useRouter()

// 用户状态
const userStore = useUserStore()

// 欢迎消息
const welcomeMessage = computed(() => {
  const username = userStore.userInfo?.name || userStore.userInfo?.username || '用户'
  return `${username}，欢迎回来！`
})

// 工具列表
const tools = ref([
  {
    id: 1,
    name: '国际象棋背谱工具',
    description: '上传棋谱图片，自动识别并练习',
    icon: IconChess,
    color: '#165DFF',
    path: '/chess'
  },
  {
    id: 2,
    name: '学习计划工具',
    description: '制定个性化学习计划，科学规划时间',
    icon: IconCalendar,
    color: '#00B42A',
    path: '/tools'
  },
  {
    id: 3,
    name: '知识点整理工具',
    description: '帮助整理学科知识点，构建知识体系',
    icon: IconBook,
    color: '#F53F3F',
    path: '/tools'
  }
])

// 跳转到工具中心
const goToTools = () => {
  router.push('/tools')
}

// 导航到指定路径
const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.home-container {
  padding: 16px;
}

.welcome-card {
  margin-bottom: 16px;
}

.welcome-content {
  padding: 16px 0;
}

.tool-item {
  transition: all 0.3s;
}

.tool-item:hover {
  transform: translateY(-5px);
}

.tool-icon {
  background-color: var(--color-fill-2);
}
</style> 