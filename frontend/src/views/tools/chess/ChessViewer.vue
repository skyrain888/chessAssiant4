<template>
  <div class="chess-viewer-container">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card class="viewer-header">
          <template #title>
            <div class="flex items-center">
              <icon-apps class="mr-2" />
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
              @invalid-move="handleInvalidMove"
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
                <div class="moves-grid">
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
import { Message } from '@arco-design/web-vue'
import ChessBoard from '@/components/chess/ChessBoard.vue'
import {
  IconApps,
  IconDashboard,
  IconCodeBlock,
  IconRefresh,
  IconLeft,
  IconRight,
  IconExperiment,
  IconInfoCircle
} from '@arco-design/web-vue/es/icon'

// 导入类型
import type { ChessNotation } from '@/stores/chessStore'

// 路由
const route = useRoute()

// 状态管理
const chessStore = useChessStore()

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
  
  if (parsedMoves.value.length === 0) {
    return result
  }
  
  try {
    // 按照国际象棋记谱法，每一回合包含白棋和黑棋的走法
    for (let i = 0; i < parsedMoves.value.length; i++) {
      const moveNumber = Math.floor(i / 2) + 1
      const isWhiteMove = i % 2 === 0
      
      if (isWhiteMove) {
        // 白棋走法: "1. e4"
        result.push(`${moveNumber}. ${parsedMoves.value[i]}`)
      } else {
        // 黑棋走法: "1... e5"
        result.push(`${moveNumber}... ${parsedMoves.value[i]}`)
      }
    }
  } catch (error) {
    console.error('格式化棋步时出错:', error)
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
  
  console.log('原始棋谱字符串:', movesString)
  
  try {
    // 首先处理换行符，将所有换行符替换为空格
    const normalizedString = movesString.replace(/\n/g, ' ')
    
    console.log('处理换行符后的棋谱字符串:', normalizedString)
    
    // 简单解析，移除回合数和注释
    const cleanedMoves = normalizedString
      .replace(/\{[^}]*\}/g, '') // 移除注释
      .replace(/\([^)]*\)/g, '') // 移除括号内容
      .replace(/\d+\./g, ' ') // 将回合数替换为空格
      .replace(/\s+/g, ' ') // 将多个空格替换为单个空格
      .trim()
    
    console.log('清理后的棋谱字符串:', cleanedMoves)
    
    // 分割成单独的步骤
    const moves = cleanedMoves.split(/\s+/).filter(move => move.length > 0 && move !== '...')
    
    console.log('解析后的棋步:', moves)
    return moves
  } catch (error) {
    console.error('解析棋谱失败:', error)
    return []
  }
}

