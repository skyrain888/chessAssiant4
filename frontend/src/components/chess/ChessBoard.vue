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
  notation?: string // 添加代数记号
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
const emit = defineEmits(['move', 'select-piece', 'board-ready', 'invalid-move'])

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

// 验证移动是否合法
const isValidMove = (from: { row: number; col: number }, to: { row: number; col: number }, piece: ChessPiece): boolean => {
  // 如果不是练习模式，允许任何移动（用于演示）
  if (!props.isPracticeMode) {
    return true
  }
  
  // 不能移动到相同位置
  if (from.row === to.row && from.col === to.col) {
    return false
  }
  
  // 不能吃自己的棋子
  const targetPiece = getPiece(to.row, to.col)
  if (targetPiece && targetPiece.color === piece.color) {
    return false
  }
  
  // 根据棋子类型验证移动
  switch (piece.type) {
    case 'pawn':
      return isValidPawnMove(from, to, piece)
    case 'knight':
      return isValidKnightMove(from, to)
    case 'bishop':
      return isValidBishopMove(from, to)
    case 'rook':
      return isValidRookMove(from, to)
    case 'queen':
      return isValidQueenMove(from, to)
    case 'king':
      return isValidKingMove(from, to)
    default:
      return false
  }
}

// 验证兵的移动
const isValidPawnMove = (from: { row: number; col: number }, to: { row: number; col: number }, piece: ChessPiece): boolean => {
  const direction = piece.color === 'white' ? -1 : 1 // 白兵向上移动，黑兵向下移动
  const startRow = piece.color === 'white' ? 7 : 2 // 白兵起始行是7，黑兵起始行是2
  
  // 前进一格
  if (to.col === from.col && to.row === from.row + direction && !getPiece(to.row, to.col)) {
    return true
  }
  
  // 起始位置可以前进两格
  if (from.row === startRow && to.col === from.col && to.row === from.row + 2 * direction && 
      !getPiece(from.row + direction, from.col) && !getPiece(to.row, to.col)) {
    return true
  }
  
  // 斜向吃子
  if (Math.abs(to.col - from.col) === 1 && to.row === from.row + direction) {
    const targetPiece = getPiece(to.row, to.col)
    if (targetPiece && targetPiece.color !== piece.color) {
      return true
    }
    // TODO: 过路兵规则
  }
  
  return false
}

// 验证马的移动
const isValidKnightMove = (from: { row: number; col: number }, to: { row: number; col: number }): boolean => {
  const rowDiff = Math.abs(to.row - from.row)
  const colDiff = Math.abs(to.col - from.col)
  
  // 马走"日"字
  return (rowDiff === 2 && colDiff === 1) || (rowDiff === 1 && colDiff === 2)
}

// 验证象的移动
const isValidBishopMove = (from: { row: number; col: number }, to: { row: number; col: number }): boolean => {
  const rowDiff = Math.abs(to.row - from.row)
  const colDiff = Math.abs(to.col - from.col)
  
  // 象走斜线
  if (rowDiff !== colDiff) {
    return false
  }
  
  // 检查路径上是否有其他棋子
  const rowDirection = to.row > from.row ? 1 : -1
  const colDirection = to.col > from.col ? 1 : -1
  
  for (let i = 1; i < rowDiff; i++) {
    const checkRow = from.row + i * rowDirection
    const checkCol = from.col + i * colDirection
    if (getPiece(checkRow, checkCol)) {
      return false
    }
  }
  
  return true
}

// 验证车的移动
const isValidRookMove = (from: { row: number; col: number }, to: { row: number; col: number }): boolean => {
  // 车走直线
  if (from.row !== to.row && from.col !== to.col) {
    return false
  }
  
  // 检查路径上是否有其他棋子
  if (from.row === to.row) {
    // 水平移动
    const start = Math.min(from.col, to.col) + 1
    const end = Math.max(from.col, to.col)
    for (let col = start; col < end; col++) {
      if (getPiece(from.row, col)) {
        return false
      }
    }
  } else {
    // 垂直移动
    const start = Math.min(from.row, to.row) + 1
    const end = Math.max(from.row, to.row)
    for (let row = start; row < end; row++) {
      if (getPiece(row, from.col)) {
        return false
      }
    }
  }
  
  return true
}

