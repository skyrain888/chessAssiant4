import { get, post, put, del, upload } from '@/utils/request'

// 定义接口类型
interface ChessNotation {
  id: number
  title: string
  description?: string
  moves: string
  image_url?: string
  created_at: string
  updated_at: string
  user_id: number
  tags?: string[]
  difficulty?: 'easy' | 'medium' | 'hard'
}

interface ChessNotationListResponse {
  code: number
  message: string
  data: {
    items: ChessNotation[]
    total: number
    page: number
    size: number
  }
}

interface ChessNotationResponse {
  code: number
  message: string
  data: ChessNotation
}

interface ChessNotationParams {
  title: string
  description?: string
  moves: string
  tags?: string[]
  difficulty?: 'easy' | 'medium' | 'hard'
}

interface ChessNotationQueryParams {
  page?: number
  size?: number
  keyword?: string
  tags?: string[]
  difficulty?: 'easy' | 'medium' | 'hard'
}

/**
 * 获取棋谱列表
 * @param params 查询参数
 */
export function getChessNotations(params: ChessNotationQueryParams = {}) {
  return get<ChessNotationListResponse>('/chess/notations', params)
}

/**
 * 获取棋谱详情
 * @param id 棋谱ID
 */
export function getChessNotation(id: number) {
  return get<ChessNotationResponse>(`/chess/notations/${id}`)
}

/**
 * 创建棋谱
 * @param params 棋谱参数
 */
export function createChessNotation(params: ChessNotationParams) {
  return post<ChessNotationResponse>('/chess/notations', params)
}

/**
 * 更新棋谱
 * @param id 棋谱ID
 * @param params 棋谱参数
 */
export function updateChessNotation(id: number, params: Partial<ChessNotationParams>) {
  return put<ChessNotationResponse>(`/chess/notations/${id}`, params)
}

/**
 * 删除棋谱
 * @param id 棋谱ID
 */
export function deleteChessNotation(id: number) {
  return del<{ code: number; message: string }>(`/chess/notations/${id}`)
}

/**
 * 上传棋谱图片
 * @param file 图片文件
 */
export function uploadChessImage(file: File) {
  return upload<{
    code: number
    message: string
    data: {
      image_url: string
      moves?: string
    }
  }>('/chess/upload', file)
}

/**
 * 解析棋谱
 * @param imageUrl 图片URL
 * @param model 使用的模型，可选值：gpt-4-vision, gemini-pro-vision等
 */
export function parseChessNotation(imageUrl: string, model: string = 'gpt-4-vision') {
  return post<{
    code: number
    message: string
    data: {
      moves: string
    }
  }>('/chess/parse', { image_url: imageUrl, model })
} 