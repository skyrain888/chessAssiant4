<template>
  <div class="chess-list-container">
    <a-card class="chess-list-card">
      <template #title>
        <div class="list-header">
          <span>棋谱列表</span>
          <a-button type="primary" @click="router.push('/chess/upload')">
            <template #icon><icon-plus /></template>
            上传棋谱
          </a-button>
        </div>
      </template>
      
      <a-form layout="inline" class="search-form" @submit.prevent>
        <a-form-item>
          <a-input v-model="searchKeyword" placeholder="搜索棋谱名称" allow-clear>
            <template #prefix><icon-search /></template>
          </a-input>
        </a-form-item>
        
        <a-form-item>
          <a-select v-model="filterDifficulty" placeholder="难度" allow-clear style="width: 120px">
            <a-option value="easy">简单</a-option>
            <a-option value="medium">中等</a-option>
            <a-option value="hard">困难</a-option>
          </a-select>
        </a-form-item>
        
        <a-form-item>
          <a-button type="primary" @click="handleSearch">
            <template #icon><icon-search /></template>
            搜索
          </a-button>
        </a-form-item>
      </a-form>
      
      <div v-if="loading" class="loading-container">
        <a-spin />
        <p>加载中...</p>
      </div>
      
      <div v-else-if="chessNotations.length === 0" class="empty-container">
        <a-empty description="暂无棋谱数据" />
        <a-button type="primary" @click="router.push('/chess/upload')" class="mt-4">
          上传棋谱
        </a-button>
      </div>
      
      <a-table
        v-else
        :data="chessNotations"
        :pagination="pagination"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
      >
        <template #columns>
          <a-table-column title="名称" data-index="title">
            <template #cell="{ record }">
              <a @click="router.push(`/chess/detail/${record.id}`)">{{ record.title }}</a>
            </template>
          </a-table-column>
          
          <a-table-column title="难度" data-index="difficulty">
            <template #cell="{ record }">
              <a-tag :color="getDifficultyColor(record.difficulty)">
                {{ getDifficultyText(record.difficulty) }}
              </a-tag>
            </template>
          </a-table-column>
          
          <a-table-column title="上传时间" data-index="createdAt">
            <template #cell="{ record }">
              {{ formatDate(record.createdAt) }}
            </template>
          </a-table-column>
          
          <a-table-column title="操作">
            <template #cell="{ record }">
              <a-space>
                <a-button type="text" size="small" @click="router.push(`/chess/viewer/${record.id}`)">
                  <template #icon><icon-eye /></template>
                  查看
                </a-button>
                
                <a-button type="text" size="small" status="success" @click="router.push(`/chess/practice/${record.id}`)">
                  <template #icon><icon-play-circle /></template>
                  练习
                </a-button>
                
                <a-button type="text" size="small" status="danger" @click="handleDelete(record.id)">
                  <template #icon><icon-delete /></template>
                  删除
                </a-button>
              </a-space>
            </template>
          </a-table-column>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Message, Modal } from '@arco-design/web-vue'
import { IconPlus, IconSearch, IconEye, IconPlayCircle, IconDelete } from '@arco-design/web-vue/es/icon'

// 路由
const router = useRouter()

// 状态
const loading = ref(false)
const searchKeyword = ref('')
const filterDifficulty = ref('')
const chessNotations = ref([])

// 分页
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: true,
  showPageSize: true
})

// 获取难度颜色
const getDifficultyColor = (difficulty) => {
  switch (difficulty) {
    case 'easy': return 'green'
    case 'medium': return 'orange'
    case 'hard': return 'red'
    default: return 'gray'
  }
}

// 获取难度文本
const getDifficultyText = (difficulty) => {
  switch (difficulty) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return '未知'
  }
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// 加载棋谱数据
const loadChessNotations = async () => {
  loading.value = true
  
  try {
    // 模拟API调用
    setTimeout(() => {
      // 模拟数据
      const mockData = Array.from({ length: 20 }, (_, index) => ({
        id: index + 1,
        title: `棋谱示例 ${index + 1}`,
        difficulty: ['easy', 'medium', 'hard'][Math.floor(Math.random() * 3)],
        createdAt: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
      }))
      
      // 过滤数据
      let filteredData = [...mockData]
      
      if (searchKeyword.value) {
        filteredData = filteredData.filter(item => 
          item.title.toLowerCase().includes(searchKeyword.value.toLowerCase())
        )
      }
      
      if (filterDifficulty.value) {
        filteredData = filteredData.filter(item => 
          item.difficulty === filterDifficulty.value
        )
      }
      
      // 更新数据和分页
      pagination.total = filteredData.length
      
      const start = (pagination.current - 1) * pagination.pageSize
      const end = start + pagination.pageSize
      
      chessNotations.value = filteredData.slice(start, end)
      loading.value = false
    }, 500)
  } catch (error) {
    console.error('加载棋谱数据失败:', error)
    Message.error('加载棋谱数据失败')
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadChessNotations()
}

// 页码变化
const onPageChange = (page) => {
  pagination.current = page
  loadChessNotations()
}

// 每页条数变化
const onPageSizeChange = (pageSize) => {
  pagination.pageSize = pageSize
  loadChessNotations()
}

// 删除棋谱
const handleDelete = (id) => {
  Modal.warning({
    title: '确认删除',
    content: '确定要删除这个棋谱吗？此操作不可恢复。',
    okText: '确认',
    cancelText: '取消',
    onOk: () => {
      // 模拟删除操作
      setTimeout(() => {
        chessNotations.value = chessNotations.value.filter(item => item.id !== id)
        Message.success('删除成功')
      }, 500)
    }
  })
}

// 初始化
onMounted(() => {
  loadChessNotations()
})
</script>

<style scoped>
.chess-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.chess-list-card {
  margin-bottom: 24px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 24px;
}

.loading-container,
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
}

.loading-container p {
  margin-top: 16px;
  color: #86909c;
}

.mt-4 {
  margin-top: 16px;
}
</style> 