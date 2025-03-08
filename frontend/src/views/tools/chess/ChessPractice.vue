<template>
  <div class="chess-practice-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="practice-header">
          <template #title>
            <div class="flex items-center">
              <icon-experiment class="mr-2" />
              <span>棋谱练习</span>
            </div>
          </template>
          <p class="text-gray-500">练习模式下，您可以自由移动棋子，系统会记录您的移动并与标准棋谱进行比较。</p>
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
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <icon-dashboard class="mr-2" />
                  <span>练习棋盘</span>
                </div>
                <a-tag :color="getDifficultyColor(notation.difficulty)">
                  {{ getDifficultyText(notation.difficulty) }}
                </a-tag>
              </div>
            </template>
            <div class="chess-board-wrapper">
              <ChessBoard 
                :fen="currentFen" 
                :is-practice-mode="true"
                @move="handleMove"
                @board-ready="handleBoardReady"
              />
            </div>
            <div class="mt-4">
              <a-space>
                <a-button type="primary" @click="resetBoard">
                  <template #icon><icon-refresh /></template>
                  重置棋盘
                </a-button>
                <a-button @click="showHint" :disabled="!canShowHint">
                  <template #icon><icon-bulb /></template>
                  提示
                </a-button>
                <a-button status="success" @click="checkProgress">
                  <template #icon><icon-check /></template>
                  检查进度
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
              <h2 class="text-lg font-bold">{{ notation.title }}</h2>
              <p class="text-gray-500 mt-2">{{ notation.description || '暂无描述' }}</p>
              
              <a-divider />
              
              <div class="info-item">
                <span class="info-label">您的进度：</span>
                <a-progress
                  :percent="progressPercent"
                  :stroke-color="getProgressColor(progressPercent)"
                  :status="progressPercent === 100 ? 'success' : 'normal'"
                />
              </div>
              
              <div class="info-item">
                <span class="info-label">当前步骤：</span>
                <span class="text-lg font-bold">{{ currentMoveIndex + 1 }} / {{ totalMoves }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">正确步骤：</span>
                <span class="text-green-500 font-bold">{{ correctMoves }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">错误步骤：</span>
                <span class="text-red-500 font-bold">{{ incorrectMoves }}</span>
              </div>
            </div>
          </a-card>
          
          <a-card class="mt-4">
            <template #title>
              <div class="flex items-center">
                <icon-history class="mr-2" />
                <span>移动历史</span>
              </div>
            </template>
            <a-scrollbar style="height: 200px; overflow: auto;">
              <div class="move-history">
                <div 
                  v-for="(move, index) in moveHistory" 
                  :key="index"
                  class="move-item"
                  :class="{ 
                    'move-correct': move.isCorrect === true,
                    'move-incorrect': move.isCorrect === false
                  }"
                >
                  <span class="move-number">{{ index + 1 }}.</span>
                  <span class="move-notation">{{ move.notation }}</span>
                  <span class="move-status">
                    <icon-check-circle-fill v-if="move.isCorrect === true" class="text-green-500" />
                    <icon-close-circle-fill v-if="move.isCorrect === false" class="text-red-500" />
                  </span>
                </div>
                <div v-if="moveHistory.length === 0" class="text-center py-4 text-gray-500">
                  尚未进行任何移动
                </div>
              </div>
            </a-scrollbar>
          </a-card>
          
          <a-card class="mt-4">
            <template #title>
              <div class="flex items-center">
                <icon-trophy class="mr-2" />
                <span>完成情况</span>
              </div>
            </template>
            <div class="completion-status">
              <div v-if="isCompleted" class="text-center py-4">
                <icon-check-circle-fill :style="{ fontSize: '32px', color: '#00b42a' }" />
                <p class="mt-2 text-lg font-bold text-green-500">恭喜！您已完成练习</p>
                <p class="text-gray-500">正确率: {{ accuracyPercent }}%</p>
                <a-button class="mt-4" type="primary" @click="goBack">
                  返回列表
                </a-button>
              </div>
              <div v-else class="text-center py-4 text-gray-500">
                继续练习，完成所有步骤
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useChessStore } from '@/stores/chessStore'
import { useNotification } from '@/composables/useNotification'
import ChessBoard from '@/components/chess/ChessBoard.vue'
import type { ChessNotation } from '@/types/custom-types'
import {
  IconExperiment,
  IconDashboard,
  IconInfoCircle,
  IconHistory,
  IconTrophy,
  IconRefresh,
  IconBulb,
  IconCheck,
  IconCheckCircleFill,
  IconCloseCircleFill,
  IconExclamationCircle
} from '@arco-design/web-vue/es/icon'

// 路由
const route = useRoute()
const router = useRouter()

