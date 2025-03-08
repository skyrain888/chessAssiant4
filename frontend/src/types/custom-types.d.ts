// 声明模块，解决导入问题
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 扩展通知组件类型
import { NotificationReturn } from '@arco-design/web-vue'

declare module '@/composables/useNotification' {
  export interface NotificationOptions {
    title: string
    content: string
    onOk?: () => void
    onCancel?: () => void
  }

  export interface NotificationInstance {
    success: (content: string, title?: string) => void
    error: (content: string, title?: string) => void
    warning: (content: string, title?: string) => void
    info: (content: string, title?: string) => void
    notify: (content: string, title: string, type?: 'info' | 'success' | 'warning' | 'error') => void
    confirm: (options: NotificationOptions) => NotificationReturn
  }

  export function useNotification(): NotificationInstance
}

// 棋谱相关类型
declare module '@/stores/chessStore' {
  /**
   * 棋谱信息接口
   */
  export interface ChessNotation {
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

  /**
   * 查询参数接口
   */
  export interface QueryParams {
    page: number
    size: number
    keyword?: string
    tags?: string[]
    difficulty?: string
  }
}

// 用户相关类型
declare module '@/stores/userStore' {
  export interface UserInfo {
    id: number
    username: string
    email: string
    name?: string
    avatar?: string
  }
} 