// 加载棋谱
const loadNotation = async (id: number) => {
  try {
    const notation = await chessStore.getNotationById(id)
    console.log('获取到的棋谱数据:', notation)
    
    if (!notation) {
      Message.error('未找到棋谱数据')
      return
    }
    
    currentNotation.value = notation
    
    // 确保moves字段存在且有效
    if (!notation.moves) {
      Message.error('棋谱数据不完整，缺少走法信息')
      parsedMoves.value = []
    } else {
      try {
        // 处理不同格式的棋谱数据
        if (Array.isArray(notation.moves)) {
          // 如果moves已经是数组，直接使用
          console.log('棋谱数据是数组格式:', notation.moves)
          parsedMoves.value = notation.moves
          Message.success(`棋谱加载成功，共${notation.moves.length}步`)
        } else if (typeof notation.moves === 'string') {
          // 如果moves是字符串，解析它
          const moves = parseMoves(notation.moves)
          if (moves.length === 0) {
            Message.error('棋谱解析失败，未找到有效的走法')
          } else {
            parsedMoves.value = moves
            Message.success(`棋谱加载成功，共${moves.length}步`)
          }
        } else {
          // 其他情况
          console.error('未知的棋谱数据格式:', typeof notation.moves, notation.moves)
          Message.error('棋谱数据格式不正确')
          parsedMoves.value = []
        }
      } catch (parseError) {
        console.error('解析棋谱失败:', parseError)
        Message.error('解析棋谱失败，格式可能不正确')
        parsedMoves.value = []
      }
    }
    
    resetBoard()
  } catch (err) {
    console.error('加载棋谱失败:', err)
    Message.error('加载棋谱失败，请稍后重试')
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
  try {
    // 确保索引有效
    if (index >= 0 && index < formattedMoves.value.length) {
      // 由于formattedMoves是按照白黑棋交替排列的，需要转换回实际的棋步索引
      const actualIndex = Math.floor(index / 2) * 2 + (index % 2);
      
      // 确保不超出parsedMoves的范围
      if (actualIndex < parsedMoves.value.length) {
        currentMoveIndex.value = actualIndex;
        console.log(`跳转到第${actualIndex + 1}步: ${parsedMoves.value[actualIndex]}`);
      }
    }
  } catch (error) {
    console.error('跳转到指定步骤失败:', error);
  }
}

// 切换练习模式
const togglePracticeMode = () => {
  isPracticeMode.value = !isPracticeMode.value
  if (isPracticeMode.value) {
    Message.success('已进入练习模式，您可以自由移动棋子')
  }
}

// 处理棋子移动
const handleMove = (move: any) => {
  console.log('棋子移动:', move)
  
  if (!isPracticeMode.value) {
    // 非练习模式下，不允许移动棋子
    Message.error('请先点击"开始练习"按钮进入练习模式')
    return
  }
  
  // 获取当前应该执行的棋步
  const expectedMoveIndex = currentMoveIndex.value + 1
  if (expectedMoveIndex >= parsedMoves.value.length) {
    // 已经到达棋谱末尾
    Message.error('棋谱已经结束，没有更多步骤')
    // 不应用移动
    if (move.apply) {
      move.apply(false)
    }
    return
  }
  
  const expectedMove = parsedMoves.value[expectedMoveIndex]
  
  // 将移动转换为简单的代数记号进行比较
  const moveNotation = move.notation?.toLowerCase()
  console.log('当前移动:', moveNotation, '期望移动:', expectedMove)
  
  try {
    // 检查移动是否符合棋谱
    const isValid = moveNotation && isMatchingMove(moveNotation, expectedMove)
    
    if (isValid) {
      // 移动符合棋谱，更新当前步骤
      currentMoveIndex.value = expectedMoveIndex
      Message.success(`走法正确！(${expectedMove})`)
      
      // 应用移动
      if (move.apply) {
        move.apply(true)
      }
    } else {
      // 移动不符合棋谱
      Message.error(`走法错误！正确的走法应该是: ${expectedMove}`)
      
      // 不应用移动
      if (move.apply) {
        move.apply(false)
      }
    }
  } catch (err) {
    console.error('验证棋步时出错:', err)
    Message.error('验证棋步时出错，请重试')
    
    // 出错时不应用移动
    if (move.apply) {
      move.apply(false)
    }
  }
}

// 处理无效移动
const handleInvalidMove = (data: any) => {
  console.log('无效移动:', data)
  Message.error(data.message || '无效的移动')
}

// 检查移动是否匹配棋谱
const isMatchingMove = (moveNotation: string, expectedMove: string): boolean => {
  // 如果没有期望的移动，返回false
  if (!expectedMove) return false
  
  console.log('比较移动:', moveNotation, '与期望移动:', expectedMove)
  
  // 处理特殊情况：王车易位
  if (expectedMove.toLowerCase() === 'o-o' || expectedMove.toLowerCase() === '0-0') {
    // 短易位
    if (moveNotation.toLowerCase().includes('e1g1') || moveNotation.toLowerCase().includes('e8g8')) {
      return true
    }
  }
  
  if (expectedMove.toLowerCase() === 'o-o-o' || expectedMove.toLowerCase() === '0-0-0') {
    // 长易位
    if (moveNotation.toLowerCase().includes('e1c1') || moveNotation.toLowerCase().includes('e8c8')) {
      return true
    }
  }
  
  // 简化比较：移除所有非字母数字字符，并转为小写
  const simplifyNotation = (notation: string) => {
    return notation.replace(/[^a-zA-Z0-9]/g, '').toLowerCase()
  }
  
  // 提取代数记号中的目标格子
  const extractTargetSquare = (notation: string) => {
    // 尝试提取最后两个字符作为目标格子
    const simplified = simplifyNotation(notation)
    if (simplified.length >= 2) {
      return simplified.slice(-2)
    }
    return simplified
  }
  
  const simplifiedMove = simplifyNotation(moveNotation)
  const simplifiedExpected = simplifyNotation(expectedMove)
  
  // 提取目标格子
  const moveTarget = extractTargetSquare(moveNotation)
  const expectedTarget = extractTargetSquare(expectedMove)
  
  console.log('简化后的移动:', simplifiedMove, '简化后的期望移动:', simplifiedExpected)
  console.log('移动目标格:', moveTarget, '期望目标格:', expectedTarget)
  
  // 首先检查完整匹配
  if (simplifiedMove === simplifiedExpected) {
    return true
  }
  
  // 然后检查目标格子匹配
  if (moveTarget && expectedTarget && moveTarget === expectedTarget) {
    return true
  }
  
  // 最后检查部分包含关系
  return simplifiedMove.includes(simplifiedExpected) || simplifiedExpected.includes(simplifiedMove)
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

.moves-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.move-item {
  transition: background-color 0.2s;
}

.move-item:hover {
  background-color: #e5e7eb;
}

/* 修复红圈标注的样式问题 */
.board-coordinates {
  display: flex;
  justify-content: space-between;
  margin-top: 8px;
}

.file-labels {
  display: flex;
  justify-content: space-around;
  width: 100%;
}

.rank-labels {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 100%;
  position: absolute;
  left: -20px;
  top: 0;
}
</style> 