// 验证后的移动
const isValidQueenMove = (from: { row: number; col: number }, to: { row: number; col: number }): boolean => {
  // 后可以走直线或斜线
  return isValidRookMove(from, to) || isValidBishopMove(from, to)
}

// 验证王的移动
const isValidKingMove = (from: { row: number; col: number }, to: { row: number; col: number }): boolean => {
  const rowDiff = Math.abs(to.row - from.row)
  const colDiff = Math.abs(to.col - from.col)
  
  // 王只能移动一格（暂不考虑王车易位）
  return rowDiff <= 1 && colDiff <= 1
}

// 将棋盘坐标转换为代数记号
const toAlgebraicNotation = (row: number, col: number): string => {
  return files[col - 1] + ranks[row - 1]
}

// 生成移动的代数记号
const generateMoveNotation = (move: ChessMove): string => {
  const from = toAlgebraicNotation(move.from.row, move.from.col)
  const to = toAlgebraicNotation(move.to.row, move.to.col)
  
  // 简单的代数记号
  return from + to
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
      // 验证移动是否合法
      if (!isValidMove(selectedCell.value, { row, col }, selectedPiece)) {
        emit('invalid-move', {
          from: selectedCell.value,
          to: { row, col },
          piece: selectedPiece,
          message: '无效的移动'
        })
        selectedCell.value = null
        return
      }
      
      const move: ChessMove = {
        from: { row: selectedCell.value.row, col: selectedCell.value.col },
        to: { row, col },
        piece: { ...selectedPiece },
        captured: clickedPiece ? { ...clickedPiece } : undefined
      }
      
      // 生成代数记号
      move.notation = generateMoveNotation(move)
      
      // 在练习模式下，先触发移动事件，让父组件验证是否符合棋谱
      if (props.isPracticeMode) {
        // 先触发移动事件，让父组件验证
        emit('move', {
          ...move,
          isValid: true, // 默认为有效，由父组件判断是否符合棋谱
          apply: (isValid: boolean) => {
            if (isValid) {
              // 如果移动有效，更新棋盘
              applyMove(move)
            }
            // 如果无效，不更新棋盘，只取消选择
            else {
              selectedCell.value = null
            }
          }
        })
      } else {
        // 非练习模式，直接应用移动
        applyMove(move)
        // 触发移动事件
        emit('move', move)
      }
    }
  } else if (clickedPiece) {
    // 如果是练习模式，只能移动当前回合的棋子
    if (props.isPracticeMode && clickedPiece.color !== currentTurn.value) {
      emit('invalid-move', {
        piece: clickedPiece,
        message: `现在是${currentTurn.value === 'white' ? '白' : '黑'}方回合`
      })
      return
    }
    
    // 选中棋子
    selectedCell.value = { row, col }
    emit('select-piece', { row, col, piece: clickedPiece })
  }
}

// 应用移动到棋盘
const applyMove = (move: ChessMove) => {
  // 更新棋盘
  board.value[`${move.to.row}-${move.to.col}`] = {
    ...move.piece,
    position: { row: move.to.row, col: move.to.col }
  }
  board.value[`${move.from.row}-${move.from.col}`] = null
  
  // 更新状态
  lastMove.value = move
  moveHistory.value.push(move)
  selectedCell.value = null
  currentTurn.value = currentTurn.value === 'white' ? 'black' : 'white'
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
  width: 100%;
  position: absolute;
  bottom: -25px;
  left: 0;
  padding: 0 calc(100% / 16);
}

.rank-labels {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  height: 100%;
  position: absolute;
  left: -25px;
  top: 0;
  padding: calc(100% / 16) 0;
}

.file-labels span, .rank-labels span {
  font-size: 14px;
  color: #666;
  font-weight: bold;
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