<template>
  <div class="chess-list-container">
    <a-card class="chess-list-card">
      <template #title>
        <div class="card-title">
          <span>棋谱列表</span>
          <a-button type="primary" @click="router.push('/chess/upload')">
            <template #icon><icon-plus /></template>
            上传棋谱
          </a-button>
        </div>
      </template>
      
      <a-form :model="{}" class="search-form" layout="inline" @submit.prevent="handleSearch">
        <a-form-item field="keyword">
          <a-input v-model="searchKeyword" placeholder="搜索棋谱名称" allow-clear>
            <template #suffix><icon-search /></template>
          </a-input>
        </a-form-item>
        <a-form-item field="difficulty">
          <a-select v-model="filterDifficulty" placeholder="难度" allow-clear style="width: 120px">
            <a-option value="easy">简单</a-option>
            <a-option value="medium">中等</a-option>
            <a-option value="hard">困难</a-option>
          </a-select>
        </a-form-item>
        <a-form-item>
          <a-button type="primary" html-type="submit">搜索</a-button>
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
        :loading="loading"
        :data="chessNotations"
        :pagination="{
          total: pagination.total,
          current: pagination.current,
          pageSize: pagination.pageSize,
          showTotal: true,
          showPageSize: true
        }"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        :bordered="false"
        stripe
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
          
          <a-table-column title="上传时间" data-index="created_at">
            <template #cell="{ record }">
              {{ formatDate(record.created_at) }}
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
import http from '@/utils/http'

// 路由
const router = useRouter()

// 状态
const loading = ref(false)
const searchKeyword = ref('')
const filterDifficulty = ref('')
const chessNotations = ref<any[]>([])

// 分页
const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showTotal: true,
  showPageSize: true
})

// 获取难度颜色
const getDifficultyColor = (difficulty: string): string => {
  switch (difficulty) {
    case 'easy':
    case 'beginner':
      return 'green'
    case 'medium':
    case 'intermediate':
      return 'orange'
    case 'hard':
    case 'advanced':
      return 'red'
    default:
      return 'blue'
  }
}

// 获取难度文本
const getDifficultyText = (difficulty: string): string => {
  switch (difficulty) {
    case 'easy':
    case 'beginner':
      return '简单'
    case 'medium':
    case 'intermediate':
      return '中等'
    case 'hard':
    case 'advanced':
      return '困难'
    default:
      return '未知'
  }
}

// 格式化日期
const formatDate = (dateString: string): string => {
  if (!dateString) return '未知时间';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  } catch (e) {
    console.error('日期格式化错误:', e);
    return dateString;
  }
}

// 定义API响应类型
interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

interface ChessNotationItem {
  id: number;
  title: string;
  difficulty: string;
  created_at: string;
  updated_at: string;
  [key: string]: any;
}

// 加载棋谱数据
const loadChessNotations = async () => {
  loading.value = true
  try {
    // 构建查询参数
    const params = {
      page: pagination.current,
      size: pagination.pageSize,
      keyword: searchKeyword.value || undefined,
      difficulty: filterDifficulty.value || undefined
    }

    console.log('请求参数:', params)

    // 调用真实API获取棋谱数据
    const response = await http.get<ApiResponse<any>>('/api/chess/notations', params)
    
    console.log('API响应:', response)
    
    // 处理响应数据
    if (response && response.code === 200) {
      // 检查返回的数据类型
      if (response.data === null || response.data === undefined) {
        console.warn('API返回的数据为空')
        chessNotations.value = []
        pagination.total = 0
      } else if (Array.isArray(response.data)) {
        // 如果是数组，直接使用
        console.log('API返回数组数据:', response.data)
        chessNotations.value = response.data
        pagination.total = response.data.length
      } else if (typeof response.data === 'object' && response.data !== null) {
        // 如果是对象，检查是否有items和total字段
        if (Array.isArray(response.data.items)) {
          console.log('API返回对象数据，包含items数组:', response.data)
          chessNotations.value = response.data.items
          pagination.total = response.data.total || response.data.items.length
        } else if (Array.isArray(response.data.data)) {
          // 有些API会在data字段内再嵌套一层data
          console.log('API返回嵌套data数组:', response.data.data)
          chessNotations.value = response.data.data
          pagination.total = response.data.total || response.data.data.length
        } else {
          // 如果没有明确的数组字段，尝试将对象转为数组
          console.warn('API返回的数据结构不符合预期，尝试转换:', response.data)
          const entries = Object.entries(response.data)
            .filter(([key]) => !isNaN(Number(key)))
            .map(([_, value]) => value)
          
          if (entries.length > 0) {
            chessNotations.value = entries
            pagination.total = entries.length
          } else {
            chessNotations.value = []
            pagination.total = 0
          }
        }
      } else {
        console.error('API返回的数据格式不支持:', response.data)
        chessNotations.value = []
        pagination.total = 0
      }
      
      console.log('处理后的棋谱数据:', chessNotations.value)
    } else {
      console.error('加载棋谱数据失败:', response)
      Message.error(response?.message || '加载棋谱数据失败')
      chessNotations.value = []
      pagination.total = 0
    }
  } catch (error) {
    console.error('加载棋谱数据出错:', error)
    Message.error('加载棋谱数据失败')
    chessNotations.value = []
    pagination.total = 0
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.current = 1
  loadChessNotations()
}

// 删除棋谱
const handleDelete = async (id: number) => {
  Modal.warning({
    title: '确认删除',
    content: '确定要删除这个棋谱吗？此操作不可恢复。',
    okText: '确认',
    cancelText: '取消',
    onOk: async () => {
      try {
        // 调用真实API删除棋谱
        const response = await http.del<ApiResponse<any>>(`/api/chess/notations/${id}`)
        
        if (response && response.code === 200) {
          Message.success('删除成功')
          // 重新加载数据
          loadChessNotations()
        } else {
          console.error('删除棋谱失败:', response)
          Message.error(response?.message || '删除棋谱失败')
        }
      } catch (error) {
        console.error('删除棋谱出错:', error)
        Message.error('删除棋谱失败')
      }
    }
  })
}

// 页码变化
const onPageChange = (page: number) => {
  pagination.current = page
  loadChessNotations()
}

// 每页条数变化
const onPageSizeChange = (pageSize: number) => {
  pagination.pageSize = pageSize
  loadChessNotations()
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

.card-title {
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