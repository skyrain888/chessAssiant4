import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { Message } from '@arco-design/web-vue'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    
    // 如果有token则添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    // 如果响应包含data字段，则返回data
    return response.data
  },
  error => {
    // 处理错误响应
    const { response } = error
    
    if (response) {
      // 服务器返回了错误状态码
      const { status, data } = response
      
      switch (status) {
        case 400:
          Message.error(data.message || '请求参数错误')
          break
        case 401:
          Message.error('未授权，请重新登录')
          // 清除token
          localStorage.removeItem('token')
          localStorage.removeItem('refreshToken')
          // 跳转到登录页
          window.location.href = '/auth/login'
          break
        case 403:
          Message.error('没有权限访问该资源')
          break
        case 404:
          Message.error('请求的资源不存在')
          break
        case 408:
          Message.error('请求超时')
          break
        case 500:
          Message.error('服务器错误，请稍后重试')
          break
        case 502:
          Message.error('网关错误')
          break
        case 503:
          Message.error('服务不可用')
          break
        case 504:
          Message.error('网关超时')
          break
        default:
          Message.error(data.message || `请求失败(${status})`)
      }
    } else {
      // 网络错误或请求被取消
      Message.error('网络错误，请检查您的网络连接')
    }
    
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

// 封装GET请求
export function get<T>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.get(url, { params, ...config })
}

// 封装POST请求
export function post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.post(url, data, config)
}

// 封装PUT请求
export function put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  return service.put(url, data, config)
}

// 封装DELETE请求
export function del<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  return service.delete(url, config)
}

// 封装上传文件请求
export function upload<T>(url: string, file: File | FormData, config?: AxiosRequestConfig & {
  validateFileType?: boolean;
  fileTypes?: string[];
  validateFileSize?: boolean;
  maxSize?: number;
}): Promise<T> {
  // 如果是File对象，则进行验证并创建FormData
  if (file instanceof File) {
    // 检查文件类型
    if (config?.validateFileType !== false && config?.fileTypes) {
      const fileTypes = config.fileTypes
      if (!fileTypes.includes(file.type)) {
        return Promise.reject(new Error(`不支持的文件类型: ${file.type}`))
      }
    }
    
    // 检查文件大小
    if (config?.validateFileSize !== false && config?.maxSize) {
      const maxSize = config.maxSize
      const fileSize = file.size / 1024 / 1024 // 转换为MB
      if (fileSize > maxSize) {
        return Promise.reject(new Error(`文件大小不能超过 ${maxSize}MB`))
      }
    }
    
    const formData = new FormData()
    formData.append('file', file)
    
    return service.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    })
  } 
  // 如果已经是FormData对象，直接发送
  else {
    return service.post(url, file, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      ...config
    })
  }
}

export default {
  get,
  post,
  put,
  del,
  upload,
  service
} 