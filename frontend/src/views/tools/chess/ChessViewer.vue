<template>
  <div class="chess-viewer-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="viewer-header">
          <template #title>
            <div class="flex items-center">
              <icon-chess class="mr-2" />
              <span>棋谱查看器</span>
            </div>
          </template>
          <p class="text-gray-500">查看和分析棋谱，练习国际象棋技巧。</p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" class="mt-4">
      <a-col :xs="24" :md="16">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-dashboard class="mr-2" />
              <span>棋盘</span>
            </div>
          </template>
          <div class="chess-board-wrapper">
            <ChessBoard 
              :fen="currentFen" 
              :current-move-index="currentMoveIndex"
              :is-practice-mode="isPracticeMode"
              @move="handleMove"
              @board-ready="handleBoardReady"
            />
          </div>
          <div class="controls mt-4">
            <a-space>
              <a-button type="primary" @click="resetBoard">
                <template #icon><icon-refresh /></template>
                重置
              </a-button>
              <a-button @click="prevMove" :disabled="currentMoveIndex <= 0">
                <template #icon><icon-left /></template>
                上一步
              </a-button>
              <a-button @click="nextMove" :disabled="currentMoveIndex >= parsedMoves.length - 1">
                <template #icon><icon-right /></template>
                下一步
              </a-button>
              <a-button status="success" @click="togglePracticeMode">
                <template #icon><icon-experiment /></template>
                {{ isPracticeMode ? '退出练习' : '开始练习' }}
              </a-button>
            </a-space>
          </div>
        </a-card>
      </a-col>
      <a-col :xs="24" :md="8">
        <a-card>
          <template #title>
            <div class="flex items-center">
              <icon-code-block class="mr-2" />
              <span>棋谱信息</span>
            </div>
          </template>
          <div v-if="currentNotation">
            <h3 class="text-lg font-bold">{{ currentNotation.title }}</h3>
            <p class="text-gray-500 mt-2">{{ currentNotation.description || '暂无描述' }}</p>
            
            <div class="mt-4">
              <div class="flex items-center">
                <span class="text-gray-500 mr-2">难度：</span>
                <a-tag :color="getDifficultyColor(currentNotation.difficulty)">
                  {{ getDifficultyText(currentNotation.difficulty) }}
                </a-tag>
              </div>
              
              <div class="flex items-center mt-2">
                <span class="text-gray-500 mr-2">标签：</span>
                <div>
                  <a-tag 
                    v-for="tag in currentNotation.tags" 
                    :key="tag" 
                    color="arcoblue" 
                    class="mr-1 mb-1"
                  >
                    {{ tag }}
                  </a-tag>
                  <span v-if="!currentNotation.tags || currentNotation.tags.length === 0">
                    暂无标签
                  </span>
                </div>
              </div>
            </div>
            
            <a-divider />
            
            <div class="moves-list">
              <h4 class="text-md font-bold mb-2">棋谱步骤</h4>
              <a-scrollbar style="height: 200px; overflow: auto;">
                <div class="grid grid-cols-2 gap-2">
                  <div 
                    v-for="(move, index) in formattedMoves" 
                    :key="index"
                    class="move-item p-1 rounded"
                    :class="{ 
                      'bg-blue-100': index === currentMoveIndex,
                      'cursor-pointer': true
                    }"
                    @click="jumpToMove(index)"
                  >
                    {{ move }}
                  </div>
                </div>
              </a-scrollbar>
            </div>
          </div>
          <div v-else class="text-center py-8">
            <icon-info-circle :style="{ fontSize: '32px', color: '#86909c' }" />
            <p class="mt-2 text-gray-500">请选择一个棋谱进行查看</p>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useChessStore } from '@/stores/chessStore'
import { useNotification } from '@/composables/useNotification'
import ChessBoard from '@/components/chess/ChessBoard.vue'
import type { ChessNotation } from '@/types/custom-types'
import {
  IconChess,
  IconDashboard,
  IconCodeBlock,
  IconRefresh,
  IconLeft,
  IconRight,
  IconExperiment,
  IconInfoCircle
} from '@arco-design/web-vue/es/icon'

// 路由
const route = useRoute()

// 状态管理
const chessStore = useChessStore()
const { success, error } = useNotification()

// 当前棋谱
const currentNotation = ref<ChessNotation | null>(null)

// 棋盘状态
const currentFen = ref('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
const currentMoveIndex = ref(-1)
const isPracticeMode = ref(false)

// 解析后的棋步
const parsedMoves = ref<string[]>([])

// 格式化后的棋步显示
const formattedMoves = computed(() => {
  const result: string[] = []
  let moveNumber = 1
  
  for (let i = 0; i < parsedMoves.value.length; i += 2) {
    // 白棋
    result.push(`${moveNumber}. ${parsedMoves.value[i] || ''}`)
    
    // 黑棋
    if (i + 1 < parsedMoves.value.length) {
      result.push(`${moveNumber}... ${parsedMoves.value[i + 1]}`)
    }
    
    moveNumber++
  }
  
  return result
})

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

// 加载棋谱
const loadNotation = async (id: number) => {
  try {
    const notation = await chessStore.getNotationById(id)
    if (notation) {
      currentNotation.value = notation
      parsedMoves.value = parseMoves(notation.moves)
      resetBoard()
      success('棋谱加载成功')
    }
  } catch (err) {
    error('加载棋谱失败')
  }
}

// 重置棋盘
const resetBoard = () => {
  currentFen.value = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
  currentMoveIndex.value = -1
}

// 上一步
const prevMove = () => {
  if (currentMoveIndex.value > 0) {
    currentMoveIndex.value--
  }
}

// 下一步
const nextMove = () => {
  if (currentMoveIndex.value < parsedMoves.value.length - 1) {
    currentMoveIndex.value++
  }
}

// 跳转到指定步骤
const jumpToMove = (index: number) => {
  currentMoveIndex.value = index
}

// 切换练习模式
const togglePracticeMode = () => {
  isPracticeMode.value = !isPracticeMode.value
  if (isPracticeMode.value) {
    success('已进入练习模式，您可以自由移动棋子')
  }
}

// 处理棋子移动
const handleMove = (move: any) => {
  // 在实际应用中，这里可以验证移动是否符合预期
  console.log('棋子移动:', move)
}

// 处理棋盘准备就绪
const handleBoardReady = () => {
  console.log('棋盘准备就绪')
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
.chess-viewer-container {
  padding: 16px;
}

.chess-board-wrapper {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.move-item {
  transition: background-color 0.2s;
}

.move-item:hover {
  background-color: #e5e7eb;
}
</style> 