// 状态管理
const chessStore = useChessStore()
const { success, error, info } = useNotification()

// 棋谱信息
const notation = ref<ChessNotation | null>(null)
const loading = ref(false)
const currentFen = ref('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

// 练习状态
const parsedMoves = ref<string[]>([])
const currentMoveIndex = ref(0)
const moveHistory = ref<Array<{
  notation: string
  isCorrect: boolean | null
}>>([])
const correctMoves = ref(0)
const incorrectMoves = ref(0)
const isCompleted = ref(false)
const canShowHint = ref(true)

// 计算总步骤数
const totalMoves = computed(() => parsedMoves.value.length)

// 计算进度百分比
const progressPercent = computed(() => {
  if (totalMoves.value === 0) return 0
  return Math.floor((currentMoveIndex.value / totalMoves.value) * 100)
})

// 计算正确率
const accuracyPercent = computed(() => {
  const total = correctMoves.value + incorrectMoves.value
  if (total === 0) return 0
  return Math.floor((correctMoves.value / total) * 100)
})

// 获取进度颜色
const getProgressColor = (percent: number) => {
  if (percent < 30) return '#ff4d4f'
  if (percent < 70) return '#faad14'
  return '#52c41a'
}

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

// 解析棋谱步骤
const parseMoves = (movesString: string) => {
  if (!movesString) return []
  
  // 简单解析，移除回合数和注释
  const cleanedMoves = movesString
    .replace(/\{[^}]*\}/g, '') // 移除注释
    .replace(/\([^)]*\)/g, '') // 移除括号内容
    .replace(/\d+\./g, '') // 移除回合数
    .trim()
  
  // 分割成单独的步骤
  return cleanedMoves.split(/\s+/).filter(move => move.length > 0)
}

// 加载棋谱详情
const loadNotation = async (id: number) => {
  try {
    loading.value = true
    const result = await chessStore.getNotationById(id)
    if (result) {
      notation.value = result
      parsedMoves.value = parseMoves(result.moves)
      resetBoard()
      success('棋谱加载成功')
    }
  } catch (err) {
    error('获取棋谱详情失败')
  } finally {
    loading.value = false
  }
}

// 处理棋子移动
const handleMove = (move: any) => {
  // 在实际应用中，这里应该验证移动是否符合预期
  const moveNotation = `${move.from.col}${move.from.row}-${move.to.col}${move.to.row}`
  
  // 检查是否是正确的移动
  const expectedMove = parsedMoves.value[currentMoveIndex.value]
  const isCorrect = moveNotation === expectedMove
  
  // 记录移动历史
  moveHistory.value.push({
    notation: moveNotation,
    isCorrect: isCorrect
  })
  
  // 更新统计
  if (isCorrect) {
    correctMoves.value++
    currentMoveIndex.value++
    success('正确的移动！')
    
    // 检查是否完成所有步骤
    if (currentMoveIndex.value >= totalMoves.value) {
      isCompleted.value = true
      success('恭喜！您已完成所有步骤')
    }
  } else {
    incorrectMoves.value++
    error('不正确的移动，请重试')
  }
}

// 处理棋盘准备就绪
const handleBoardReady = () => {
  console.log('棋盘准备就绪')
}

// 重置棋盘
const resetBoard = () => {
  currentFen.value = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
  currentMoveIndex.value = 0
  moveHistory.value = []
  correctMoves.value = 0
  incorrectMoves.value = 0
  isCompleted.value = false
  canShowHint.value = true
}

// 显示提示
const showHint = () => {
  if (currentMoveIndex.value < parsedMoves.value.length) {
    const nextMove = parsedMoves.value[currentMoveIndex.value]
    info(`下一步应该是: ${nextMove}`)
    canShowHint.value = false
    
    // 5分钟后重新启用提示
    setTimeout(() => {
      canShowHint.value = true
    }, 5 * 60 * 1000)
  }
}

// 检查进度
const checkProgress = () => {
  success(`当前进度: ${progressPercent.value}%, 正确率: ${accuracyPercent.value}%`)
}

// 返回列表
const goBack = () => {
  router.push('/chess/list')
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
.chess-practice-container {
  padding: 16px;
}

.practice-header {
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

.move-history {
  padding: 8px 0;
}

.move-item {
  display: flex;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #e5e6eb;
}

.move-item:last-child {
  border-bottom: none;
}

.move-number {
  width: 30px;
  font-weight: 500;
}

.move-notation {
  flex: 1;
  font-family: monospace;
}

.move-status {
  width: 24px;
  text-align: center;
}

.move-correct {
  background-color: rgba(0, 180, 42, 0.1);
}

.move-incorrect {
  background-color: rgba(245, 63, 63, 0.1);
}

.completion-status {
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style> 