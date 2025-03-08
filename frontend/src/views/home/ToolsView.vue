<template>
  <div class="tools-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="tools-header">
          <template #title>
            <div class="flex items-center">
              <icon-tool class="mr-2" />
              <span>工具中心</span>
            </div>
          </template>
          <p class="text-gray-500">这里汇集了各种实用工具，帮助您更好地辅导孩子学习。</p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="24">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-apps class="mr-2" />
              <span>全部工具</span>
            </div>
          </template>
          <a-row :gutter="[16, 16]">
            <a-col :span="8" v-for="tool in tools" :key="tool.id">
              <a-card class="tool-item" hoverable @click="navigateTo(tool.path)">
                <template #cover>
                  <div class="tool-icon flex justify-center items-center py-6">
                    <component :is="tool.icon" :style="{ fontSize: '64px', color: tool.color }" />
                  </div>
                </template>
                <a-card-meta :title="tool.name">
                  <template #description>
                    <div>
                      <p class="text-gray-500 mb-2">{{ tool.description }}</p>
                      <a-tag v-if="tool.isNew" color="green">新</a-tag>
                      <a-tag v-if="tool.isHot" color="red">热门</a-tag>
                    </div>
                  </template>
                </a-card-meta>
              </a-card>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :span="24">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-bulb class="mr-2" />
              <span>工具推荐</span>
            </div>
          </template>
          <p>更多工具正在开发中，敬请期待...</p>
          <a-empty v-if="recommendations.length === 0" description="暂无推荐工具" />
          <a-row :gutter="[16, 16]" v-else>
            <a-col :span="8" v-for="tool in recommendations" :key="tool.id">
              <a-card class="tool-item" hoverable @click="navigateTo(tool.path)">
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  IconTool,
  IconApps,
  IconBulb,
  IconChess,
  IconCalendar,
  IconBook,
  IconEdit,
  IconMindMapping,
  IconCommon
} from '@arco-design/web-vue/es/icon'

// 路由
const router = useRouter()

// 工具列表
const tools = ref([
  {
    id: 1,
    name: '国际象棋背谱工具',
    description: '上传棋谱图片，自动识别并练习',
    icon: IconChess,
    color: '#165DFF',
    path: '/chess',
    isNew: true,
    isHot: true
  },
  {
    id: 2,
    name: '学习计划工具',
    description: '制定个性化学习计划，科学规划时间',
    icon: IconCalendar,
    color: '#00B42A',
    path: '/tools',
    isNew: false,
    isHot: false
  },
  {
    id: 3,
    name: '知识点整理工具',
    description: '帮助整理学科知识点，构建知识体系',
    icon: IconBook,
    color: '#F53F3F',
    path: '/tools',
    isNew: false,
    isHot: false
  },
  {
    id: 4,
    name: '作业批改工具',
    description: '利用AI辅助批改作业，提供详细反馈',
    icon: IconEdit,
    color: '#FF7D00',
    path: '/tools',
    isNew: false,
    isHot: false
  },
  {
    id: 5,
    name: '思维导图工具',
    description: '创建思维导图，梳理知识结构',
    icon: IconMindMapping,
    color: '#7B61FF',
    path: '/tools',
    isNew: false,
    isHot: false
  },
  {
    id: 6,
    name: '学习资源库',
    description: '汇集各学科优质学习资源',
    icon: IconCommon,
    color: '#86909C',
    path: '/tools',
    isNew: false,
    isHot: false
  }
])

// 推荐工具列表
const recommendations = ref([])

// 导航到指定路径
const navigateTo = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.tools-container {
  padding: 16px;
}

.tools-header {
  margin-bottom: 16px;
}

.tool-item {
  transition: all 0.3s;
  height: 100%;
}

.tool-item:hover {
  transform: translateY(-5px);
}

.tool-icon {
  background-color: var(--color-fill-2);
}
</style> 