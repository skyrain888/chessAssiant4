<template>
  <div class="chess-detail-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="detail-header">
          <template #title>
            <div class="flex items-center">
              <icon-chess class="mr-2" />
              <span>棋谱详情</span>
            </div>
          </template>
          <p class="text-gray-500">查看棋谱的详细信息，包括棋谱步骤和分析。</p>
        </a-card>
      </a-col>
    </a-row>

    <div v-if="loading" class="py-8 text-center">
      <a-spin />
      <p class="mt-2 text-gray-500">加载中...</p>
    </div>

    <div v-else-if="!notation" class="py-8 text-center">
      <icon-exclamation-circle :style="{ fontSize: '32px', color: '#f53f3f' }" />
      <p class="mt-2 text-gray-500">未找到棋谱信息</p>
      <a-button class="mt-4" type="primary" @click="goBack">返回列表</a-button>
    </div>

    <template v-else>
      <a-row :gutter="16" class="mt-4">
        <a-col :xs="24" :md="16">
          <a-card>
            <template #title>
              <div class="flex items-center">
                <icon-dashboard class="mr-2" />
                <span>棋盘预览</span>
              </div>
            </template>
            <div class="chess-board-wrapper">
              <ChessBoard 
                :fen="initialFen" 
                :is-practice-mode="false"
                @board-ready="handleBoardReady"
              />
            </div>
            <div class="mt-4 flex justify-center">
              <a-space>
                <a-button type="primary" @click="goToViewer(notation.id)">
                  <template #icon><icon-eye /></template>
                  查看棋谱
                </a-button>
                <a-button status="success" @click="goToPractice(notation.id)">
                  <template #icon><icon-experiment /></template>
                  开始练习
                </a-button>
              </a-space>
            </div>
          </a-card>
        </a-col>
        <a-col :xs="24" :md="8">
          <a-card>
            <template #title>
              <div class="flex items-center">
                <icon-info-circle class="mr-2" />
                <span>棋谱信息</span>
              </div>
            </template>
            <div class="notation-info">
              <h2 class="text-xl font-bold">{{ notation.title }}</h2>
              
              <a-divider />
              
              <div class="info-item">
                <span class="info-label">难度：</span>
                <a-tag :color="getDifficultyColor(notation.difficulty)">
                  {{ getDifficultyText(notation.difficulty) }}
                </a-tag>
              </div>
              
              <div class="info-item">
                <span class="info-label">创建时间：</span>
                <span>{{ formatDate(notation.created_at) }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">更新时间：</span>
                <span>{{ formatDate(notation.updated_at) }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">标签：</span>
                <div class="flex flex-wrap">
                  <a-tag 
                    v-for="tag in notation.tags" 
                    :key="tag" 
                    color="arcoblue" 
                    class="mr-1 mb-1"
                  >
                    {{ tag }}
                  </a-tag>
                  <span v-if="!notation.tags || notation.tags.length === 0">
                    暂无标签
                  </span>
                </div>
              </div>
              
              <a-divider />
              
              <div class="info-item">
                <span class="info-label">描述：</span>
                <p class="mt-2 text-gray-600">{{ notation.description || '暂无描述' }}</p>
              </div>
            </div>
          </a-card>
          
          <a-card class="mt-4">
            <template #title>
              <div class="flex items-center">
                <icon-code-block class="mr-2" />
                <span>棋谱步骤</span>
              </div>
            </template>
            <a-scrollbar style="height: 200px; overflow: auto;">
              <pre class="notation-moves">{{ formatMoves(notation.moves) }}</pre>
            </a-scrollbar>
          </a-card>
          
          <a-card v-if="notation.image_url" class="mt-4">
            <template #title>
              <div class="flex items-center">
                <icon-image class="mr-2" />
                <span>棋谱图片</span>
              </div>
            </template>
            <div class="image-wrapper">
              <img :src="notation.image_url" alt="棋谱图片" class="notation-image" />
            </div>
          </a-card>
        </a-col>
      </a-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChessStore } from '@/stores/chessStore'
import { useNotification } from '@/composables/useNotification'
import ChessBoard from '@/components/chess/ChessBoard.vue'
import type { ChessNotation } from '@/types/custom-types'
import {
  IconChess,
  IconDashboard,
  IconInfoCircle,
  IconCodeBlock,
  IconImage,
  IconEye,
  IconExperiment,
  IconExclamationCircle
} from '@arco-design/web-vue/es/icon'

// 路由
const route = useRoute()
const router = useRouter()

// 状态管理
const chessStore = useChessStore()
const { error } = useNotification()

// 棋谱信息
const notation = ref<ChessNotation | null>(null)
const loading = ref(false)
const initialFen = ref('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

// 获取难度颜色
const getDifficultyColor = (difficulty?: string) => {
  switch (difficulty) {
    case 'easy': return 'green'
    case 'medium': return 'orange'
    case 'hard': return 'red'
    default: return 'gray'
  }
}

// 获取难度文本
const getDifficultyText = (difficulty?: string) => {
  switch (difficulty) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return '未知'
  }
}

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化棋谱步骤
const formatMoves = (moves: string) => {
  if (!moves) return ''
  
  // 简单格式化，可以根据需要调整
  return moves
    .replace(/(\d+\.)/g, '\n$1 ')  // 在回合数前添加换行
    .trim()
}

// 加载棋谱详情
const loadNotation = async (id: number) => {
  try {
    loading.value = true
    const result = await chessStore.getNotationById(id)
    if (result) {
      notation.value = result
    }
  } catch (err) {
    error('获取棋谱详情失败')
  } finally {
    loading.value = false
  }
}

// 处理棋盘准备就绪
const handleBoardReady = () => {
  console.log('棋盘准备就绪')
}

// 返回列表
const goBack = () => {
  router.push('/chess/list')
}

// 跳转到查看器
const goToViewer = (id: number) => {
  router.push(`/chess/viewer/${id}`)
}

// 跳转到练习页
const goToPractice = (id: number) => {
  router.push(`/chess/practice/${id}`)
}

// 组件挂载时加载数据
onMounted(async () => {
  const id = Number(route.params.id)
  if (!isNaN(id)) {
    await loadNotation(id)
  }
})
</script>

<style scoped>
.chess-detail-container {
  padding: 16px;
}

.detail-header {
  margin-bottom: 16px;
}

.chess-board-wrapper {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.notation-info {
  padding: 8px 0;
}

.info-item {
  margin-bottom: 16px;
}

.info-label {
  font-weight: 500;
  color: #4e5969;
  margin-right: 8px;
}

.notation-moves {
  font-family: monospace;
  white-space: pre-wrap;
  padding: 8px;
  background-color: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
}

.image-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.notation-image {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style> 