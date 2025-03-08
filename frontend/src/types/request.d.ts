import { AxiosRequestConfig } from 'axios'

// 扩展AxiosRequestConfig类型
declare module 'axios' {
  export interface AxiosRequestConfig {
    // 是否验证文件类型
    validateFileType?: boolean
    // 允许的文件类型列表
    fileTypes?: string[]
    // 是否验证文件大小
    validateFileSize?: boolean
    // 最大文件大小（MB）
    maxSize?: number
  }
} 