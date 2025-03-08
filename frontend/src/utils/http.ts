import axios from 'axios'
import { Message } from '@arco-design/web-vue'

// 创建axios实例
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(
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
http.interceptors.response.use(
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
          window.location.href = '/login'
          break
        case 403:
          Message.error('没有权限访问该资源')
          break
        case 404:
          Message.error('请求的资源不存在')
          break
        case 500:
          Message.error('服务器错误，请稍后重试')
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

export default http 