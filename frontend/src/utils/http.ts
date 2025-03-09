import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { Message } from '@arco-design/web-vue'
import { getToken, removeToken, removeRefreshToken, getRefreshToken, setToken } from './auth'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 是否正在刷新token
let isRefreshing = false
// 等待刷新token的请求队列
let requests: Array<(token: string) => void> = []

// 刷新token
const refreshToken = async () => {
  try {
    const refreshTokenValue = getRefreshToken()
    if (!refreshTokenValue) {
      console.log('没有刷新令牌，无法刷新访问令牌')
      return null
    }
    
    console.log('开始刷新访问令牌，当前刷新令牌:', refreshTokenValue.substring(0, 15) + '...')
    
    // 直接使用axios而不是service，避免循环调用
    const response = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'}/api/auth/refresh`,
      {},  // 不需要在请求体中发送refresh_token
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${refreshTokenValue}`  // 在头部使用刷新令牌
        }
      }
    )
    
    console.log('刷新令牌响应:', response.data)
    
    // 处理不同的响应格式
    if (response.data && response.data.access_token) {
      console.log('成功获取新的访问令牌(直接格式)')
      return response.data.access_token
    } else if (response.data && response.data.code === 200 && response.data.data && response.data.data.access_token) {
      console.log('成功获取新的访问令牌(标准格式)')
      return response.data.data.access_token
    }
    
    console.error('刷新令牌响应格式不正确:', response.data)
    return null
  } catch (error: any) {
    console.error('刷新令牌失败:', error)
    
    // 记录更详细的错误信息
    if (error.response) {
      console.error('错误状态码:', error.response.status)
      console.error('错误数据:', error.response.data)
    }
    
    return null
  }
}

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = getToken()
    
    // 调试信息
    console.log(`请求URL: ${config.url}`)
    console.log(`请求方法: ${config.method?.toUpperCase()}`)
    console.log(`当前Token: ${token ? token.substring(0, 15) + '...' : '无'}`)
    
    // 如果有token则添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('已添加Authorization头')
    } else {
      console.warn('没有可用的Token，请求将不包含Authorization头')
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
  async error => {
    // 处理错误响应
    const { response, config } = error
    
    // 如果是401错误且不是刷新token的请求，尝试刷新token
    if (response && response.status === 401 && !config.url.includes('/api/auth/refresh')) {
      if (!isRefreshing) {
        isRefreshing = true
        
        try {
          const newToken = await refreshToken()
          
          if (newToken) {
            // 更新token
            setToken(newToken)
            
            // 更新当前请求的token
            config.headers.Authorization = `Bearer ${newToken}`
            
            // 执行队列中的请求
            requests.forEach(cb => cb(newToken))
            requests = []
            
            // 重试当前请求
            return service(config)
          } else {
            // 刷新token失败，清除登录状态
            removeToken()
            removeRefreshToken()
            Message.error('登录已过期，请重新登录')
            
            // 重定向到登录页（在组件中处理）
            return Promise.reject(error)
          }
        } catch (refreshError) {
          console.error('刷新token失败:', refreshError)
          
          // 清除登录状态
          removeToken()
          removeRefreshToken()
          Message.error('登录已过期，请重新登录')
          
          return Promise.reject(error)
        } finally {
          isRefreshing = false
        }
      } else {
        // 将请求加入队列
        return new Promise(resolve => {
          requests.push((token: string) => {
            config.headers.Authorization = `Bearer ${token}`
            resolve(service(config))
          })
        })
      }
    }
    
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
          removeToken()
          removeRefreshToken()
          // 跳转到登录页（在组件中处理）
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
        case 422:
          // 对422错误进行更详细的处理
          console.error('验证错误详情:', data)
          if (data && data.message) {
            Message.error(data.message)
          } else if (data && data.errors) {
            // 如果有具体的字段错误信息
            const errorMessages = Object.values(data.errors).flat() as string[]
            if (errorMessages.length > 0) {
              Message.error(errorMessages[0])
            } else {
              Message.error('请求数据验证失败')
            }
          } else {
            Message.error('请求数据验证失败')
          }
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