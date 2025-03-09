import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { post, get, upload } from '@/utils/http'
import config from '@/config/env'
import { Message } from '@arco-design/web-vue'

// 定义类型
interface ChessNotation {
  id?: number;
  title: string;
  description?: string;
  moves: string;
  image_url?: string;
  created_at?: string;
  updated_at?: string;
  user_id?: number;
  tags?: string[];
  difficulty?: 'easy' | 'medium' | 'hard';
}

interface QueryParams {
  page: number;
  size: number;
  keyword?: string;
  tags?: string[];
  difficulty?: 'easy' | 'medium' | 'hard';
}

/**
 * 国际象棋状态管理
 */
export const useChessStore = defineStore('chess', () => {
  // 状态
  const notations = ref<ChessNotation[]>([])
  const currentNotation = ref<ChessNotation | null>(null)
  const loading = ref(false)
  const uploadLoading = ref(false)
  const parseLoading = ref(false)
  const total = ref(0)
  const queryParams = ref<QueryParams>({
    page: 1,
    size: 10
  })

  // 计算属性
  const hasMore = computed(() => {
    return total.value > notations.value.length
  })

  // 获取棋谱列表
  const getNotations = async (params?: Partial<QueryParams>) => {
    try {
      loading.value = true
      const mergedParams = { ...queryParams.value, ...params }
      queryParams.value = mergedParams

      const response = await get<{ data: ChessNotation[]; total: number }>(
        '/api/chess/notations',
        mergedParams
      )

      if (response) {
        notations.value = response.data
        total.value = response.total
      }

      return response
    } catch (error) {
      console.error('获取棋谱列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取更多棋谱
  const getMoreNotations = async () => {
    if (!hasMore.value || loading.value) return

    try {
      loading.value = true
      const nextPage = Math.ceil(notations.value.length / queryParams.value.size) + 1
      const params = { ...queryParams.value, page: nextPage }

      const response = await get<{ data: ChessNotation[]; total: number }>(
        '/api/chess/notations',
        params
      )

      if (response) {
        notations.value = [...notations.value, ...response.data]
        total.value = response.total
      }

      return response
    } catch (error) {
      console.error('获取更多棋谱失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 根据ID获取棋谱
  const getNotationById = async (id: number) => {
    try {
      loading.value = true
      const response = await get<ChessNotation>(`/api/chess/notations/${id}`)
      
      if (response) {
        currentNotation.value = response
      }
      
      return response
    } catch (error) {
      console.error('获取棋谱详情失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建棋谱
  const createNotation = async (notation: Partial<ChessNotation>) => {
    try {
      loading.value = true
      const response = await post<ChessNotation>('/api/chess/notations', notation)
      
      if (response) {
        // 更新列表
        await getNotations()
      }
      
      return response
    } catch (error) {
      console.error('创建棋谱失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 上传棋谱图片
  const uploadImage = async (file: File) => {
    try {
      uploadLoading.value = true
      
      // 验证文件类型
      const supportedImageFormats = config.getAllowedImageFormats()
      if (!supportedImageFormats.includes(file.type.split('/')[1])) {
        throw new Error(`不支持的文件类型: ${file.type}，请上传 JPG 或 PNG 格式的图片`)
      }
      
      // 验证文件大小
      const maxUploadSize = config.getMaxUploadSize() / (1024 * 1024) // 转换为MB
      const fileSize = file.size / 1024 / 1024 // 转换为MB
      if (fileSize > maxUploadSize) {
        throw new Error(`文件大小不能超过 ${maxUploadSize}MB`)
      }
      
      const result = await upload('/api/chess/upload', file, {
        validateFileType: false, // 已经手动验证过
        validateFileSize: false  // 已经手动验证过
      })
      
      return result
    } catch (error) {
      console.error('上传图片失败:', error)
      throw error
    } finally {
      uploadLoading.value = false
    }
  }

  // 解析棋谱
  const parseNotation = async (imageUrl: string, model: string) => {
    try {
      parseLoading.value = true
      
      const response = await post<{ moves: string }>(
        '/api/chess/parse',
        { image_url: imageUrl, model }
      )
      
      return response?.moves
    } catch (error) {
      console.error('解析棋谱失败:', error)
      throw error
    } finally {
      parseLoading.value = false
    }
  }

  // 重置状态
  const resetState = () => {
    notations.value = []
    currentNotation.value = null
    total.value = 0
    queryParams.value = {
      page: 1,
      size: 10
    }
  }

  return {
    // 状态
    notations,
    currentNotation,
    loading,
    uploadLoading,
    parseLoading,
    total,
    queryParams,
    
    // 计算属性
    hasMore,
    
    // 方法
    getNotations,
    getMoreNotations,
    getNotationById,
    createNotation,
    uploadImage,
    parseNotation,
    resetState
  }
})

export default useChessStore 