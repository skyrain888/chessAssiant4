<template>
  <div class="chess-board-container">
    <div class="chess-board" :class="{ 'practice-mode': isPracticeMode }">
      <div v-for="row in 8" :key="`row-${row}`" class="board-row">
        <div 
          v-for="col in 8" 
          :key="`col-${col}`" 
          class="board-cell"
          :class="{ 
            'cell-black': isBlackCell(row, col),
            'cell-white': !isBlackCell(row, col),
            'cell-selected': isSelectedCell(row, col),
            'cell-last-move': isLastMoveCell(row, col)
          }"
          @click="handleCellClick(row, col)"
        >
          <div 
            v-if="getPiece(row, col)" 
            class="chess-piece"
            :class="[`piece-${getPiece(row, col)?.color}`, `piece-${getPiece(row, col)?.type}`]"
            :draggable="!isPracticeMode || isPlayerTurn(getPiece(row, col)?.color)"
            @dragstart="handleDragStart($event, row, col)"
            @dragend="handleDragEnd"
          >
            {{ getPieceSymbol(getPiece(row, col)) }}
          </div>
        </div>
      </div>
    </div>
    
    <div class="board-coordinates">
      <div class="file-labels">
        <span v-for="file in files" :key="file">{{ file }}</span>
      </div>
      <div class="rank-labels">
        <span v-for="rank in ranks" :key="rank">{{ rank }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

// 定义棋子类型
interface ChessPiece {
  type: 'pawn' | 'knight' | 'bishop' | 'rook' | 'queen' | 'king'
  color: 'white' | 'black'
  position: { row: number; col: number }
}

// 定义棋盘类型
interface ChessBoard {
  [key: string]: ChessPiece | null
}

// 定义移动类型
interface ChessMove {
  from: { row: number; col: number }
  to: { row: number; col: number }
  piece: ChessPiece
  captured?: ChessPiece
  promotion?: 'queen' | 'rook' | 'bishop' | 'knight'
}

// 定义棋盘坐标
const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
const ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

// 定义棋子符号
const pieceSymbols = {
  'white-king': '♔',
  'white-queen': '♕',
  'white-rook': '♖',
  'white-bishop': '♗',
  'white-knight': '♘',
  'white-pawn': '♙',
  'black-king': '♚',
  'black-queen': '♛',
  'black-rook': '♜',
  'black-bishop': '♝',
  'black-knight': '♞',
  'black-pawn': '♟'
}

// 定义属性
const props = defineProps({
  fen: {
    type: String,
    default: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' // 初始局面
  },
  moves: {
    type: String,
    default: ''
  },
  isPracticeMode: {
    type: Boolean,
    default: false
  },
  currentMoveIndex: {
    type: Number,
    default: -1
  }
})

// 定义事件
const emit = defineEmits(['move', 'select-piece', 'board-ready'])

// 棋盘状态
const board = ref<ChessBoard>({})
const selectedCell = ref<{ row: number; col: number } | null>(null)
const lastMove = ref<ChessMove | null>(null)
const moveHistory = ref<ChessMove[]>([])
const currentTurn = ref<'white' | 'black'>('white')

// 初始化棋盘
const initBoard = () => {
  const newBoard: ChessBoard = {}
  
  // 清空棋盘
  for (let row = 1; row <= 8; row++) {
    for (let col = 1; col <= 8; col++) {
      const key = `${row}-${col}`
      newBoard[key] = null
    }
  }
  
  // 解析FEN字符串
  const fenParts = props.fen.split(' ')
  const fenBoard = fenParts[0]
  const rows = fenBoard.split('/')
  
  // 设置棋子
  for (let row = 0; row < 8; row++) {
    let col = 0
    for (let i = 0; i < rows[row].length; i++) {
      const char = rows[row][i]
      
      if ('12345678'.includes(char)) {
        // 数字表示空格数量
        col += parseInt(char)
      } else {
        // 字母表示棋子
        const pieceColor = char === char.toUpperCase() ? 'white' : 'black'
        let pieceType: ChessPiece['type'] = 'pawn'
        
        switch (char.toLowerCase()) {
          case 'p': pieceType = 'pawn'; break
          case 'n': pieceType = 'knight'; break
          case 'b': pieceType = 'bishop'; break
          case 'r': pieceType = 'rook'; break
          case 'q': pieceType = 'queen'; break
          case 'k': pieceType = 'king'; break
        }
        
        newBoard[`${row + 1}-${col + 1}`] = {
          type: pieceType,
          color: pieceColor,
          position: { row: row + 1, col: col + 1 }
        }
        
        col++
      }
    }
  }
  
  // 设置当前回合
  currentTurn.value = fenParts[1] === 'w' ? 'white' : 'black'
  
  board.value = newBoard
  emit('board-ready')
}

// 获取指定位置的棋子
const getPiece = (row: number, col: number): ChessPiece | null => {
  return board.value[`${row}-${col}`]
}

// 获取棋子符号
const getPieceSymbol = (piece: ChessPiece | null): string => {
  if (!piece) return ''
  return pieceSymbols[`${piece.color}-${piece.type}`] || ''
}

// 判断是否为黑色格子
const isBlackCell = (row: number, col: number): boolean => {
  return (row + col) % 2 === 1
}

// 判断是否为选中的格子
const isSelectedCell = (row: number, col: number): boolean => {
  return selectedCell.value?.row === row && selectedCell.value?.col === col
}

// 判断是否为最后一步移动的格子
const isLastMoveCell = (row: number, col: number): boolean => {
  if (!lastMove.value) return false
  
  return (
    (lastMove.value.from.row === row && lastMove.value.from.col === col) ||
    (lastMove.value.to.row === row && lastMove.value.to.col === col)
  )
}

// 判断是否为玩家回合
const isPlayerTurn = (color: string | undefined): boolean => {
  if (!color) return false
  return color === currentTurn.value
}

// 处理格子点击事件
const handleCellClick = (row: number, col: number) => {
  const clickedPiece = getPiece(row, col)
  
  // 如果已经选中了一个棋子，尝试移动
  if (selectedCell.value) {
    const selectedPiece = getPiece(selectedCell.value.row, selectedCell.value.col)
    
    // 如果点击的是同一个格子，取消选择
    if (selectedCell.value.row === row && selectedCell.value.col === col) {
      selectedCell.value = null
      return
    }
    
    // 如果点击的是同色棋子，更新选择
    if (clickedPiece && selectedPiece && clickedPiece.color === selectedPiece.color) {
      selectedCell.value = { row, col }
      emit('select-piece', { row, col, piece: clickedPiece })
      return
    }
    
    // 尝试移动棋子
    if (selectedPiece) {
      const move: ChessMove = {
        from: { row: selectedCell.value.row, col: selectedCell.value.col },
        to: { row, col },
        piece: { ...selectedPiece },
        captured: clickedPiece ? { ...clickedPiece } : undefined
      }
      
      // 在实际应用中，这里应该验证移动是否合法
      
      // 更新棋盘
      board.value[`${row}-${col}`] = {
        ...selectedPiece,
        position: { row, col }
      }
      board.value[`${selectedCell.value.row}-${selectedCell.value.col}`] = null
      
      // 更新状态
      lastMove.value = move
      moveHistory.value.push(move)
      selectedCell.value = null
      currentTurn.value = currentTurn.value === 'white' ? 'black' : 'white'
      
      // 触发移动事件
      emit('move', move)
    }
  } else if (clickedPiece) {
    // 如果是练习模式，只能移动当前回合的棋子
    if (props.isPracticeMode && clickedPiece.color !== currentTurn.value) {
      return
    }
    
    // 选中棋子
    selectedCell.value = { row, col }
    emit('select-piece', { row, col, piece: clickedPiece })
  }
}

// 处理拖拽开始事件
const handleDragStart = (event: DragEvent, row: number, col: number) => {
  const piece = getPiece(row, col)
  
  if (!piece) return
  
  // 如果是练习模式，只能移动当前回合的棋子
  if (props.isPracticeMode && piece.color !== currentTurn.value) {
    event.preventDefault()
    return
  }
  
  // 设置拖拽数据
  if (event.dataTransfer) {
    event.dataTransfer.setData('text/plain', JSON.stringify({ row, col }))
    event.dataTransfer.effectAllowed = 'move'
  }
  
  // 选中棋子
  selectedCell.value = { row, col }
  emit('select-piece', { row, col, piece })
}

// 处理拖拽结束事件
const handleDragEnd = () => {
  // 如果没有成功放置，取消选择
  setTimeout(() => {
    if (selectedCell.value) {
      selectedCell.value = null
    }
  }, 100)
}

// 监听当前移动索引变化
watch(() => props.currentMoveIndex, (newIndex: number) => {
  if (newIndex >= 0 && newIndex < moveHistory.value.length) {
    // 应用指定的移动
    const move = moveHistory.value[newIndex]
    lastMove.value = move
  } else if (newIndex === -1) {
    // 重置到初始状态
    initBoard()
    lastMove.value = null
  }
}, { immediate: true })

// 监听FEN变化
watch(() => props.fen, () => {
  initBoard()
  moveHistory.value = []
  lastMove.value = null
  selectedCell.value = null
}, { immediate: true })

// 组件挂载时初始化
onMounted(() => {
  initBoard()
})

// 导出方法
defineExpose({
  resetBoard: initBoard,
  getBoard: () => board.value,
  getMoveHistory: () => moveHistory.value
})
</script>

<style scoped>
.chess-board-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  position: relative;
}

.chess-board {
  width: 100%;
  aspect-ratio: 1 / 1;
  display: flex;
  flex-direction: column;
  border: 2px solid #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.board-row {
  display: flex;
  flex: 1;
}

.board-cell {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  cursor: pointer;
}

.cell-white {
  background-color: #f0d9b5;
}

.cell-black {
  background-color: #b58863;
}

.cell-selected {
  box-shadow: inset 0 0 0 4px rgba(0, 128, 255, 0.7);
}

.cell-last-move {
  background-color: rgba(255, 255, 0, 0.3);
}

.chess-piece {
  font-size: 2.5rem;
  cursor: grab;
  user-select: none;
  width: 80%;
  height: 80%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.chess-piece:active {
  cursor: grabbing;
}

.piece-white {
  color: #fff;
  text-shadow: 0 0 2px #000, 0 0 2px #000;
}

.piece-black {
  color: #000;
  text-shadow: 0 0 2px #fff, 0 0 2px #fff;
}

.board-coordinates {
  position: relative;
  width: 100%;
  height: 100%;
}

.file-labels {
  display: flex;
  justify-content: space-around;
  padding: 0 calc(100% / 16);
  width: 100%;
  position: absolute;
  bottom: -25px;
}

.rank-labels {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: calc(100% / 16) 0;
  height: 100%;
  position: absolute;
  left: -25px;
  top: 0;
}

.file-labels span, .rank-labels span {
  font-size: 14px;
  color: #666;
}

/* 练习模式样式 */
.practice-mode .chess-piece {
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .chess-piece {
    font-size: 2rem;
  }
  
  .file-labels, .rank-labels {
    display: none;
  }
}
</style> 